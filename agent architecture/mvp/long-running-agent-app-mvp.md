# MVP 2：独立长任务 Agent Application

## 定位

Agent Application 是面向用户的独立产品，提供必选 UI、应用 API 和可恢复的 Task Runtime。它负责管理 Task，不负责重新实现 Agent。

**依赖原则**：Task Worker 通过 `AgentClient` 调用 [MVP 1：通用 Agent Library](./agent-library-mvp.md) 的能力契约。Application、UI 和 Task 模型不得直接依赖 Pi 或其他 Harness 专有 API。

首个长任务不要求复杂 Workflow。MVP 使用数据库持久化、Worker Lease、Heartbeat、Checkpoint 和 Recovery Scanner 提供简单管理与进程重启恢复，不引入 Temporal。

## 目标与非目标

### MVP 目标

- 提供任务创建、列表、详情和结果查看 UI；
- 支持 Task 的提交、查询、事件查看、取消、重试和恢复；
- 使用持久化 Task Store 保存 Task、Attempt、Lease、Event 和引用；
- Worker 通过 `AgentClient` 调用 Library 执行一个或多个有界 Agent Run；
- 通过 Lease 和 Heartbeat 检测失联 Worker；
- Worker 重启或 Lease 过期后，从 checkpoint 恢复或进入明确失败状态；
- 将 AgentEvent 持久化并投影为用户可理解的 Task Timeline；
- 对副作用提供稳定幂等键和状态不确定处置路径；
- 保持语言、Web 框架和数据库产品未绑定。

### MVP 非目标

- Temporal、通用 BPM、任意 DAG 或低代码流程平台；
- Timer、周期调度、复杂 Signal 和长达数天的确定性 Workflow；
- 承载非 Agent 类型的组织级任务中心；
- 用户、租户、RBAC 和组织管理后台；
- 动态 Worker 市场、跨区域容灾和多 Cluster 治理；
- 多 Agent 协同 Workspace；
- 默认开放 Shell、代码执行、浏览器或不可信依赖；
- 完整 Sandbox 平台；
- 首版同时实现 Local 与 Remote 两种 Agent Binding。

## 逻辑架构

```text
┌──────────────────────────────────────────────┐
│ Browser UI                                   │
│ 创建 / 列表 / 详情 / Timeline / 操作 / 结果 │
└──────────────────────┬───────────────────────┘
                       │ Application API
                       ▼
┌──────────────────────────────────────────────┐
│ Task Service                                 │
│ create / list / get / cancel / retry / resume│
└───────────────┬──────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────┐
│ Durable Task Store                          │
│ Task / Attempt / Lease / Event / Ref         │
└───────────────┬──────────────────────────────┘
                │ claim / heartbeat / recover
       ┌────────┴────────┐
       ▼                 ▼
┌───────────────┐  ┌──────────────────┐
│ Task Worker   │  │ Recovery Scanner │
│     │         │  │ expired leases   │
│     ▼         │  └──────────────────┘
│ AgentClient   │
└───────┬───────┘
        │ local package or remote protocol
        ▼
┌──────────────────────────────────────────────┐
│ MVP 1 Agent Library                         │
│ Harness / Skill / Tool / Session / Event     │
└──────────────────────────────────────────────┘
```

UI 只能访问 Application API，不能直接调用 Library、数据库或 Harness。

## UI MVP

UI 是产品必选项，但首版只覆盖 Task 闭环，不建设复杂聊天工作台。

### 任务列表

至少展示 Task ID、标题、状态、当前阶段、更新时间和尝试次数，并支持按状态过滤。

### 创建任务

至少支持任务描述、Agent Definition、Skill 选择和输入参数。Harness、凭据和执行环境等内部配置不直接暴露给普通用户。

### 任务详情

至少展示基本信息、状态、进度时间线、Agent Run、Tool 调用、错误、checkpoint/恢复记录和最终结果。

### 任务操作

根据状态提供 Cancel、Retry、Resume、补充恢复输入和查看 Artifact。所有操作必须经过 Application API 的状态校验和授权。

## 核心领域对象

| 对象 | 含义 | 状态归属 |
|------|------|----------|
| `AgentDefinitionRef` | 版本化的 Agent 行为引用 | Application 配置存储 |
| `Task` | 对用户稳定的逻辑长任务 | Task Store |
| `TaskAttempt` | Worker 对 Task 的一次执行尝试 | Task Store |
| `AgentRun` | Library 的一次有界执行 | Library 运行态 + Event Store |
| `Lease` | Worker 对 Task 的限时执行权 | Task Store |
| `SessionRef` | Agent 上下文连续性引用 | Session Provider |
| `CheckpointRef` | 可恢复 Agent 状态引用 | Agent State Provider |
| `ArtifactRef` | 文件、报告或大结果引用 | Artifact Provider |

