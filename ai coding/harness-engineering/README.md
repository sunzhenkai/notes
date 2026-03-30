# Harness Engineering — 缰绳工程

> 围绕 AI Agent 构建约束、反馈和质量保障的系统工程实践。
> 来源：[花叔《Harness Engineering又他妈是啥？》](https://mp.weixin.qq.com/s/mRxWLuqlLsleUmwW78_Qxg)
> 最后更新：2026年3月

## 概述

Harness（缰绳/马具）指的是套在 AI 身上让它能被引导的那整套东西——没有它，AI 就是乱跑的野马，能力再强也白搭。Harness Engineering 是围绕 AI Agent 设计这套系统的工程实践。

## 三层递进关系

| 层次 | 类比 | 管什么 |
|------|------|--------|
| **Prompt Engineering** | 你对马说的话（向左转、跑快点） | 你问什么 |
| **Context Engineering** | 帮马看路的一切（地图、路标、地形） | 你给模型看什么 |
| **Harness Engineering** | 缰绳、马鞍、围栏和道路本身 | 整个系统怎么运转 |

Context 是 Harness 的一部分，Harness 还多管了**约束、反馈和质量检查**。

## 核心证据

### LangChain 案例

- Terminal Bench 2.0：成绩从 52.8% → 66.5%，排名 Top 30 → Top 5
- **模型完全没换**，只改了：系统提示词、工具配置、中间件钩子
- 结论：**模型可能已经不是瓶颈，瓶颈是你给它搭的环境**

### OpenAI Codex 实验

- 3→7 个工程师，5 个月，100 万行代码 beta 产品，零行手写
- ~1500 个 PR，每人每天 3.5 个 PR，速度约传统 10 倍
- 隐忧：速度快 ≠ 质量好，长期维护成本未知

## Martin Fowler 的三块拆解

### 1. 上下文工程（Context Engineering）

- 给模型一张地图，不是 1000 页的说明书
- 维护持续更新的代码库知识库 + agent 能实时看到的系统状态
- **上下文是稀缺资源，塞太多反而挤占干活的空间**

### 2. 架构约束（Architectural Constraints）

- 不光靠 AI 自检，还有 linter、结构测试在旁边盯着
- 硬规则，不遵守就编译不过

### 3. 垃圾回收（Garbage Collection）

- 专门一个 agent 周期性运行，只干一件事：找文档矛盾和架构违规
- 一个**专职找茬的 AI**

## Anthropic 的三 Agent 架构

| 角色 | 职责 |
|------|------|
| **Planner（规划者）** | 把简单指令扩展成详细的产品规格 |
| **Generator（生成者）** | 按迭代一次做一个功能 |
| **Evaluator（评估者）** | 跑端到端测试，持续挑刺 |

灵感来自**生成对抗网络（GAN）**：训练一个专门的评估者让它一直挑刺，比让生成者自己检查自己管用得多。

额外发现：Claude Sonnet 4.5 有**上下文焦虑**——上下文太多表现反而变差，必须定期清空重来。**Harness 不是越大越好。**

## 实践要素

### 配置文件（活的规则）

- CLAUDE.md / .cursorrules / CONVENTIONS.md 都是 harness 的一部分
- **每次 agent 犯错，就工程化一个方案，让它再也犯不了同样的错**（Mitchell Hashimoto 方法）
- 文件是活的，一直在长

### Hooks（物理拦截）

- 在 agent 关键操作前后注入脚本
- 编辑文件前自动跑 linting，生成代码后自动做类型检查
- **这不是 prompt 里写的"请注意规范"，是物理上拦住它**

### Skills（按需加载）

- 每个 skill 是独立能力包，平时不占 context，需要时才调

### 让 AI 查 AI

- 写完后开新对话，把结果贴进去："找出所有问题"
- 第二个 AI 能发现第一个漏掉的很多问题

## 三条起步建议

1. **给地图不给说明书** — CLAUDE.md 应该像地图（项目结构、文件关系、关键约束），不要把每步写死
2. **每次犯错加一条规则** — 空文件开始，三个月后就是你的 harness，高度定制
3. **让 AI 查 AI** — 别让 AI 自己查自己，用独立的评估者

## Martin Fowler 的警告

> 如果太早把人类从「in the loop」移到「on the loop」，将来可能没人真正懂得怎么回事，也就没人能设计好的 harness。

现在能设计好 harness 的人，都是有丰富经验的老手。问题在于：**不管积累的是什么经验，足够多的经验本身就是设计 harness 的前提。没有捷径，换了个赛道而已。**

## 与历史工程实践的联系

- **航天工程** — 60 年前 NASA 就在做类似的事：约束、反馈循环、冗余检查、异常处理
- **工业控制** — PLC 编程里的安全联锁机制就是一种 harness
- AI 圈不是发明了 harness engineering，是终于意识到自己需要学几十年前就有的工程纪律

## 与其他概念的关系

- [OpenSpec](../openspec) — 规范驱动开发，是 harness 中"约束"层面的具体实践
- [CLAUDE.md](../agents/claude) — Claude Code 的项目配置文件，是 harness 的核心载体之一
- [.cursorrules](../agents/cursor) — Cursor 的项目配置文件
