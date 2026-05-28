# Superpowers — AI Agent 技能框架 & 软件开发方法论

> 为 AI 编程 Agent 注入完整的软件开发方法论，通过可组合的 Skill 自动驱动。
> 最后更新：2026年5月

## 简介

**Superpowers** 是一个 AI Agent 技能框架（Skills Framework），它不是编辑器，不是工具集，而是一套**完整的软件开发方法论**。它通过一系列可组合的 Skill，让你的 AI 编程 Agent 在正确的时机自动执行正确的工作流——从头脑风暴、设计、规划到实现、测试、审查和发布。

**一句话定位：** 不是给你更多功能，而是让 Agent 拥有"什么时候该做什么"的判断力。

- **作者**：Jesse Vincent（Prime Radiant）
- **GitHub**：[obra/superpowers](https://github.com/obra/superpowers)
- **许可**：MIT
- **版本**：v5.1.0
- **支持 Agent**：Claude Code、OpenCode、Cursor、Codex CLI、Codex App、Gemini CLI、Factory Droid、GitHub Copilot CLI

---

## 核心理念

| 原则 | 含义 |
|------|------|
| **Test-Driven Development** | 先写测试，永远如此 |
| **Systematic over Ad-hoc** | 流程优于猜测 |
| **Complexity reduction** | 简单是首要目标 |
| **Evidence over claims** | 验证后再声明成功 |

---

## 核心工作流

Superpowers 的核心是一条完整的开发流水线，每个环节自动触发：

```
Brainstorm → Worktree → Plan → Implement → Review → Finish
```

### 1. Brainstorming（头脑风暴）

**触发时机**：Agent 检测到你要构建新东西时自动激活。

- 不会直接跳进去写代码，而是退后一步问你"你到底想做什么"
- 一次一个问题，逐步提炼出完整设计
- 将设计分成小段呈现，让你逐段审阅
- 设计批准后保存设计文档

### 2. Using Git Worktrees（工作区隔离）

**触发时机**：设计批准后自动激活。

- 创建隔离的工作区（新分支上的 git worktree）
- 运行项目设置
- 验证测试基线干净

### 3. Writing Plans（编写计划）

**触发时机**：设计批准后自动激活。

- 把工作拆解成 2-5 分钟的小任务
- 每个任务有精确的文件路径、完整代码、验证步骤
- 计划足够清晰，让一个热情但缺乏判断力的初级工程师也能执行

### 4. Subagent-Driven Development（子 Agent 驱动开发）

**触发时机**：计划就绪后自动激活。

- 每个任务分配一个全新的子 Agent
- 两阶段审查：先检查规范合规性，再检查代码质量
- Claude 可以自主工作数小时不偏离计划

### 5. Test-Driven Development（测试驱动开发）

**触发时机**：实现阶段自动激活。

- 强制 RED-GREEN-REFACTOR 循环
- 先写失败测试 → 看它失败 → 写最小代码 → 看它通过 → 提交
- **删除先于测试写的代码**

### 6. Code Review（代码审查）

**触发时机**：任务间自动激活。

- 对照计划审查
- 按严重程度报告问题
- 关键问题阻止继续推进

### 7. Finishing a Development Branch（完成开发分支）

**触发时机**：所有任务完成后自动激活。

- 验证测试通过
- 呈现选项（merge / PR / keep / discard）
- 清理 worktree

---

## 技能清单（14 个）

### 测试

| 技能 | 说明 |
|------|------|
| `test-driven-development` | RED-GREEN-REFACTOR 循环，含测试反模式参考 |

### 调试

| 技能 | 说明 |
|------|------|
| `systematic-debugging` | 4 阶段根因分析（含根因追踪、纵深防御、条件等待技术） |
| `verification-before-completion` | 确保真正修复了问题 |

### 协作

| 技能 | 说明 |
|------|------|
| `brainstorming` | 苏格拉底式设计提炼 |
| `writing-plans` | 详细实现计划 |
| `executing-plans` | 带检查点的批量执行 |
| `dispatching-parallel-agents` | 并发子 Agent 工作流 |
| `subagent-driven-development` | 快速迭代 + 两阶段审查 |
| `requesting-code-review` | 审查前检查清单 |
| `receiving-code-review` | 响应审查反馈 |
| `using-git-worktrees` | 并行开发分支 |
| `finishing-a-development-branch` | Merge / PR 决策工作流 |

### 元技能

| 技能 | 说明 |
|------|------|
| `writing-skills` | 创建新 Skill 的最佳实践（含测试方法论） |
| `using-superpowers` | 技能系统入门 |

---

## 自动触发机制

**Superpowers 不是"你需要时手动调用"的工具集，而是"Agent 在正确时机自动使用"的方法论。**

关键设计：
1. **Skill 优先于直接回答**：当用户请求匹配某个 Skill 时，Agent 必须调用该 Skill，而不是自己回答
2. **红牌检查**：一系列"如果出现这些想法，立即停止"的规则，防止 Agent 绕过工作流
3. **强制流程**：不是建议，而是必须遵守的工作流
4. **人类伙伴**：始终称呼用户为"human partner"，强调 Agent 是辅助者而非替代者

---

## 安装概览

不同 Agent 安装方式不同，详见各平台教程：

| Agent | 安装方式 | 详细教程 |
|-------|---------|---------|
| **Claude Code** | Plugin Marketplace | [Claude Code 教程](./claude-code-guide.md) |
| **OpenCode** | opencode.json plugin | [OpenCode 教程](./opencode-guide.md) |
| **Cursor** | Plugin Marketplace | [Cursor 教程](./cursor-guide.md) |
| **Codex CLI** | Plugin Marketplace | — |
| **Codex App** | Plugin Marketplace | — |
| **Gemini CLI** | Extension | — |
| **Factory Droid** | Marketplace | — |
| **GitHub Copilot CLI** | Marketplace | — |

---

## 与同类工具对比

| 特性 | Superpowers | gstack | OpenSpec |
|------|-------------|--------|----------|
| 定位 | Agent 方法论框架 | AI 软件工厂 | 规范驱动开发 |
| 核心单位 | Skill 工作流 | Sprint 流程 | Change 生命周期 |
| 自动触发 | 是（会话启动时注入） | 是（斜杠命令 + 路由规则） | 否（需手动命令） |
| TDD 强制 | 是（RED-GREEN-REFACTOR） | 否 | 否 |
| 子 Agent | 是（两阶段审查） | 否 | 否 |
| 浏览器测试 | 否 | 是（真实 Chromium） | 否 |
| 支持 Agent | 8+ | 10+ | 20+ |
| 配置文件 | CLAUDE.md / opencode.json | CLAUDE.md 块 | openspec/ 目录 |
| 设计哲学 | 流程驱动（强制） | 角色驱动（专家团队） | 规范驱动（先共识后编码） |

---

## 适用场景

- **追求工程质量的开发者**——TDD 强制、系统化调试、证据驱动
- **多 Agent 并行开发**——subagent-driven-development + git worktrees
- **跨 Agent 使用**——一次学习，8+ Agent 通用
- **团队协作**——审查流程标准化、分支管理自动化
- **AI Agent 新手**——自动化工作流比手动 prompt 更可靠

---

## 文档目录

- **[OpenCode 使用教程](./opencode-guide.md)** — 在 OpenCode 中安装和使用
- **[Cursor 使用教程](./cursor-guide.md)** — 在 Cursor 中安装和使用
- **[Claude Code 使用教程](./claude-code-guide.md)** — 在 Claude Code 中安装和使用

## 相关资源

- [Superpowers GitHub](https://github.com/obra/superpowers)
- [Superpowers Discord](https://discord.gg/superpowers)
- [OpenCode 官方文档](https://opencode.ai/docs/)
- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code)
