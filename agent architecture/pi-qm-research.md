---
title: Pi 与 QM 调研：自建可嵌入 Agent Library 的架构取舍
categories:
  - AI 编程
tags:
  - Agent
  - Pi
  - QM
  - 架构
date: "2026-08-10T23:32:00+08:00"
update: "2026-08-10T23:32:00+08:00"
---

# Pi 与 QM 调研：自建可嵌入 Agent Library 的架构取舍

> 本文记录为“自建并集成到其他应用的 Agent”进行的 Pi、QM 调研及架构取舍。当前长期方案见 [自建可嵌入 Agent Library 架构](./README.md)。

## 结论

- **Pi** 适合作为嵌入式 Agent Library 的 Runtime：它提供统一模型 API、Agent Loop、工具调用、状态管理、会话和事件流。
- **QM** 不是 Pi 的同类替代品，而是组织协作型 Agent 平台：它将 Pi、OpenCode、Codex 或 Claude Code 等 Harness 放在可替换适配器之后，并增加身份、策略、持久化 Sandbox、协作入口和部署能力。
- 第一阶段应该采用 **TypeScript + Node.js + Pi `agent-core` + 自己的薄封装**，而不是直接部署或复刻 QM。

## Pi

### 定位与包结构

Pi 是 Agent Harness 项目，主要由以下包组成：

| 包 | 职责 |
|----|------|
| `@earendil-works/pi-ai` | 多 Provider LLM API |
| `@earendil-works/pi-agent-core` | 带工具调用和状态管理的 Agent Runtime |
| `@earendil-works/pi-coding-agent` | 交互式 Coding Agent CLI，并包含嵌入式 SDK |
| `@earendil-works/pi-telemetry` | 与厂商无关的 Telemetry 契约与参考实现 |

`pi-agent-core` 提供状态化 Agent、上下文变换、工具循环、流式事件、工具执行模式和调用前后 Hook。它支持直接注入工具、在调用前阻断工具，并由调用者决定会话和业务状态如何保存。

### 嵌入方式

Pi 提供三种对应用集成有价值的方式：

1. **`pi-agent-core`**：低层 Runtime。适用于希望完全控制 Prompt、工具、会话和业务状态的 Library。
2. **`pi-coding-agent` SDK**：适用于还要复用 Pi 的 Session、上下文压缩、Skills、扩展和资源加载能力的 Node.js 应用。
3. **RPC mode**：适用于非 Node.js 调用方或希望把 Agent 进程隔离的场景。

对于自建嵌入式 Library，优先用 `pi-agent-core`；不要在生产服务中以 CLI 终端输出作为主集成协议。

### 安全边界

Pi 不包含用于限制文件、进程、网络或凭据访问的内建 Sandbox；进程默认继承启动用户的权限。项目信任只控制项目资源是否加载，不构成执行隔离。

因此：

- 不将高权限原始工具默认放入 Agent；
- 在宿主的工具实现或授权回调中执行权限、参数和业务校验；
- 无人值守、高风险或不可信内容驱动的任务，由宿主部署到容器、VM 或其他隔离环境。

## QM

### 定位

QM 是面向组织协作的 Multiplayer Agent Harness。它提供 Slack、Web、管理入口和 Headless Core，并可在 Pi、OpenCode、Codex、Claude Code 等 Harness 间切换。

QM 的核心抽象是 **Scope**：个人、频道、群组或项目都可拥有作用域化的记忆、文件、密钥视图、权限、定时任务、Web App 与持久化 Sandbox。这个设计使独立工作与协作可以并存。

### 架构经验

QM 的平台架构可概括为：

```text
Slack / Web / Admin / API
          │
Headless Core
身份、策略、调度、审计、队列
          │
Harness Adapter（Pi / OpenCode / Codex / Claude Code）
          │
Per-Scope Sandbox
          │
Postgres：会话、记忆、队列和持久状态
```

其中值得保留的设计原则是：

