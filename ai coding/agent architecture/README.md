# 自建可嵌入 Agent Library 架构

> 本文记录面向“集成到其他应用”的自建 Agent 库方案。它是持续迭代的设计入口；Pi 与 QM 的调研、选型理由和可延后引入的平台能力见 [Pi 与 QM 调研](./pi-qm-research.md)。

## 目标与边界

目标是提供一个可被 Web、IM、桌面端、后端服务或工作流调用的 Agent **库**，而不是在第一阶段构建完整的组织级 Agent 平台。

第一阶段：

- 以 SDK 方式嵌入宿主应用；
- 接收宿主提供的身份、会话上下文、模型配置和业务工具；
- 提供 Agent Loop、上下文组装、工具调度、流式事件和统一错误处理；
- 支持少量显式注入、可校验的业务工具。

第一阶段不负责：

- 用户、租户、RBAC、管理后台；
- 数据库、队列、任务调度和观测平台；
- 多人独立工作区、持久化沙箱、组织级模型路由；
- 将 Shell、数据库或内部 HTTP 等原始权限默认暴露给模型。

这些能力由宿主提供，或在后续作为可选的平台层增加。

## 已确定的技术选择

| 层次 | 选择 | 说明 |
|------|------|------|
| 语言与运行时 | TypeScript + Node.js | 直接复用 Pi 的 TypeScript/Node Runtime |
| Agent Runtime | `@earendil-works/pi-agent-core` | 提供状态化 Agent、工具调用、流式事件和工具 Hook |
| 工具参数 Schema | TypeBox | 与 Pi 的工具定义保持一致 |
| 发布形态 | npm package | 作为宿主应用的依赖，不要求单独部署服务 |
| HTTP 接入 | 可选 Fastify Adapter | 仅为示例服务或 BFF 提供，不成为核心库依赖 |
| 跨语言接入 | 可选 HTTP / Pi RPC Adapter | 不为每种语言重写 Agent Runtime |

不在核心库中引入 Web 框架或额外的 Agent 编排框架。Pi 已覆盖模型接入、Agent Loop、工具调用、状态和流式事件；外围框架应由宿主按需组合。

## 简化架构

```text
宿主应用
用户 / 鉴权 / 数据库 / UI / IM / 队列
        │
        ▼
Agent Library
Agent.run(input, scope, tools)
 ├─ Context Builder
 ├─ Pi Runtime Adapter
 ├─ Tool Registry
 ├─ 可选 Memory Adapter
 ├─ 可选 Authorize Hook
 └─ Event Stream
        │
        ▼
LLM + 宿主注入的业务工具
```

`scope` 是调用上下文的载体，例如 `userId`、`tenantId`、`conversationId` 与业务对象标识。核心库只透传它给 Memory、工具和授权回调，不在库内实现独立工作区或权限体系。

## 最小公共抽象

```ts
const agent = createAgent({
  model,
  tools: [searchKnowledge, queryOrder, createTicket],
  memory,       // 可选，由宿主实现
  authorize,    // 可选，在工具调用前执行
  onEvent,      // 可选，用于流式 UI、审计和日志
});

await agent.run({
  input: "查一下订单状态",
  scope: { userId, tenantId, conversationId },
});
```

| 抽象 | 职责 |
|------|------|
| `Agent` | 编排一次运行，维护模型交互、上下文和工具循环 |
| `Tool` | 定义名称、参数 Schema、执行器和可选元数据；由宿主实现真实业务访问 |
| `Memory` | 可选的读取、写入和检索接口；具体存储由宿主决定 |
| `Authorize` | 工具调用前的同步授权 / 审批 / 白名单校验 Hook |
| `Event` | 对文本增量、工具进度、结果、错误的统一事件表达 |
| `Scope` | 宿主定义的调用上下文，传递隔离与审计所需标识 |

## 职责边界

| Agent Library 负责 | 宿主应用负责 |
|-------------------|--------------|
| 模型调用和 Agent Loop | 身份认证、租户隔离和业务授权 |
| Prompt / Context 组装 | 业务数据、数据库和知识库实现 |
| 工具注册与调度 | 工具的业务语义、凭据和网络访问 |
| 工具调用前的 Hook | 持久化、队列、日志与指标基础设施 |
| 流式事件和错误归一化 | UI、IM 渠道、后台任务和部署 |

工具必须显式注入；Library 不为模型内置高权限的 Shell、数据库或内部服务访问。宿主可在 `Authorize` 中根据 `scope`、工具名与参数执行自己的策略。

## 演进路线

### 阶段 1：嵌入式 SDK

- 单进程 TypeScript/Node 集成；
- Pi `agent-core` 作为默认 Runtime；
- 少量低风险、业务明确的工具；
- 宿主保存会话与记忆；
- 以 `onEvent` 对接流式 UI、日志和审计。

### 阶段 2：外围适配器

- 增加 Fastify HTTP/SSE Adapter；
- 增加 RPC / 跨语言 Adapter；
- 增加可选 Memory Provider、Trace Provider 与 Background Job Provider；
- 保持核心 API 与具体基础设施解耦。

### 阶段 3：可选平台层

仅在需求确认后增加多 Scope、共享 Skills、异步任务、Sandbox、组织级策略与多 Harness 路由。此层应建立在 Library 之上，不反向侵入核心 SDK。

## 待验证问题

- 宿主应用的主要形态：单体 Web、IM Bot、后端服务还是桌面应用？
- Memory 的一致性、保留期和隐私边界由哪个宿主系统负责？
- 哪些工具有写操作，是否需要宿主实现人工审批？
- 是否需要跨语言调用；若需要，HTTP 与 RPC 的首选接入方式是什么？
- 何时出现多人协作、长任务或隔离执行环境的真实需求？

## 相关内容

- [通用 Agent Service 与可执行任务模块架构](./agent-service-task-module-architecture.md)
- [可插拔外围 Runtime 架构](./runtime-architecture.md)
- [Pi 与 QM 调研：自建可嵌入 Agent Library 的架构取舍](./pi-qm-research.md)
- [Harness Engineering](../harness-engineering/README.md)
- [AI Coding Agents 概览](../agents/README.md)
