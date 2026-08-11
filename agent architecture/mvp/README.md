# Agent 项目 MVP 总览

## 需求拆分

项目面向两个不同但相关的产品需求：

1. **通用 Agent Library**：作为 TypeScript/Node.js package，被 Web、IM、桌面端、后端服务或工作流等宿主直接集成。
2. **独立 Agent 应用**：作为可部署服务接收和管理长任务；任务在需要模型推理、上下文组装或工具调用时，复用通用 Agent Library。

**决策：需求 2 依赖需求 1。** 依赖方向必须保持单向：独立应用可以组合 Library，Library 不得依赖独立应用的 HTTP、Temporal、数据库、任务状态或部署模型。

这里的“依赖”不表示长任务的每个阶段都必须执行 Agent。长任务可以处于等待、Signal、重试或人工审批阶段；只有执行 Agent Slice 时才调用 Library。

## 方案比较

| 方案 | 做法 | 成本 | 主要风险 | 可逆性 | 结论 |
|------|------|------|----------|--------|------|
| A. 共享 Library 契约优先 | 先冻结通用运行契约；独立应用的 API 和 Worker 都依赖同一 package | 中 | 需提前约束公共接口 | 高 | **推荐** |
| B. Service 优先、Library 后抽取 | 先完成长任务服务，再从服务内部提取 SDK | 前期低、后期高 | Service/Temporal 概念容易泄漏到核心 | 中 | 不推荐作为 MVP |
| C. 两套独立实现 | Library 与独立应用分别实现 Agent Loop | 前期并行、长期最高 | 行为漂移、重复修复、难以复用 | 低 | 拒绝 |

**推荐方案 A**，因为它直接验证两个需求的共同核心，并让长任务可靠性与 Agent 推理能力独立演进。接受的取舍是：MVP 1 必须先定义少量稳定契约，MVP 2 才能基于这些契约实现。

## 目标架构

```text
其他宿主应用
    │ package dependency
    ▼
┌────────────────────────────────────┐
│ MVP 1: 通用 Agent Library          │
│ AgentRunner / Context / Tool /     │
│ Policy Hook / Event / Provider     │
└────────────────────────────────────┘
                 ▲
                 │ package dependency
       ┌─────────┴─────────┐
       │                   │
┌──────┴────────┐   ┌──────┴─────────────┐
│ Agent Service │   │ Long-task Worker    │
│ HTTP / SSE    │   │ Agent Slice Activity│
└──────┬────────┘   └────────┬────────────┘
       │                     │
       └──────┬──────────────┘
              ▼
┌────────────────────────────────────┐
│ MVP 2: 独立 Agent 应用             │
│ Task API / Temporal Workflow /     │
│ State / Artifact / Operations      │
└────────────────────────────────────┘
```

禁止的反向依赖：

```text
Agent Library -X-> HTTP 框架 / Temporal / 数据库 / Artifact 实现
Temporal Workflow -X-> LLM / Agent Loop / Tool / 网络或文件 I/O
模型输入 -X-> Namespace / Task Queue / ExecutionTarget / 凭据
```

## MVP 边界

| 维度 | MVP 1：通用 Agent Library | MVP 2：独立 Agent 应用 |
|------|----------------------------|-------------------------|
| 产品形态 | npm package | 独立部署的 Service + Worker |
| 核心目标 | 完成一次有界 Agent Run | 可靠推进跨时间的 AgentTask |
| 状态范围 | 当前 Run 与宿主注入的引用 | Task、Workflow、checkpoint、artifact |
| 接口 | TypeScript API、Provider、Event | HTTP/SSE、Task API、Signal、Cancel |
| 可靠性 | deadline、取消、预算、错误归一化 | 重试、恢复、幂等、Continue-As-New |
| 基础设施 | 无强制基础设施 | Temporal、状态存储、Artifact Store |
| Sandbox | 仅预留 Execution Provider | 按首个任务风险决定是否实现 |
| 用户与 RBAC | 不负责 | MVP 仅接入上游身份，不建设管理平台 |

## 跨 MVP 最小契约

MVP 1 与 MVP 2 只冻结以下稳定语义，不提前冻结具体 URL、数据库或厂商类型：

- `AgentDefinitionRef`：`definitionId + version`，Task 创建后固定版本；
- `AgentRunRequest`：运行标识、Definition、输入或引用、最小化 Scope、checkpoint 引用、deadline、取消信号和预算；
- `AgentRunResult`：完成、暂停或失败状态，以及 result/checkpoint/artifact 引用；
- `AgentEvent`：带 schema version 的文本、工具、进度、结果和错误事件；
- `AgentError`：区分可重试、不可重试、取消、预算耗尽和副作用状态不确定；
- Provider 调用上下文：`runId`、最小 Scope、deadline，以及副作用调用的 `idempotencyKey`；
- checkpoint 与 artifact 对 Library 是 opaque ref，持久化、保留期和访问控制由应用侧 Provider 负责。

## 交付与验证顺序

```text
冻结 MVP 1 契约
    ↓
用普通宿主验证嵌入式运行
    ↓
MVP 2 Service/Worker 集成同一 Library
    ↓
用一个真实长任务验证恢复、Signal、取消和幂等
    ↓
再决定 Schedule、Sandbox、多环境与跨语言接入
```

这一顺序不是要求两个产品串行发布；MVP 2 的服务骨架可以并行设计，但其 Agent 执行路径必须等待 MVP 1 的公共契约稳定。

## 总体验收标准

- 一个普通 Node.js 宿主可直接集成 MVP 1，不需要部署 MVP 2；
- MVP 2 的 Service 在线运行和 Task Worker 均调用 MVP 1，不存在第二套 Agent Loop；
- 停用 Task Module 后，MVP 1 及独立应用的在线运行能力不受影响；
- Library package 不传递依赖 Temporal、Web 框架或具体存储 SDK；
- 长任务能跨 Worker 重启继续推进，并支持查询、Signal 和取消；
- 所有副作用写调用都具备稳定幂等键或明确的人工处置路径；
- 模型不能选择或提升 ExecutionTarget、Task Queue、Sandbox Profile 或凭据权限。

## 文档

- [MVP 1：通用 Agent Library](./agent-library-mvp.md)
- [MVP 2：独立长任务 Agent 应用](./long-running-agent-app-mvp.md)
- [开放问题与决策门](./open-questions.md)
- [Agent Library 架构入口](../README.md)
- [通用 Agent Service 与可执行任务模块架构](../agent-service-task-module-architecture.md)
- [可插拔外围 Runtime 架构](../runtime-architecture.md)
