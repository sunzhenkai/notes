# MVP 2：独立长任务 Agent 应用

## 定位

独立 Agent 应用是可部署的 Agent Service 与长任务执行系统。它面向需要异步提交、等待外部事件、失败恢复、人工审批或跨较长时间推进的任务。

**依赖原则**：应用必须依赖 [MVP 1：通用 Agent Library](./agent-library-mvp.md)。Service 的在线执行路径与 Task Worker 的 Agent Slice 都调用同一个 `AgentRunner`，不得复制 Agent Loop。

长任务不等于一个永久运行的 Agent Run。一个 `AgentTask` 由多个有界 Slice 和等待阶段组成；等待、Signal、Timer、重试和状态恢复由 Workflow 负责，模型推理和工具调用由 Library 负责。

## 目标与非目标

### MVP 目标

- 提供独立 HTTP/SSE 接入；
- 支持在线有界运行，以证明 Service 直接复用 Library；
- 支持 Task 的提交、状态查询、事件订阅、Signal 和取消；
- 使用 Temporal 可靠推进一个版本固定的 `AgentTask`；
- Worker 在 Activity 中调用 Library 执行有界 Agent Slice；
- 持久化 checkpoint、result 和 artifact 引用；
- 支持 Worker 重启后的恢复、Activity 重试和 Workflow Continue-As-New；
- 对副作用提供稳定幂等键和状态不确定处置路径；
- 由可信配置解析并固定 ExecutionTarget。

### MVP 非目标

- 通用 BPM、任意 DAG 或低代码流程平台；
- 承载非 Agent 类型的组织级任务中心；
- 用户、租户、RBAC 和组织管理后台；
- 动态 Worker 市场、跨区域容灾和多 Cluster 治理；
- 多 Agent 协同 Workspace；
- 默认开放 Shell、代码执行、浏览器或不可信依赖；
- 完整 Sandbox 平台，除非首个验证任务明确需要隔离执行；
- `scheduleTask` 默认不进入首个 MVP，除非首个真实用例必须定时触发。

## 逻辑与部署架构

```text
Client / Host
      │ HTTP / SSE
      ▼
┌──────────────────────────────┐
│ Agent Service                │
│  ├─ Auth/Scope Adapter       │
│  ├─ Online Run API           │──in-process──> Agent Library
│  ├─ Task API / Task Facade   │
│  ├─ Provider Registry        │
│  └─ Event / Status Read API  │
└──────────────┬───────────────┘
               │ start/signal/query/cancel
               ▼
┌──────────────────────────────┐
│ Temporal                     │
│  AgentTaskWorkflow           │
│  deterministic state only    │
└──────────────┬───────────────┘
               │ schedule Activity
               ▼
┌──────────────────────────────┐
│ Environment Task Worker      │
│  RunAgentSliceActivity       │
│          │ in-process        │
│          ▼                   │
│  MVP 1 Agent Library         │
└───────┬───────────┬──────────┘
        │           │
        ▼           ▼
 Agent State     Artifact Store
 checkpoint      files/reports
```

Service 与 Worker 建议分进程部署，以隔离在线请求和长任务资源；二者可位于同一仓库，并依赖同一版本的 Library package。

## 核心领域对象

| 对象 | 含义 | 状态归属 |
|------|------|----------|
| `AgentDefinition` | 版本化的行为、Prompt、工具和 Provider 配置 | Service 配置存储 |
| `AgentRun` | 一次有边界的 Library 执行 | Library 运行态 + 事件存储 |
| `AgentTask` | 需要可靠推进的逻辑长任务 | Task Store + Temporal Workflow |
| `TaskAttempt` | Worker 对某个 Slice 的一次实际尝试 | Task/事件存储 |
| `ExecutionTarget` | 环境、Namespace、Task Queue、capability、policy 和 secret scope 的可信解析结果 | Service 配置存储 |
| `CheckpointRef` | 可恢复 Agent 状态的引用 | Agent State Provider |
| `ArtifactRef` | 文件、报告、快照或大结果引用 | Artifact Provider |

Task 创建时固定 `AgentDefinition` 版本和 `ExecutionTarget`。模型、Prompt、用户输入和工具结果都不能修改它们。

## 最小外部接口

具体 URL 可按实现调整，但 MVP 语义至少包含：

| 操作 | 建议接口 | 语义 |
|------|----------|------|
| 在线运行 | `POST /v1/runs` | 调用 Library 执行一次有界 Run |
| 在线/任务事件 | `GET /v1/runs/{runId}/events` | SSE 订阅版本化事件 |
| 提交任务 | `POST /v1/tasks` | 创建 AgentTask，固定 Definition 与 Target |
| 查询状态 | `GET /v1/tasks/{taskId}` | 返回阶段、进度、结果/错误引用 |
| 发送 Signal | `POST /v1/tasks/{taskId}/signals` | 提交审批、外部数据或继续指令 |
| 取消任务 | `POST /v1/tasks/{taskId}/cancel` | 请求 Workflow 与执行中的 Activity 协同取消 |

`submitTask` 返回 `taskId`，不等待任务完成。重复提交应支持客户端幂等键，返回同一逻辑 Task 或明确冲突。

## Workflow 与 Slice

```text
submitTask
    ↓
创建并固定 DefinitionRef + ExecutionTarget
    ↓
启动 AgentTaskWorkflow
    ↓
调度 RunAgentSliceActivity
    ↓
Worker 调用 MVP 1 AgentRunner
    ├─ completed ──> 保存 resultRef ──> Task 完成
    ├─ paused: approval/signal ──> 保存 checkpointRef ──> Workflow 等待
    ├─ paused: budget boundary ──> 保存 checkpointRef ──> 下一 Slice
    └─ retryable failure ──> Temporal 按策略重试

Workflow History 达到阈值 ──> Continue-As-New，仅传稳定 ID/引用
```