1. **Harness 可替换**：业务层不绑定 Pi、模型厂商或某一个 CLI。
2. **工具访问经过统一策略层**：工具调用应可审批、拒绝、审计，而不是仅依赖 Prompt。
3. **持久状态外置**：会话、记忆、任务、审计与产物不能只存在上下文窗口。
4. **执行环境应隔离**：长任务和高风险操作需要明确的 Sandbox 边界。
5. **渠道是外围适配器**：Slack、Web、Admin 不应成为 Agent Core 的前提。

### QM 的策略模型

QM 提供 Strict、Auto、Dangerous 三种组织级安全姿态：Strict 中每个 Harness 工具调用都需人工审批；Auto 对标注来源的外部内容和工具结果做筛查；Dangerous 不做筛查或停顿。无论模式如何，破坏性命令的预声明硬拒绝策略仍然生效。

这说明“策略层独立于 Prompt”是可靠的架构方向，但第一阶段 SDK 只需实现 `Authorize` Hook；完整策略引擎应在真实组织需求出现后再建设。

## Pi 与 QM 的关系

| 维度 | Pi | QM |
|------|----|----|
| 核心定位 | 可嵌入 Harness / Agent Runtime | 组织级协作 Agent 平台 |
| 主集成方式 | npm SDK、Runtime、RPC | 部署实例、HTTP API、Slack/Web 插件 |
| 关注点 | 模型、Agent Loop、工具、会话、扩展 | 身份、Scope、策略、Sandbox、协作、运维 |
| 适合第一阶段嵌入式库 | 是 | 否，过重 |
| 与另一方关系 | 可作为 QM 的底层 Harness | 可参考其平台化边界设计 |

## 为什么不直接使用或复刻 QM

当前目标是将 Agent 集成到其他应用，因此由宿主已有的用户、鉴权、数据、UI 与任务系统承担平台职责更合适。直接采用 QM 会过早引入 PostgreSQL、队列、Sandbox、Slack/Web 管理面、多 Scope 和部署体系。

此外，QM 当前版本为 `0.1.0`，仓库较新，并使用了 QM 定制发行的 `pi-coding-agent` 包。若未来采用，应在生产前验证其升级、补丁和安全维护策略。

## 可延后引入的外围架构

当嵌入式 SDK 的需求增长时，可在其上增加以下能力：

| 能力 | 触发条件 | 建议位置 |
|------|----------|----------|
| HTTP/SSE Adapter | 多个 Web 或后端应用接入 | Library 外围 Adapter |
| RPC Adapter | 非 Node.js 宿主或进程隔离 | Library 外围 Adapter |
| 异步 Worker / Scheduler | 长任务、定时任务、失败重试 | 宿主基础设施或平台层 |
| Scope 工作区 | 多用户或多人协作 | 平台层 |
| 持久化 Sandbox | 代码执行、外部工具和高风险动作 | 平台层 / 基础设施 |
| 组织级 Policy Engine | 多租户、合规、管理员控制 | 平台层 |
| 多 Harness 路由 | 不同任务需要不同 Agent Runtime | Runtime Adapter 层 |

## 与 Harness Engineering 的对应关系

Pi 提供 Agent Loop 和工具 Hook；宿主负责把这些 Hook 与上下文、状态、权限、评测和恢复机制组合起来。整体上，Library 不能只依赖 Prompt，而要为工具、状态和失败路径建立明确边界。

这与 Harness Engineering 的原则一致：上下文按需提供，状态外化，工具保持最小集合，使用独立校验与硬约束处理失败。

## 外部来源

- [Pi GitHub 仓库](https://github.com/earendil-works/pi)
- [Pi Agent Core README](https://raw.githubusercontent.com/earendil-works/pi/main/packages/agent/README.md)
- [Pi SDK 文档](https://pi.dev/docs/latest/sdk)
- [Pi Extensions 文档](https://pi.dev/docs/latest/extensions)
- [Pi Security 文档](https://pi.dev/docs/latest/security)
- [QM GitHub 仓库](https://github.com/yc-software/qm)
- [QM package.json](https://raw.githubusercontent.com/yc-software/qm/main/package.json)
- [QM GitHub Repository API](https://api.github.com/repos/yc-software/qm)
- [Harness Engineering](../ai%20coding/harness-engineering/README.md)
- [Harness Engineering 详解](../ai%20coding/harness-engineering/xiaolin-coding-harness-engineering.md)
