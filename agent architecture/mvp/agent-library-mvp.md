# MVP 1：通用 Agent Library

## 定位

通用 Agent Library 是可嵌入宿主进程的 Agent 执行内核。它提供一致的 Agent Loop、上下文组装、工具调用、安全 Hook 和事件模型，但不拥有宿主的身份系统、业务数据或运行基础设施。

**MVP 成功定义**：至少两种宿主形态通过同一个 npm package 完成有界 Agent Run，且其中一个宿主是独立长任务 Agent 应用。

## 目标与非目标

### MVP 目标

- 提供稳定、最小的 TypeScript 运行入口；
- 使用 Pi `agent-core` 作为默认 Runtime，但公共接口不暴露 Pi 专有类型；
- 支持显式注册、TypeBox 校验的业务工具；
- 在每次工具调用前执行宿主提供的授权 Hook；
- 支持宿主注入 Context/Memory、Model、Telemetry 等 Provider；
- 输出统一的流式事件与错误；
- 支持 deadline、取消和运行预算，保证单次 Run 有界；
- 为长任务提供 checkpoint/result/artifact 引用语义，但不实现 Workflow。

### MVP 非目标

- HTTP Server、BFF、RPC 服务；
- 后台队列、定时调度、Temporal Workflow；
- 用户、租户、RBAC 和管理后台；
- 数据库、向量库、Artifact Store 的产品化实现；
- 原始 Shell、数据库或内部 HTTP 等默认高权限工具；
- 通用多 Agent DAG、组织级策略平台或多 Harness 路由；
- Sandbox 基础设施。

## 逻辑架构

```text
宿主应用
  ├─ identity / session / business data
  ├─ AgentDefinition
  ├─ Scope
  └─ Providers + Tools
           │
           ▼
┌──────────────────────────────────────────┐
│ Agent Library                            │
│                                          │
│  AgentRunner                             │
│    ├─ Context Builder                    │
│    ├─ Runtime Adapter (default: Pi)      │
│    ├─ Tool Registry + Schema Validation  │
│    ├─ Authorize Hook                     │
│    ├─ Budget / Deadline / Cancellation   │
│    └─ Event + Error Normalization        │
└──────────────────────────────────────────┘
           │ capability contracts
           ▼
 Model / Context / Memory / Policy / Telemetry Providers
```

## 组件职责

| 组件 | MVP 职责 | 明确不负责 |
|------|----------|------------|
| `AgentRunner` | 驱动一次有界 Agent Run | 长期任务推进和重试 |
| `RuntimeAdapter` | 适配 Pi 的模型和 Agent Loop | 向公共 API 泄漏 Pi 类型 |
| `ContextBuilder` | 组装输入、允许的上下文和 checkpoint | 决定数据保留期 |
| `ToolRegistry` | 显式注册、Schema 校验和调度工具 | 自动发现高权限工具 |
| `Authorize` | 工具执行前允许、拒绝或请求审批 | 取代宿主 RBAC |
| `EventSink` | 输出版本化运行事件 | 持久保存所有事件 |
| Provider ports | 隔离模型、记忆、策略和观测实现 | 绑定具体厂商 SDK |

## 最小公共契约

以下为语义草案，用于约束边界，不代表最终文件布局：

```ts
type AgentDefinitionRef = {
  definitionId: string
  version: string
}

type AgentRunRequest = {
  runId: string
  definition: AgentDefinitionRef
  input?: unknown
  inputRef?: string
  scope: Record<string, string>
  checkpointRef?: string
  deadlineAt?: string
  budget?: {
    maxTurns?: number
    maxToolCalls?: number
    maxTokens?: number
    maxCost?: number
  }
}

type AgentRunResult = {
  status: "completed" | "paused" | "cancelled" | "failed"
  resultRef?: string
  checkpointRef?: string
  artifactRefs?: string[]
  pauseReason?: "approval" | "external_signal" | "budget_boundary"
  error?: AgentError
}

interface AgentRunner {
  run(request: AgentRunRequest, options: RunOptions): Promise<AgentRunResult>
}
```

`scope` 由宿主签发并最小化，可包含 `userId`、`tenantId`、`conversationId` 和业务对象标识。Library 只将必要字段或其派生物传给 Provider、Tool 和 Authorize，不建立自己的 Workspace 或权限体系。

