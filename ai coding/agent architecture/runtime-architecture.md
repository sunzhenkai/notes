# 可插拔外围 Runtime 架构

> 本文定义围绕 [自建可嵌入 Agent Library](./README.md) 的外围 Runtime 能力槽位、接入边界与候选实现。它不要求第一阶段部署独立平台；组件应按真实需求启用。面向可部署服务、Temporal 任务和 Sandbox 的组合方案见[通用 Agent Service 与可执行任务模块架构](./agent-service-task-module-architecture.md)。

## 结论

“Runtime”不是一个单一、可由 OpenViking 或 Temporal 互换实现的组件，而是一组独立的能力槽位：

```text
宿主应用
身份 / 业务数据 / UI / 业务授权
        │
        ▼
Agent Library
Context Builder / Tool Registry / Authorize Hook / Event Stream
        │
        ├─ Agent Runtime          Pi
        ├─ Context Runtime        OpenViking
        ├─ Workflow Runtime       Temporal
        ├─ Tool Runtime           直接工具 / MCP Client / MCP Gateway
        ├─ Execution Runtime      Sandbox
        ├─ Policy Runtime         宿主策略 / Policy Engine
        └─ Telemetry Runtime      OpenTelemetry / 观测与评测 Provider
```

核心库依赖各槽位的稳定契约，而非具体产品 SDK；宿主按部署、风险和业务要求组合 Provider。一个产品可覆盖多个槽位，但不能因此混淆职责。

## 分层与边界

| 层 | 职责 | 不负责 |
|---|---|---|
| 宿主应用 | 身份、租户、业务授权、业务数据、UI、业务工具与凭据来源 | Agent Loop、Provider 适配细节 |
| Agent Library | 单次 Agent 运行、Prompt/Context 组装、工具调度、统一事件与错误 | 持久队列、组织级策略、Sandbox 基础设施 |
| Agent Runtime | 模型交互、Agent Loop、工具调用、运行中状态 | 跨运行持久化工作流与业务权限 |
| 外围 Runtime Provider | 提供特定的上下文、任务、工具、隔离、策略或观测能力 | 取代宿主的业务系统 |

`scope` 继续由宿主定义与签发。所有 Provider 都接收经过最小化处理的 `scope` 或其受限派生物，用于隔离、授权和审计；不应把原始凭据、完整业务对象或不必要的用户数据传播给每个 Provider。

## 能力槽位

### 1. Agent Runtime

| 项目 | 内容 |
|---|---|
| 职责 | 执行 LLM 调用、Agent Loop、工具调用、流式事件与运行中状态 |
| 默认实现 | `@earendil-works/pi-agent-core` |
| 必要程度 | **P0：第一阶段必需** |
| 接入位置 | `Pi Runtime Adapter` |
| 替换条件 | 需要不同语言 Runtime、专用 Coding Harness 或不同的会话/扩展能力 |

Pi 的 `agent-core` 提供状态化 Agent、工具调用、上下文转换、工具 Hook 与流式事件；其上层 `AgentHarness` 还负责会话持久化、运行配置、资源解析、操作锁与保存点。本文中的外围 Runtime 不应重复实现这些内核能力。

### 2. Context Runtime

| 项目 | 内容 |
|---|---|
| 职责 | 管理知识、资源、技能与长期记忆，并按任务检索、压缩和组装上下文 |
| 推荐实现 | OpenViking |
| 必要程度 | **P1：有持久知识、跨会话记忆或 Skills 管理需求时引入** |
| 接入位置 | `Context Builder` 前的 `ContextRuntime` Provider |
| 状态归属 | Provider 保存上下文资产；宿主定义数据源、scope 与保留策略 |

OpenViking 是 Context Runtime，不只是向量记忆：它把 memory、resources 与 skills 统一为 `viking://` 虚拟文件系统，以 L0（摘要）、L1（概览）、L2（完整内容）分层按需加载，支持目录递归检索和检索轨迹观察；session commit 后还能异步提炼长期记忆。它不执行 Agent Loop，也不提供任务调度或可靠重试。

可选候选：