关系：

```text
Task #123
├── Attempt 1
│   └── Agent Run R1
│       └── Checkpoint C1
├── Worker lost / Lease expired
└── Attempt 2
    └── Agent Run R2 resumes C1
        └── Completed
```

## Task 最小模型

```text
Task
├── id
├── version
├── title
├── input | input_ref
├── status
├── agent_definition_ref
├── skill_refs[]
├── session_ref?
├── current_run_id?
├── checkpoint_ref?
├── result_ref?
├── error?
├── attempt_count
├── lease_owner?
├── lease_expires_at?
├── created_at
└── updated_at
```

`version` 用于乐观锁，避免 UI、Worker 和 Recovery Scanner 并发覆盖状态。

## Task 状态机

```text
PENDING
   │
   ▼
RUNNING ───────────────┐
   │                   │
   ├──> PAUSED         │
   │       │           │
   │       └── resume ─┘
   │
   ├──> FAILED
   │       │
   │       └── retry ──> PENDING
   │
   ├──> CANCELLED
   │
   └──> COMPLETED
```

首版不增加更多外部状态。Lease 过期、恢复扫描等内部过程通过 TaskEvent 表达。

## Application API 语义

具体 URL 和传输协议可在实现阶段选择，但必须覆盖：

| 操作 | 语义 |
|------|------|
| Create Task | 创建 Task 并立即返回 task_id |
| List Tasks | 分页、按状态筛选和排序 |
| Get Task | 返回状态、当前 Run、错误和结果引用 |
| Get Task Events | 返回或流式订阅 Task Timeline |
| Cancel Task | 阻止新 Run，并请求取消当前 Run |
| Retry Task | 为 FAILED Task 创建新 Attempt |
| Resume Task | 从 PAUSED Task 的 checkpoint 继续 |
| Get Artifact | 经授权读取结果或 Artifact |

HTTP/JSON、SSE、WebSocket 或轮询均为实现选择；UI 不依赖 Harness 的原始事件协议。

## AgentClient 适配

Task Worker 只依赖：

```text
AgentClient
├── run(agent_run_spec) -> AgentEvent + AgentRunOutcome
└── cancel(run_id)
```

实现阶段可选择：

```text
LocalAgentClient
    同语言进程内调用 Agent Library

RemoteAgentClient
    不同语言或独立部署时通过 HTTP/RPC 调用
```

MVP 只实现其中一种。Task Service、状态机和 UI 不因 Binding 改变。

## Worker、Lease 与恢复

### 正常执行

```text
Worker 查询 PENDING Task
    ↓
原子 Claim 并写入 Lease
    ↓
Task -> RUNNING，创建 TaskAttempt
    ↓
调用 AgentClient，持久化 AgentEvent
    ↓
定期 Heartbeat 续租
    ↓
保存 checkpoint/result 后更新最终状态
    ↓
释放 Lease
```

### Worker 失联

```text
RUNNING Task
    ↓ Lease 超时
Recovery Scanner
    ↓
检查 checkpoint 与副作用状态
    ├── 可安全恢复 ──> 清理旧 Lease，Task -> PENDING
    └── 不可安全恢复 ──> Task -> FAILED，等待人工 Retry
```

约束：

- Claim 必须是原子操作；
- 同一 Task 同一时间最多存在一个有效 Lease；
- Lease 有限时长且 Worker 定期 Heartbeat；
- checkpoint 持久化成功后才能推进可恢复边界；
- 旧 Worker 在失去 Lease 后不得继续提交状态；
- AgentEvent 使用递增 sequence 去重和排序；
- 重复 Attempt 不得创建新的逻辑 Task。

## AgentEvent 与 TaskEvent

Library 产生 `AgentEvent`；Application 产生 `TaskEvent` 并把二者关联为 Timeline。

```text
Task Timeline
├── task.created
├── task.claimed
├── attempt.started
├── agent.run.started
├── agent.tool.completed
├── task.paused
├── lease.expired
├── task.recovered
└── task.completed
```

Application 负责持久化、脱敏、访问控制和 UI 投影，不修改 AgentEvent 的原始语义。

## Retry 与幂等

MVP 采用 at-least-once 执行语义，不承诺 exactly-once。

- Task 创建支持客户端幂等键；
- 每个 Attempt 使用独立 `attempt_id`；
- 每个 Agent Run 使用稳定 `run_id`；
- Tool 调用携带 `tool_call_id`；
- 副作用写操作使用由 task、逻辑步骤和 Tool 调用派生的稳定幂等键；
- Library 只处理单个 Run 内的有界瞬时重试；
- Application 负责跨 Attempt 的 Task Retry 和恢复；
- 状态未知的副作用不得自动重试，应查询历史结果、补偿或转人工。

