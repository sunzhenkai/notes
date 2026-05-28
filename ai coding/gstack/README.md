# GStack — AI 软件工厂

> YC CEO Garry Tan 开源的 AI 编程工作流框架，将 Claude Code 变成一支虚拟工程团队。
> 最后更新：2026年5月

## 简介

**gstack** 是一个角色化的 AI 编程技能包（Skills Pack）。它通过 23 个专家角色和 8 个强力工具，把一个通用的 AI 编程助手转变为结构化的虚拟工程团队——CEO 做产品决策、工程经理锁定架构、设计师审查视觉、QA 用真实浏览器测试、安全官做 OWASP 审计、发布工程师推送 PR。

**一句话定位：** 不是编辑器，不是 IDE，而是一套完整的 AI 编程**流程**。

- **作者**：Garry Tan（Y Combinator CEO）
- **GitHub**：[garrytan/gstack](https://github.com/garrytan/gstack)
- **许可**：MIT
- **要求**：Claude Code / Git / Bun v1.0+

---

## 核心理念

### 1. Boil the Lake（把湖水烧开）

AI 让"做完整的事"的边际成本趋近于零。当完整实现只比快捷方案多花几分钟时——**永远做完整的事**。

- 湖（Lake）：可煮——100% 测试覆盖、完整功能实现、所有边界情况
- 海（Ocean）：不可煮——从零重写整个系统、跨季度平台迁移
- **煮湖。把海标记为范围外。**

### 2. Search Before Building（先搜再做）

1000x 工程师的第一直觉是"有人已经解决这个问题了吗？"，而不是"让我从零设计"。

三层知识来源：
1. **经典（Tried and true）**——标准模式、久经考验的方案
2. **前沿（New and popular）**——最新实践、博客文章、生态趋势
3. **原创（First principles）**——从问题本身推导出的独到洞察（最有价值）

### 3. User Sovereignty（用户主权）

AI 推荐，用户决定。两个 AI 模型达成的共识是强信号，但不是命令。用户始终拥有模型缺少的上下文：领域知识、商业关系、战略时机、个人品味。

---

## Sprint 流程

gstack 不是工具集合，而是一套流程。技能按 Sprint 的顺序运行：

```
Think → Plan → Build → Review → Test → Ship → Reflect
```

每个技能的输出自动流入下一个技能。`/office-hours` 写的设计文档被 `/plan-ceo-review` 读取；`/plan-eng-review` 写的测试计划被 `/qa` 接续；`/review` 发现的 bug 在 `/ship` 中验证修复。

---

## 23 个专家角色

### 规划阶段

| 技能 | 角色 | 做什么 |
|------|------|--------|
| `/office-hours` | YC Office Hours | **起点。** 六个关键提问，在写代码前重新框定产品。挑战你的前提假设 |
| `/plan-ceo-review` | CEO / 创始人 | 重新思考问题。四种模式：扩展、选择性扩展、维持范围、缩减 |
| `/plan-eng-review` | 工程经理 | 锁定架构、数据流、图表、边界情况、测试 |
| `/plan-design-review` | 高级设计师 | 每个设计维度 0-10 评分，解释 10 分长什么样，然后编辑计划去实现 |
| `/plan-devex-review` | DX Lead | 开发者体验审查：开发者画像、TTHW 基准测试、魔法时刻设计 |
| `/autoplan` | 审查流水线 | **一条命令，自动跑完 CEO → 设计 → 工程 → DX 审查** |
| `/design-consultation` | 设计伙伴 | 从零构建完整设计系统 |
| `/design-shotgun` | 设计探索者 | 生成 4-6 个 AI 模型变体，浏览器中对比，迭代到满意为止 |
| `/design-html` | 设计工程师 | 把模型稿变成可发布的 HTML，30KB 零依赖 |

### 评审阶段

| 技能 | 角色 | 做什么 |
|------|------|--------|
| `/review` | Staff Engineer | 找到通过 CI 但在生产环境会爆炸的 bug |
| `/design-review` | 会写代码的设计师 | 同样的审计 + 自动修复，原子提交，前后截图 |
| `/devex-review` | DX Tester | 实际测试上手流程，对比计划评分 |
| `/codex` | 第二意见 | OpenAI Codex CLI 的独立代码审查。三种模式：审查、对抗、咨询 |

### 测试 & 质量阶段

| 技能 | 角色 | 做什么 |
|------|------|--------|
| `/qa` | QA Lead | 真实浏览器测试，找 bug，修复，原子提交，回归测试 |
| `/qa-only` | QA 报告员 | 只报告 bug，不改代码 |
| `/benchmark` | 性能工程师 | 页面加载、Core Web Vitals、资源大小基线 |
| `/cso` | 首席安全官 | OWASP Top 10 + STRIDE 威胁模型 |
| `/investigate` | 调试员 | 系统性根因分析。铁律：没有调查就不修复 |

### 发布阶段

| 技能 | 角色 | 做什么 |
|------|------|--------|
| `/ship` | 发布工程师 | 同步 main、跑测试、审计覆盖率、推送、开 PR |
| `/land-and-deploy` | 发布工程师 | 合并 PR → 等 CI → 部署 → 验证生产健康 |
| `/canary` | SRE | 部署后监控循环：控制台错误、性能回归、页面失败 |

### 辅助阶段

| 技能 | 角色 | 做什么 |
|------|------|--------|
| `/retro` | 工程经理 | 团队周报：每人统计、交付连续、测试健康趋势 |
| `/browse` | QA 工程师 | 给 AI 眼睛——真实 Chromium 浏览器，真实点击，真实截图 |
| `/document-release` | 技术写作者 | 自动更新所有项目文档 |
| `/document-generate` | 文档作者 | 用 Diataxis 框架从零生成文档 |
| `/learn` | 记忆 | 管理跨会话学习：审查、搜索、修剪、导出项目模式 |

### 8 个强力工具

| 技能 | 做什么 |
|------|--------|
| `/careful` | 安全护栏——破坏性命令前警告（rm -rf、DROP TABLE、force-push） |
| `/freeze` | 编辑锁——限制文件编辑到一个目录 |
| `/guard` | 完整安全 = `/careful` + `/freeze` |
| `/open-gstack-browser` | 启动 GStack Browser——侧边栏、反检测、自动模型路由 |
| `/setup-deploy` | 一键配置部署平台 |
| `/setup-gbrain` | GBrain 持久知识库——从零到运行 < 5 分钟 |
| `/sync-gbrain` | 保持知识库最新——重新索引代码 |
| `/gstack-upgrade` | 自升级到最新版本 |

---

## 安装

### 基础安装（30 秒）

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup
```

### OpenCode 安装

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack
cd ~/gstack && ./setup --host opencode
```

技能安装到：`~/.config/opencode/skills/gstack-*/`

### 支持的 AI Agent

安装脚本自动检测已安装的 Agent，也可指定：

| Agent | 参数 | 安装位置 |
|-------|------|---------|
| Claude Code | 默认 | `~/.claude/skills/gstack/` |
| OpenCode | `--host opencode` | `~/.config/opencode/skills/gstack-*/` |
| Cursor | `--host cursor` | `~/.cursor/skills/gstack-*/` |
| Codex CLI | `--host codex` | `~/.codex/skills/gstack-*/` |
| Factory Droid | `--host factory` | `~/.factory/skills/gstack-*/` |
| Slate | `--host slate` | `~/.slate/skills/gstack-*/` |
| Kiro | `--host kiro` | `~/.kiro/skills/gstack-*/` |
| Hermes | `--host hermes` | `~/.hermes/skills/gstack-*/` |
| GBrain | `--host gbrain` | `~/.gbrain/skills/gstack-*/` |

### 团队模式（推荐）

```bash
# 在仓库内运行，团队成员自动获得 gstack
(cd ~/.claude/skills/gstack && ./setup --team) && ~/.claude/skills/gstack/bin/gstack-team-init required
```

---

## 适用场景

- **独立开发者**——一个人完成设计、开发、测试、发布全流程
- **技术创始人**——兼职做产品，full-time 跑公司
- **首次使用 AI 编程**——结构化角色比空白 prompt 好用
- **Tech Lead**——每次 PR 自动获得严格审查、QA、发布自动化
- **并行 Sprint**——搭配 Conductor 同时跑 10-15 个并行任务

---

## 与同类工具对比

| 特性 | gstack | OpenSpec | Superpowers |
|------|--------|----------|-------------|
| 定位 | AI 软件工厂（流程） | 规范驱动开发（SDD） | Agent 增强技能包 |
| 核心单位 | Sprint 流程 | Change 生命周期 | Skill 工作流 |
| 角色系统 | 23 个专家角色 | 无 | 可扩展 |
| 浏览器测试 | 真实 Chromium | 无 | 无 |
| 支持工具 | 10+ Agent | 20+ Agent | Claude Code / OpenCode |
| 适用阶段 | 全生命周期 | 编码前 | 编码中 |
| 配置文件 | CLAUDE.md 块 | openspec/ 目录 | .opencode/ 目录 |

---

## 文档目录

- **[OpenCode 使用教程](./opencode-guide.md)** — 在 OpenCode 中安装、配置和使用 gstack 的完整指南

## 相关资源

- [gstack GitHub](https://github.com/garrytan/gstack)
- [Builder Ethos](https://github.com/garrytan/gstack/blob/master/ETHOS.md)
- [Boil the Lake](https://garryslist.org/posts/boil-the-ocean)
- [gstack Discord](https://discord.gg/gstack)
