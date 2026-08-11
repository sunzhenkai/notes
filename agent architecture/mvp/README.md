# Agent 项目 MVP 总览

## 需求拆分

项目包含两个不同但相关的产品层：

1. **通用 Agent Library**：向 Web、IM、桌面端、后端服务或工作流等宿主提供可复用的 Agent 能力；
2. **独立 Agent Application**：提供必选 UI、应用 API 和长任务管理，任务执行 Agent Slice 时复用通用 Agent Library。

**决策：Agent Application 依赖 Agent Library，Agent Library 不依赖 Agent Application。** Library 不感知 UI、Task、Worker、数据库或部署模型，Application 不得复制 Agent Loop。

长任务不是一个永久运行的 `Agent.run()`。它由一个或多个有界 Agent Run、等待、重试和恢复阶段组成；只有 Agent Run 阶段调用 Library。

## 设计阶段约束

当前设计只冻结产品语义、模块边界和适配契约，不绑定具体语言、Web 框架、数据库或 Harness 实现。

实现阶段仍需选择一种原生语言：同语言宿主可进程内调用 Library，不同语言宿主需要通过 HTTP/RPC Binding 调用。两种 Binding 必须遵循同一 Agent 能力契约。

```text
Agent Capability Contract
├── Local Library Binding
└── Remote HTTP/RPC Binding
```

## 方案比较

| 方案 | 做法 | 成本 | 主要风险 | 可逆性 | 结论 |
|------|------|------|----------|--------|------|
| A. 契约优先、实现后选 | 先冻结语言无关语义，再选择原生语言和 Binding | 中 | 实现前仍需一次技术决策 | 高 | **推荐** |
| B. 先固定语言和框架 | 直接以某个生态设计公共接口 | 低 | 公共边界被框架类型污染 | 中 | 当前不采用 |
| C. 首版即多语言 | 同时实现多个 SDK 和远程 Runtime | 高 | 协议和运维成本掩盖 MVP 目标 | 中 | 延后 |

**推荐方案 A**：先验证 Agent 和 Task 两个产品抽象，再根据首批宿主选择原生语言。跨语言能力只在真实需求出现后增加。

## 目标架构

```text
┌───────────────────────────────────────────┐
│ MVP 2: Agent Application                  │
│                                           │
│  Browser UI                               │
│      │                                    │
│      ▼                                    │
│  Application API                          │
│      │                                    │
│      ▼                                    │
│  Task Service ───────> Durable Task Store │
│      │                       │             │
│      ▼                       │             │
│  Task Worker <───────────────┘             │
│      │ AgentClient                         │
└──────┼─────────────────────────────────────┘
       │ local package or remote protocol
       ▼
┌───────────────────────────────────────────┐
│ MVP 1: Agent Library                      │
│                                           │
│ Agent / Context / Skills / Tools / Session │
│ Events / Budget / Cancellation             │
│                   │                       │
│                   ▼                       │
│              Harness Port                 │
└───────────────────┬───────────────────────┘
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
      Pi Adapter  Future A  Future B
```

禁止的依赖：

```text
Agent Library -X-> Task / UI / Worker / 数据库 / Web 框架
Agent Application -X-> Pi 或其他 Harness 专有 API
UI -X-> Agent Library 或 Harness
模型输入 -X-> 执行环境、凭据或权限升级配置
```

## MVP 边界

| 维度 | MVP 1：Agent Library | MVP 2：Agent Application |
|------|----------------------|--------------------------|
| 产品目标 | 完成一次有界 Agent Run | 管理一个可恢复的长任务 |
| 产品形态 | 原生 Library，按需增加远程 Binding | UI + API + Task Service + Worker |
| Agent Loop | 负责 | 只调用，不实现 |
| Harness | 定义 Port，首版选一个 Adapter | 不感知具体 Harness |
| Skill/Tool/Context | 定义契约并执行 | 提供资产、配置和权限 |
| Session/Checkpoint | 定义语义 | 持久化并管理生命周期 |
| Event | 产生 AgentEvent | 持久化、关联并投影 Task Timeline |
| Retry | 有界操作重试 | Task 级持久重试和恢复 |
| 状态 | 当前 Run 和外部引用 | Task、Attempt、Lease、Event、Artifact |
| UI | 不负责 | **必选** |
| Task Runtime | 不负责 | 数据库 + Worker Lease + Heartbeat + Recovery |
| Temporal | 不依赖 | 首版不使用，复杂度触发后再评估 |

## 跨 MVP 最小契约

只冻结语义，不冻结具体编程语言或厂商类型：

- `AgentDefinitionRef`：Agent 定义的稳定标识与版本；
- `AgentRunSpec`：`run_id`、输入、Skill/Tool 引用、Scope、Session/Checkpoint 引用和运行预算；
- `AgentRunOutcome`：完成、暂停、失败或取消，以及 output/session/checkpoint/artifact 引用；
- `AgentEvent`：带 schema version、sequence 和 run_id 的运行事件；
- `AgentError`：区分可重试、不可重试、取消、预算耗尽和副作用状态不确定；
- `HarnessPort`：执行、取消和能力声明；
- `AgentClient`：Application 调用 Agent 能力的内部端口，可绑定本地 Library 或远程协议；
- checkpoint 和 artifact 使用 opaque ref，持久化、保留期和访问控制由 Application 或宿主负责。

## 交付与验证顺序

```text
冻结语言无关 Agent 契约
    ↓
选择一种原生语言和首个 Harness Adapter
    ↓
用普通宿主验证有界 Agent Run
    ↓
Agent Application 通过 AgentClient 集成同一能力
    ↓
用 UI 完成长任务创建、查看、取消、重试和恢复闭环
    ↓
再根据证据决定跨语言、Temporal、Sandbox 和复杂 Workflow
```

## 总体验收标准

- 普通宿主无需部署 Agent Application 即可使用 Agent Library；
- Agent Application 不直接依赖 Pi 或其他 Harness 专有 API；
- UI 支持任务创建、列表、详情、事件时间线、取消、重试、恢复和结果查看；
- Task Worker 通过 `AgentClient` 调用 Library，不存在第二套 Agent Loop；
- Task、Attempt、Agent Run 和 Checkpoint 可以独立关联；
- Worker 重启或 Lease 过期后，未完成 Task 可从 checkpoint 恢复或进入明确失败状态；
- Library 不依赖 Task、数据库、Web 框架或具体存储实现；
- 第一版不要求 Temporal、定时调度、复杂 Workflow 或多语言 SDK；
- 所有副作用写调用具备稳定幂等键或明确的人工处置路径。

## 文档

- [MVP 1：通用 Agent Library](./agent-library-mvp.md)
- [MVP 2：独立长任务 Agent Application](./long-running-agent-app-mvp.md)
- [开放问题与决策门](./open-questions.md)
- [Agent Library 架构入口](../README.md)
- [通用 Agent Service 与可执行任务模块架构](../agent-service-task-module-architecture.md)
- [可插拔外围 Runtime 架构](../runtime-architecture.md)