### Tool 契约

每个 Tool 至少包含：

- 稳定名称和版本；
- TypeBox 参数 Schema；
- 执行器；
- 风险级别和是否具有副作用；
- 可选的幂等能力描述；
- timeout/deadline 行为。

执行顺序固定为：参数校验 → 授权 → 执行 → 结果归一化 → 事件输出。Schema 校验和 Prompt 不能替代授权。

### Event 契约

事件至少覆盖：

- `run.started` / `run.completed` / `run.failed`；
- `text.delta`；
- `tool.requested` / `tool.authorized` / `tool.started` / `tool.completed` / `tool.failed`；
- `checkpoint.created`；
- `run.paused` / `run.cancelled`。

每个事件包含 `schemaVersion`、`eventId`、`occurredAt`、`runId` 和关联上下文。事件载荷不得默认包含完整 Prompt、凭据或敏感工具结果。

## 单次运行流程

```text
宿主创建 request
    ↓
校验 Definition、Scope、deadline 和 budget
    ↓
ContextBuilder 读取必要上下文 / checkpoint
    ↓
RuntimeAdapter 驱动 Agent Loop
    ↓
模型请求工具 ──> Schema 校验 ──> Authorize ──> Tool
    │                                           │
    └────────────── Event stream <──────────────┘
    ↓
完成，或因审批/预算/取消生成 checkpoint
    ↓
返回 result/checkpoint/artifact 引用
```

## 依赖规则

Library 可以依赖：

- Pi Agent Core 与 TypeBox；
- 轻量、无基础设施绑定的公共类型和工具函数；
- 宿主通过接口注入的 Provider。

Library 不得依赖：

- Fastify 或其他 HTTP 框架；
- Temporal、队列、数据库客户端；
- 具体 Memory、Artifact、Sandbox 或观测厂商 SDK；
- 独立 Agent 应用的 Task、Workflow、Worker 类型。

## 状态与故障语义

| 情况 | MVP 行为 |
|------|----------|
| 可选 Memory 未配置 | 无记忆运行，并输出明确能力信息 |
| Authorize 未配置 | 仅允许显式标记为低风险只读的工具；其他工具拒绝 |
| Policy Provider 不可用 | 高风险工具 fail closed |
| Tool 超时 | 遵守 deadline，返回分类错误并发出失败事件 |
| 取消 | 停止继续发起模型/工具调用，返回 `cancelled` |
| 达到预算 | 生成 checkpoint，返回 `paused: budget_boundary` |
| 副作用结果未知 | 返回 `effect_unknown` 类错误，不自动假定失败并重试 |
| Event Sink 失败 | 不阻塞低风险运行；审计强制场景由宿主配置 fail closed |

## MVP 验收标准

- 普通 Node.js 宿主可只安装 Library 完成运行；
- 独立长任务应用的 Worker 使用同一 `AgentRunner` 完成一个 Slice；
- Tool 参数在执行前经过 Schema 校验和 Authorize；
- deadline、取消、最大轮次和最大工具数至少各有一种可验证路径；
- 事件消费者可重建一次 Run 的关键时间线；
- 替换 Model、Context/Memory 或 Telemetry Provider 不修改 Agent Loop；
- 未配置可选 Provider 时的降级或拒绝行为明确；
- package 依赖树中不存在 Temporal、Web 框架或具体存储实现；
- 公共契约不暴露 Pi 专有类型。

## 主要取舍

- **选择 package 内进程调用，而不是先做远程服务**：获得最低集成延迟和最强宿主控制；跨语言能力延后。
- **选择有界 Run，而不是在 Library 内实现永久循环**：便于取消、计费、恢复和被 Workflow 调度。
- **选择能力 Provider，而不是统一大而全 Runtime**：降低基础设施耦合，但要求 Provider 生命周期和错误语义一致。
- **checkpoint 使用 opaque ref**：避免 Library 管理持久化，但跨版本恢复需要应用侧定义兼容策略。

## 相关文档

- [MVP 总览](./README.md)
- [MVP 2：独立长任务 Agent 应用](./long-running-agent-app-mvp.md)
- [Agent Library 架构入口](../README.md)
- [可插拔外围 Runtime 架构](../runtime-architecture.md)