## 状态所有权

| 状态 | Owner | 不应作为唯一来源的位置 |
|------|-------|--------------------------|
| Task、Attempt、Lease、TaskEvent | Task Store | Worker 内存 |
| 当前 Agent Run | Agent Library + Event Store | UI 本地状态 |
| Session、Checkpoint | Agent State Provider | Task Event payload |
| 文件、报告、大结果 | Artifact Provider | Task 表或事件正文 |
| 业务事实 | 上游宿主系统 | Agent Task 状态 |
| Definition、Policy、执行配置 | Application 配置存储 | 模型输入 |

跨模块优先传稳定 ID 和引用，避免把敏感正文、凭据或大对象写入事件。

## 安全边界

- 上游身份适配器签发最小 Scope；
- UI 和 API 不能选择或提升 Harness、凭据和执行权限；
- Worker 只执行可信配置允许的 AgentDefinition、Skill 和 Tool；
- 凭据不进入 Prompt、Task payload、checkpoint 或浏览器；
- Policy 不可用时高风险能力 fail closed；
- 未实现 Sandbox 时拒绝 Shell、任意代码、浏览器自动化和不可信依赖执行；
- Task、Event 和 Artifact 读取均执行访问控制，不能仅凭 ID 访问。

## 故障与降级

| 故障 | MVP 行为 |
|------|----------|
| API 重启 | Task 保持在持久化存储中，恢复后继续查询 |
| Worker 重启 | Lease 过期后由 Recovery Scanner 恢复或标记失败 |
| Task Store 不可用 | 不 Claim 新 Task，不在内存静默执行 |
| AgentClient 不可用 | 保留 checkpoint，按 Task 重试策略处理 |
| Agent State 不可用 | 不推进恢复边界，Task 暂停或失败 |
| Artifact Store 不可用 | 不把大结果塞入 Task/Event，明确失败或暂停 |
| Policy 不可用 | 高风险 Tool 拒绝 |
| UI 事件连接中断 | 通过 sequence 从上次位置恢复 Timeline |
| Cancel 与 Tool 竞态 | 停止新调用，已发出的副作用按幂等/状态查询处理 |
| Sandbox 不可用 | 需要隔离的 Task 失败，不在 Worker 主机降级执行 |

## MVP 验收场景

使用一个可在合理时间内完成、支持 checkpoint 的真实任务验证：

- 用户可在 UI 创建 Task，并立即在列表中看到状态；
- 详情页持续展示 Agent Run、Tool 和 Task 状态时间线；
- Worker 使用 AgentClient 调用同一 Agent Library；
- Worker 执行中断后，Lease 过期并产生可见恢复事件；
- 存在 checkpoint 时由新 Attempt 恢复，不存在安全 checkpoint 时明确失败；
- 用户可在 UI Cancel、Retry 或 Resume；
- 重复 Claim、Retry 或事件投递不产生重复逻辑 Task；
- Task、Attempt、Run、Tool 调用可通过关联 ID 追踪；
- UI 能查看最终结果或经授权访问 Artifact；
- Application 不包含第二套 Agent Loop，也不依赖 Harness 专有 API。

## 主要取舍

- **选择数据库 Durable Worker，而不是进程内后台任务**：获得重启恢复；接受 Lease 和并发控制复杂度。
- **首版不使用 Temporal**：降低基础设施和认知成本；复杂 Signal、Timer、长周期 Workflow 延后。
- **UI 为必选但保持任务导向**：完成产品闭环；不建设复杂聊天和协作工作台。
- **选择多个有界 Agent Run，而不是永久执行**：获得取消和恢复边界；需要管理 checkpoint 兼容。
- **AgentClient 隔离本地/远程 Binding**：设计不绑定语言；实现阶段仍需选定一种 Binding。

## Temporal 升级触发条件

出现以下任一真实需求时，再评估用 Temporal 或其他 Workflow Engine 替换 Task Runtime 内部实现：

- 任务持续数小时或数天并包含大量 Timer；
- 需要复杂 Signal、审批和分支编排；
- 需要多个 Activity 的独立重试和补偿；
- 数据库状态机难以保证恢复正确性；
- 需要完整、可重放的 Workflow History；
- Worker 类型和执行环境显著增加。

升级不得改变 UI 的核心 Task 语义或 Agent Library 契约。

## 相关文档

- [MVP 总览](./README.md)
- [MVP 1：通用 Agent Library](./agent-library-mvp.md)
- [开放问题与决策门](./open-questions.md)
- [通用 Agent Service 与可执行任务模块架构](../agent-service-task-module-architecture.md)
