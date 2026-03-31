# OpenSpec — 规范驱动开发 (Spec-Driven Development)

> AI 编程助手的规范驱动开发框架，让人类与 AI 在写代码之前先对齐需求。
> 最后更新：2026年3月

## 概述

OpenSpec 是一个轻量级的规范层，核心理念是 **先达成共识，再编写代码**。它通过结构化的 Markdown 规范文档，让人类和 AI 在编码前就需求、设计和实现计划达成一致，从而解决 AI 编码中"需求模糊、结果不可预测"的问题。

- **GitHub**: [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- **官网**: [intent-driven.dev](https://intent-driven.dev/knowledge/openspec/)
- **许可**: MIT
- **要求**: Node.js 20.19.0+

## 核心理念

```
→ 流式而非僵化 (fluid not rigid)
→ 迭代而非瀑布 (iterative not waterfall)
→ 简单而非复杂 (easy not complex)
→ 支持棕地项目，不限于绿地 (built for brownfield not just greenfield)
→ 从个人项目到企业级可扩展 (scalable from personal projects to enterprises)
```

## 工作流程

OpenSpec 的核心是一个三阶段循环：**Propose → Apply → Archive**

### 1. Propose（提案）

通过斜杠命令让 AI 生成规范文档：

```
/opsx:propose "add-dark-mode"
```

AI 会自动创建 `openspec/changes/add-dark-mode/` 目录，包含：

- `proposal.md` — 为什么要做、改变什么
- `specs/` — 需求和场景
- `design.md` — 技术方案
- `tasks.md` — 实现清单

### 2. Apply（实施）

确认规范后，让 AI 按照任务清单执行：

```
/opsx:apply
```

AI 会按 tasks.md 中的清单逐步实现，完成后标记每个任务。

### 3. Archive（归档）

实施完成后归档，将变更合并到源规范中：

```
/opsx:archive
```

归档后，delta 规范合并到主规范，保持单一信息源（Single Source of Truth）。

## 快速开始

```bash
# 全局安装
npm install -g @fission-ai/openspec@latest

# 在项目中初始化
cd your-project
openspec init

# 告诉 AI 开始
/opsx:propose "your feature idea"
```

## 斜杠命令

### 简化工作流（推荐）

| 命令            | 说明             |
| --------------- | ---------------- |
| `/opsx:propose` | 创建变更提案     |
| `/opsx:apply`   | 按规范实施       |
| `/opsx:archive` | 归档已完成的变更 |

### 扩展工作流

通过 `openspec config profile` 切换到扩展模式后可用：

| 命令                 | 用途                                                                | 旧版 0.x 命令        |
| -------------------- | ------------------------------------------------------------------- | -------------------- |
| `/opsx-explore`      | 自由思考，只读模式，不写代码。允许在动手前理清思路，可衔接 opsx-new | -                    |
| `/opsx-new`          | 开始一个新变更                                                      | `/openspec:proposal` |
| `/opsx-continue`     | 创建下一个产物（一次一个）。产物是指 proposal、specs、design、tasks | `/openspec:proposal` |
| `/opsx-ff`           | Fast-Forward，按依赖顺序一口气生成四个产物。适合需求明确的场景      | `/openspec:proposal` |
| `/opsx-apply`        | 实现 tasks.md 里的任务                                              | `/openspec:apply`    |
| `/opsx-verify`       | 检查代码和规范是否一致                                              | -                    |
| `/opsx-sync`         | 预览规格合并（可选 —— 如需要会提示归档）                            | -                    |
| `/opsx-archive`      | 完成并归档变更                                                      | `/openspec:archive`  |
| `/opsx-bulk-archive` | 批量归档多个变更                                                    | -                    |
| `/opsx:onboard`      | 项目入门引导                                                        | -                    |

## 三种规范文档

### 1. Delta Specs（变更规范）

标记为 `ADDED`、`MODIFIED`、`REMOVED`，清晰传达提案内容，无需对比整个文档。

### 2. Source of Truth（源规范）

系统当前状态的唯一权威参考，所有 delta 变更最终合并到此文档。

### 3. Archived Specs（归档规范）

已合并的 delta 规范历史记录，保留决策脉络和审计轨迹。

## 支持的 AI 工具

OpenSpec 支持 20+ AI 编程助手，包括但不限于：

- Claude Code
- Cursor
- GitHub Copilot
- Windsurf
- Aider
- OpenCode
- ChatGPT
- Replit Agent

## 与同类工具对比

| 特性         | OpenSpec                    | Spec Kit (GitHub) | Kiro (AWS)        |
| ------------ | --------------------------- | ----------------- | ----------------- |
| 重量级       | 轻量                        | 较重              | 中等              |
| 阶段门控     | 无，自由迭代                | 严格阶段门控      | 有                |
| 工具锁定     | 无，支持 20+ 工具           | GitHub 生态       | Kiro IDE + Claude |
| 安装         | npm（简单）                 | Python（较复杂）  | IDE 内置          |
| 棕地项目支持 | 原生支持                    | 有限              | 有限              |
| 定制性       | 高（自定义 Profile/Schema） | 低                | 低                |

## 适用场景

- **需求频繁变化** — 需要快速迭代规范
- **AI 编码结果不可预测** — 需要事先对齐需求
- **棕地项目** — 现有项目需要增量引入规范
- **团队协作** — 需要统一的信息源
- **功能交互复杂** — 需要检测功能间 unintended interactions

## 最佳实践

1. **推荐模型**：使用高推理能力模型（如 Opus 4.5、GPT 5.2）效果最佳
2. **上下文管理**：开始实施前清空上下文窗口，保持干净的上下文
3. **小步迭代**：每次提案保持小范围、聚焦的变更
4. **及时归档**：完成后尽快归档，保持源规范的准确性

## CLI 常用命令

```bash
# 初始化项目
openspec init

# 配置 Profile
openspec config profile

# 更新 agent 指令
openspec update

# 升级 OpenSpec
npm install -g @fission-ai/openspec@latest
```

## 文档目录

- **入门**
  - [入门指南](./getting-started.md) - 了解 OpenSpec 如何工作，创建第一个变更
  - [工作流程](./workflows.md) - 常见的工作流模式和最佳实践
  - [Cursor IDE 专用指南](./cursor-guide.md) - Cursor IDE 的四个命令和 proposal 改进方法

- **命令参考**
  - [斜杠命令](./commands.md) - AI 助手中的斜杠命令（如 `/opsx:propose`）
  - [CLI 参考](./cli-reference.md) - 终端命令参考

- **核心概念**
  - [核心概念](./concepts.md) - 深入了解规范、变更、工件和 delta 规范
  - [支持的工具](./supported-tools.md) - 支持的 AI 编程助手列表

- **高级主题**
  - [自定义配置](./customization.md) - 自定义工作流和项目配置
  - [多语言指南](./multi-language-guide.md) - 配置非英语语言支持

## 相关资源

- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec 官方文档](https://intent-driven.dev/knowledge/openspec/)
- [OpenSpec 中文版](https://github.com/studyzy/OpenSpec-cn)
- [OpenSpec Skills 扩展](https://github.com/partme-ai/openspec-skills)
- [OpenSpec Discord](https://discord.gg/openspec)