### Workflow/Activity 硬边界

Temporal Workflow 仅保存确定性编排状态、Timer、Signal、取消和稳定引用。以下操作只能发生在 Activity：

- LLM 或 Agent Loop；
- Context/Memory 访问；
- Tool 和网络调用；
- checkpoint/artifact I/O；
- Sandbox 创建和执行。

MVP 默认使用粗粒度 `RunAgentSliceActivity`。只有高风险写工具、需要独立重试的外部副作用或恢复成本过高的步骤，才考虑拆分为独立 `ExecuteToolActivity`；该粒度在真实任务验证前不冻结。

## 状态所有权

| 状态 | Owner | 不应存放的位置 |
|------|-------|----------------|
| Workflow 阶段、Timer、Signal | Temporal | Prompt、完整对话、大文件 |
| Task 查询视图、Attempt、关联 ID | Task Store | Library 内存作为唯一来源 |
| 对话、Memory、checkpoint | Agent State Provider | Temporal History |
| 文件、报告、快照、大结果 | Artifact Provider | Event 或 Workflow payload |
| 业务事实 | 上游宿主系统 | Agent Task 状态 |
| 计算租约 | Sandbox Manager（若启用） | checkpoint 或长期状态 |
| Definition、Policy、Target | Service 配置存储 | 模型输入 |

跨系统只传稳定 ID 和引用，避免把敏感正文、凭据或大对象放入事件、日志和 Workflow History。

## 可靠性与幂等

MVP 采用 at-least-once 执行语义，不承诺 exactly-once。

- Task 创建使用客户端幂等键；
- 每次 Slice 具有稳定 `runId`，每次尝试具有独立 `attemptId`；
- Tool 调用携带 `toolCallId`；
- 副作用写调用使用由 `taskId + logicalStep + toolCallId` 派生的稳定 `idempotencyKey`；
- Activity 重试可以产生新 Attempt，但不能产生新逻辑 Task 或新副作用键；
- 结果未知的副作用不得盲目重试，应查询历史结果、执行补偿或转人工；
- deadline 与取消传播到 Library 和 Provider；
- checkpoint 必须在 Slice 边界持久化成功后，Workflow 才推进阶段。

## 安全边界

- 上游身份适配器签发最小 Scope；
- Service 通过可信策略把请求映射到 ExecutionTarget；
- Worker 只监听被授权的 Task Queue；
- 凭据通过目标环境注入并短期化，不进入 Prompt、Task payload 或 checkpoint；
- Policy 不可用时高风险能力 fail closed；
- 若未实现 Sandbox，则拒绝 Shell、任意代码、浏览器和不可信依赖执行，不得退化到 Worker 主机直接运行；
- Artifact 和事件读取沿用上游授权，不因知道 ID 即可访问。

## 故障与降级

| 故障 | MVP 行为 |
|------|----------|
| Service 重启 | 已提交 Workflow 不受影响；API 恢复后可继续查询 |
| Worker 重启 | Temporal 重新投递未完成 Activity；沿用稳定幂等键 |
| Temporal 不可用 | 新 Task 明确返回能力不可用；不得静默改为进程内任务 |
| Agent State 不可用 | 不启动下一 Slice；按可重试策略处理 |
| Artifact Store 不可用 | 需要 Artifact 的任务暂停或失败，不把大结果塞入 Workflow |
| Policy 不可用 | 高风险工具拒绝；低风险是否降级由配置决定 |
| Signal 重复 | 依据 signalId 去重 |
| 取消与工具调用竞态 | 停止新调用；已发出的副作用按幂等/状态查询处理 |
| Sandbox 不可用 | 需要隔离执行的任务失败或暂停，不在宿主降级执行 |

## MVP 验收场景

选取一个真实长任务，至少包含两个 Agent Slice 和一次跨时间等待。验收应证明：

- Task 提交后立即返回 `taskId`，可持续查询状态和订阅事件；
- 第一个 Slice 调用 MVP 1，生成 checkpoint 后等待 Signal；
- Worker 在等待期间可重启，Signal 到达后由另一 Worker 恢复；
- 重复 Activity 或重复 Signal 不产生重复业务副作用；
- Task 可取消，取消后不再调度新 Slice；
- Workflow History 达到测试阈值时可 Continue-As-New；
- 在线 Run 与 Task Slice 使用相同 Definition 和 Library package；
- 关闭 Task Module 后在线 Run 仍可使用；
- 事件可通过 `taskId/runId/attemptId/toolCallId` 关联；
- 未启用 Sandbox 时，高风险执行工具被明确拒绝。

## 主要取舍

- **选择 Temporal，而不是进程内队列**：获得持久 Timer、Signal、重试和恢复；接受额外基础设施与确定性约束。
- **选择多个有界 Slice，而不是永久 Agent Run**：获得可取消、可计费和可恢复边界；接受 checkpoint 兼容成本。
- **Service 与 Worker 分进程**：隔离在线与后台资源；接受部署单元增加。
- **首个 MVP 不建设通用任务平台**：快速验证 Agent 长任务；未来若承载非 Agent 工作负载，应独立立项。
- **Sandbox 按风险触发**：降低首版成本；代价是未启用时必须拒绝部分高风险任务。

## 相关文档

- [MVP 总览](./README.md)
- [MVP 1：通用 Agent Library](./agent-library-mvp.md)
- [开放问题与决策门](./open-questions.md)
- [通用 Agent Service 与可执行任务模块架构](../agent-service-task-module-architecture.md)