| 候选 | 适用场景 | 注意事项 | 阶段 |
|---|---|---|---|
| OpenViking | 统一知识、记忆、资源与 Skills；需要层级化、可解释的上下文装配 | 将其能力建模为 `ContextRuntime`，不要只降级为 `Memory` KV 接口 | P1 |
| Mem0 | 用户偏好、对话事实与轻量个性化记忆 | 更适合 memory 子槽位，不替代知识/技能目录 | P1/P2 |
| Graphiti / Zep | 实体关系及“何时为真”的时态事实 | Zep 托管化倾向较强；自建 Graphiti 需自行承担图存储与运维 | P2 |
| 宿主自有 RAG | 已有知识库、权限模型和检索链路 | 通过 Provider 适配，不让 Library 绑定特定向量库 | P1 |

### 3. Workflow Runtime

| 项目 | 内容 |
|---|---|
| 职责 | 长任务、定时、重试、暂停恢复、人工等待与跨 Worker 编排 |
| 推荐实现 | Temporal |
| 必要程度 | **P2：长时间、异步或必须可靠恢复的任务出现后引入** |
| 接入位置 | `BackgroundJobProvider` / `WorkflowRuntime`，位于 Library 外围 |
| 状态归属 | Workflow Runtime 保存工作流历史；业务与上下文状态仍分别归宿主或对应 Provider |

Temporal 的 TypeScript Workflow 是可重放的确定性编排函数，外部 I/O、模型调用、工具调用必须作为 Activity 执行；它提供 Activity 重试、定时器、Signal、Query 与 Update。**不要将 Pi 的实时、非确定性 Agent Loop 直接实现为 Temporal Workflow。** 合理的边界是把“运行一次 Agent”“执行一个工具”“提交记忆”等包装为 Activity，由 Workflow 编排、等待与重试。

### 4. Tool Runtime

| 项目 | 内容 |
|---|---|
| 职责 | 发现、定义、调用与治理模型可使用的外部工具 |
| 默认实现 | 宿主显式注入的 TypeBox Tool |
| 必要程度 | **P0：显式业务工具必需；MCP 按需引入** |
| 接入位置 | `Tool Registry` 与 `Authorize Hook` |

工具按风险升级：

| 方式 | 适用场景 | 阶段 |
|---|---|---|
| Direct Tool | 少量业务明确、可校验的内部工具 | P0 |
| MCP Client | 要复用标准化第三方/跨团队工具时 | P1 |
| MCP Gateway | 多租户、第三方 MCP、配额、审计、输出脱敏或人工审批 | P2 |

MCP 是工具协议，不是权限边界。MCP Gateway 可提供认证、工具白名单、参数 Schema 校验、限流、审计及审批；它应作为高风险工具的统一入口，而非把授权逻辑写进 Prompt。

### 5. Execution Runtime

| 项目 | 内容 |
|---|---|
| 职责 | 在受控环境中执行文件、进程、浏览器、代码或受限网络操作 |
| 候选实现 | E2B、宿主自建容器/VM/microVM |
| 必要程度 | **P2：运行不可信代码、Shell、浏览器自动化或高风险网络工具时必需** |
| 接入位置 | 工具实现之后的 `ExecutionRuntime` Provider |

E2B 提供按需创建的 Firecracker microVM Sandbox，适用于隔离执行 AI 生成代码。普通的低风险业务 API 工具不应强制经过 Sandbox。执行环境的最小权限、文件挂载、网络 egress allowlist、资源上限、生命周期和产物处理必须由 Provider 契约显式表达。

### 6. Policy 与 Identity Runtime

| 项目 | 内容 |
|---|---|
| 职责 | 根据主体、scope、工具、参数、风险、预算与来源决定允许、拒绝或等待审批 |
| 默认实现 | 宿主在 `Authorize` Hook 中实现 |
| 候选扩展 | OPA、Cedar、MCP Gateway 内置策略 |
| 必要程度 | **P0：基础授权必需；P2：集中策略引擎与审批** |

策略判定必须位于工具调用前的强制执行路径。模型不得拿到长期原始凭据；工具执行时由宿主或凭据 Provider 注入最小权限、短期的凭据。策略和审计只记录脱敏参数与决定，不默认记录敏感正文。

### 7. Telemetry、Observability 与 Evaluation Runtime

| 项目 | 内容 |
|---|---|
| 职责 | Trace、日志、事件、token/成本、调试、评测与质量反馈 |
| 推荐契约 | OpenTelemetry / OTLP |
| 推荐 Provider | Langfuse |
| 必要程度 | **P0：结构化事件与基础日志；P1：Trace 与成本；P2：系统化评测** |

Library 应传播 `traceId`、`runId`、`scope` 的脱敏标识、模型调用、工具调用和策略决定。以 OpenTelemetry 作为导出契约可以避免绑定某一家观测平台；Langfuse 可作为接收 OTLP 的 LLM 观测、成本追踪和评分 Provider。评测与实时执行分离：前者消费已脱敏的 trace/样本，不阻塞在线调用。

### 8. Artifact Runtime

| 项目 | 内容 |
|---|---|
| 职责 | 保存报告、文件、Sandbox 输出、长任务中间产物与可下载结果 |
| 候选实现 | 宿主对象存储、S3、MinIO |
| 必要程度 | **P2：Sandbox 或异步任务有文件产物时引入** |

Artifact Provider 只保存经授权且已扫描的产物与元数据；用引用传递给 Agent 和事件流，避免将大文件或敏感原文放进模型上下文、任务记录或日志。

## Provider 契约原则

第一阶段不必冻结所有 TypeScript 类型，但应先遵守以下规则：

1. **能力导向，不以厂商命名接口。** 例如 `ContextRuntime`、`WorkflowRuntime`，而非 `OpenVikingAdapter` 作为公共抽象。
2. **生命周期可控。** Provider 通过工厂创建；Library 管理一次 Run 的调用顺序，宿主负责连接池、部署与长期资源。
3. **状态与幂等显式化。** 每个跨进程调用携带 `runId`、`scope`、截止时间和可选幂等键；不承诺端到端“恰好一次”。
4. **安全默认最小化。** 工具、数据、凭据和网络权限均显式注入；Provider 不获得超出任务所需的宿主权限。
5. **退化路径明确。** Context、Workflow、Sandbox、评测 Provider 不可用时，Library 应能在配置允许时降级、重试或失败，而不是静默改变安全语义。
6. **事件统一。** Provider 内部事件映射到统一 `Event`；原始调试事件可作为可选扩展，不泄漏敏感数据。

## 推荐组合与阶段

| 阶段 | 目标 | 建议组合 | 不引入的复杂度 |
|---|---|---|---|
| P0：嵌入式 SDK | 单进程、在线交互、低风险业务工具 | Pi + Direct Tool + 宿主 `Authorize` + 结构化事件 | 工作流引擎、MCP Gateway、Sandbox、独立观测平台 |
| P1：增强上下文与可观测性 | 持久知识/记忆、跨服务追踪 | P0 + OpenViking（或宿主 RAG）+ OpenTelemetry + Langfuse + 可选 MCP Client | 持久化任务平台、集中策略控制面 |
| P2：可靠异步与受控执行 | 长任务、审批、高风险外部能力 | P1 + Temporal + Artifact Provider + Sandbox + MCP Gateway/Policy Engine | 多人工作区与完整组织级平台 |
| P3：平台层 | 多 Scope、协作、管理面、多 Harness | 按实际需求组合并部署控制面 | 不预设为当前 Library 的必经路径 |

## 典型数据流

### 在线问答

```text
宿主请求
  → Agent Library
  → ContextRuntime.recall(scope, query)             [可选]
  → Pi Agent Runtime
  → Authorize / Tool Runtime
  → Event / OpenTelemetry
  → 宿主流式响应
```

### 可恢复长任务

```text
宿主提交任务
  → Temporal Workflow
  → Activity：Agent Library + Pi Agent Runtime
  → Activity：ContextRuntime / ToolRuntime / ArtifactRuntime
  → Temporal 负责等待、重试、信号与恢复
  → 宿主查询结果或接收回调
```

## 暂不决定

- 不规定向量库、图数据库、队列、对象存储或 Sandbox 的具体产品。
- 不将 OpenViking、Temporal、Langfuse、E2B 变为核心库的必选依赖。
- 不将多 Agent DAG、协作空间或组织级管理后台提前并入 Library。
- 不以 Benchmark 宣称某个 Memory Provider “最佳”；应针对检索质量、时态正确性、成本、隐私与运维成本建立自己的评测。

## 参考资料

- [Pi Agent Core](https://github.com/earendil-works/pi/tree/main/packages/agent)
- [Pi AgentHarness 生命周期](https://github.com/earendil-works/pi/blob/main/packages/agent/docs/agent-harness.md)
- [OpenViking](https://github.com/volcengine/OpenViking)
- [Temporal TypeScript Workflows](https://docs.temporal.io/develop/typescript/workflows/basics)
- [E2B](https://github.com/e2b-dev/E2B)
- [OpenTelemetry](https://opentelemetry.io/)
- [Langfuse OpenTelemetry 集成](https://langfuse.com/integrations/native/opentelemetry)
