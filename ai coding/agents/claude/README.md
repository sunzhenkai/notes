# Claude (Anthropic)

## 简介

**Claude** 是 Anthropic 的 AI 助手；**Claude Code** 是其终端 / IDE / 桌面 / 网页上的 **Agent 式编程工具**：读代码库、改文件、跑命令、接 MCP 等。下文 **「使用手册」** 整理 Claude Code 的用法；时间戳可与某套视频章节对照，便于跳转复习。

**Claude Code 产品页与文档：** [claude.com/product/claude-code](https://claude.com/product/claude-code) · [code.claude.com 文档索引](https://code.claude.com/docs/llms.txt)

---

## Claude Code 使用手册

### 第一部分：环境搭建与基础交互

#### 安装 Claude Code

**原生安装（推荐，通常带后台自动更新）**

- macOS / Linux / WSL：`curl -fsSL https://claude.ai/install.sh | bash`
- Windows PowerShell：`irm https://claude.ai/install.ps1 | iex`
- Windows CMD：需先装 [Git for Windows](https://git-scm.com/downloads/win)，再按官方文档执行 `install.cmd` 流程

**包管理器（需自行定期升级）**

- Homebrew：`brew install --cask claude-code`，之后 `brew upgrade claude-code`
- WinGet：`winget install Anthropic.ClaudeCode`

进入项目目录后执行 `claude` 即可启动。更多平台要求、卸载与故障排查见官方 [Setup](https://code.claude.com/docs/en/setup.md) / [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md)。

**运行环境：** 除 CLI 外，还支持 VS Code / Cursor 扩展、JetBrains 插件、桌面端、网页 [claude.ai/code](https://claude.ai/code) 等；各端共用同一套引擎能力，配置如 `CLAUDE.md`、MCP 等可跨端使用（详见 [Platforms](https://code.claude.com/docs/en/platforms.md)）。

#### 登录与授权

- 首次使用会引导登录。订阅账号与 [Anthropic Console](https://console.anthropic.com/) API 计费等场景，以官方认证文档为准：[Authentication](https://code.claude.com/docs/en/authentication.md)。
- CLI 常用命令：
  - `claude auth login`（可加 `--console` 等选项）
  - `claude auth logout`
  - `claude auth status`（`--text` 为人类可读输出）

#### 第一个实战问题

在项目根目录启动后，用自然语言描述任务即可，例如：

```bash
cd your-project
claude "解释这个项目的入口与主要模块职责"
```

Claude Code 会检索代码库、多文件推理并给出修改或命令建议；复杂功能可让它「先规划再改」——见下文规划模式。

#### 三种模式详解（默认 / 自动接受编辑 / 规划）

默认模式: -
自动接收编辑模式: accept edits on
规划模式: plan mode on

NOTE: 通过 Shift + Tab 切换模式

**权限模式**决定 Claude 是否在执行前询问你；可在会话中用快捷键或 UI 切换，也可用启动参数固定。

- **CLI 会话内：** `Shift+Tab` 在模式间循环：`default` → `acceptEdits` → `plan` → `auto`（`auto` 需满足计划与模型等条件，且通常需启动时加 `--enable-auto-mode` 才会进入循环；若启用绕过权限，循环中会多出相应项）。
- **启动时指定：** `claude --permission-mode plan`（同理可用 `default`、`acceptEdits`、`auto`、`bypassPermissions` 等，以官方 [Permission modes](https://code.claude.com/docs/en/permission-modes.md) 为准）。

**命名的对应关系（便于记忆）：**

| 说法 | 设置键 / 概念 | 要点 |
|----------|----------------|------|
| 默认 | `default` | 敏感操作前会询问，适合不熟悉代码库或高风险改动 |
| 自动 | `acceptEdits` / `auto` | `acceptEdits` 自动接受编辑类权限；`auto` 由后台分类器代你决策是否拦截（Team 等计划 + 新模型要求，见官方文档） |
| 规划 | `plan` | 先只读分析与出方案，你确认后再进入实际修改 |

默认模式还可在 `settings.json` 里用 `permissions.defaultMode` 持久化。VS Code / Desktop 界面上的「Ask permissions / Auto accept edits / Plan mode」等与上述键一一对应，详见 [Permission modes](https://code.claude.com/docs/en/permission-modes.md)。

---

### 第二部分：复杂任务处理与终端控制

#### 执行终端命令（Bash）

Claude Code 内置 **Bash** 等工具，可安装依赖、跑测试、执行构建脚本。是否每次提示授权由当前**权限模式**与 **allowedTools / disallowedTools** 等规则决定（见 [Permissions](https://code.claude.com/docs/en/permissions.md)、[Tools reference](https://code.claude.com/docs/en/tools-reference.md)）。

**注意：** 下文 **Checkpoint / Rewind** 主要跟踪「编辑工具」对文件的修改；纯 Bash 造成的文件变更一般无法通过 rewind 一键撤销，重要操作仍应依赖 Git。

#### 使用规划模式（Plan Mode）

- 启动：`claude --permission-mode plan`，或在交互界面中切换到 Plan。
- 用途：先通读与设计，再让你审查计划，减少「一上来就改错一大片」的风险；适合重构、跨模块功能、不熟悉域时的探索。

#### 跳过所有权限检测（`dangerously-skip-permissions`）

- **标志：** `--dangerously-skip-permissions` 会跳过权限提示（具体仍受官方文档中「仍不会跳过」项约束，请务必阅读 [Permission modes · bypass](https://code.claude.com/docs/en/permission-modes.md#skip-all-checks-with-bypasspermissions-mode)）。
- **`--allow-dangerously-skip-permissions`：** 仅允许在会话中**选用**绕过模式，而不默认开启，便于与 `--permission-mode plan` 等组合。
- **风险：** 仅在隔离环境、可信代码库或自动化流水线中考虑；日常开发优先用 `default` / `plan` / 精细 `allowedTools`。

#### 后台任务管理（Background Tasks）

- **网页 / 云端：** 可在 [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md) 发起长任务，稍后查看结果；CLI 可用 `--remote` 等能力与云端会话配合（见 [CLI reference](https://code.claude.com/docs/en/cli-reference.md)）。
- **本地：** 桌面端支持多会话、计划任务；CLI 可与 `git worktree`（如 `claude -w feature-name`）并行隔离分支上的任务（见 [Common workflows](https://code.claude.com/docs/en/common-workflows.md)）。
- **续聊与远程：** `--teleport` 可把网页会话拉回终端；Remote Control 可从手机或其他设备接续本地会话（[Remote Control](https://code.claude.com/docs/en/remote-control.md)）。

---

### 第三部分：多模态与上下文管理

#### 版本回滚（Rewind / Checkpointing）

Claude Code 会按对话与编辑自动建立检查点。

- **操作：** 连按两次 `Esc`，或使用 `/rewind`，在列表中选择某一用户消息对应的点，然后选择：
  - 同时恢复代码与对话
  - 只恢复对话 / 只恢复代码
  - **Summarize from here：** 从该点起把后续对话压缩成摘要，释放上下文，而不回滚磁盘文件
- **局限：** Bash 等命令对文件的修改、会话外手工改文件等通常不在检查点内；检查点不能替代 Git。详见 [Checkpointing](https://code.claude.com/docs/en/checkpointing.md)。

#### 图片处理

Claude 模型支持视觉输入；在 Claude Code 各端按产品当前能力附加截图或设计稿，便于对照 UI / 报错界面排查问题（能力以官方发布为准）。

#### 安装 MCP Server（以 Figma 为例）

**MCP（Model Context Protocol）** 把外部工具与数据源接到 Claude Code 上。

- CLI 管理：`claude mcp`（子命令与配置见 [MCP 文档](https://code.claude.com/docs/en/mcp.md)）。
- 可通过 `~/.claude.json`、项目内配置或 `--mcp-config ./mcp.json` 指定服务器；`--strict-mcp-config` 可限制仅使用指定配置中的 MCP。
- Figma 等具体服务器：在对应 MCP 市场或厂商文档中查找安装方式，再在 Claude Code 中注册同名服务；「用 MCP 还原设计稿」即依赖此类工具读出设计数据并在本地生成代码。

#### 恢复历史会话（Resume）

- 继续当前目录最近一次会话：`claude -c` 或 `claude --continue`
- 按 ID 或名称恢复：`claude -r "session-name-or-id"` 或 `claude --resume` 打开交互选择器
- 恢复时新开分支会话（不覆盖原会话 ID）：`claude --resume ... --fork-session`
- 命名会话便于识别：`claude -n "my-feature"`，会话中也可用 `/rename`

完整列表见 [CLI reference](https://code.claude.com/docs/en/cli-reference.md)。

#### 使用 MCP 工具还原设计稿

在 MCP 已连接设计工具（如 Figma）的前提下，在对话中要求 Claude 拉取指定画板/组件信息并生成前端代码结构；具体能力取决于 MCP 服务器暴露的工具与权限。

#### 上下文压缩与清除

- **`/compact` 类能力：** 压缩对话以腾出上下文（与 Rewind 里「Summarize from here」的针对性压缩互补）。
- **成本与窗口：** 见 [Context window 说明](https://code.claude.com/docs/en/context-window.md)、[Costs](https://code.claude.com/docs/en/costs.md)。
- **打印 / 脚本模式：** `claude -p "..."` 适合管道与 CI；可加 `--max-turns`、`--max-budget-usd`、`--no-session-persistence` 等（见 CLI 文档）。

#### 项目记忆文件（`CLAUDE.md`）

- **作用：** 每次会话自动加载的项目说明：技术栈、目录约定、测试命令、禁止事项等。
- **位置：** 仓库根或子目录；可配合 `.claude/rules/` 做按路径加载的规则，避免单文件过长。详见 [Memory](https://code.claude.com/docs/en/memory.md)。
- **与 Skill 分工：** 永远要遵守的放 `CLAUDE.md`；偶尔查阅或 `/` 触发的流程放 Skill（见第四部分）。

**配置示例：**

```markdown
# 项目规范

## 编码标准
- 使用 TypeScript 和 React
- 遵循函数式编程原则

## 架构决策
- 使用 Redux 进行状态管理
- API 调用统一放在 services 目录

## 测试要求
- 单元测试使用 Jest
- E2E 测试使用 Cypress
```

**配置目录：** 项目下 `.claude` 目录还容纳 hooks、skills、commands、subagents、rules 等（[claude-directory](https://code.claude.com/docs/en/claude-directory.md)）。

---

### 第四部分：高级功能扩展与定制

#### Hook

在特定生命周期（如编辑前后、提交前、权限询问时）运行**确定性脚本**（shell 等），用于格式化、Lint、审计日志，**不经过模型**。配置与事件列表见 [Hooks](https://code.claude.com/docs/en/hooks.md) 与 [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)。

#### Agent Skill

**Skill** 是可复用的说明、知识与工作流；可用 `/命令` 显式调用，也可由模型按描述自动选用。可放在用户级、项目级或通过插件分发。详见 [Skills](https://code.claude.com/docs/en/skills.md)。Claude Code 也自带部分内置技能（如文档中提到的 `/simplify`、`/batch` 等，以当前版本为准）。

#### SubAgent

**Subagent** 在**独立上下文**中执行子任务，只把摘要结果写回主会话，适合大量读文件、并行子任务、避免主对话窗口被细节撑满。定义与 frontmatter 见 [Sub-agents](https://code.claude.com/docs/en/sub-agents.md)；CLI 可 `claude agents` 列出已配置子代理，或用 `--agents '{...}'` 临时注入 JSON 定义。

#### Skill 与 SubAgent 的区别（摘要）

| 维度 | Skill | Subagent |
|------|--------|----------|
| 本质 | 可加载的说明 / 流程 | 独立循环的工作单元 |
| 上下文 | 进入当前或其它约定上下文 | 隔离上下文，通常只回传摘要 |
| 典型用途 | 规范文档、可重复 `/` 工作流 | 大范围检索、专项审查、并行子任务 |

二者可组合（例如子代理预载指定 Skills）。官方对比表见 [Extend Claude Code](https://code.claude.com/docs/en/features-overview.md)。

#### Plugin

**Plugin** 把 Skills、Subagents、Hooks、MCP 等打成可安装单元，并可通过 **Marketplace** 分发。CLI：`claude plugin`（或 `claude plugins`）。见 [Plugins](https://code.claude.com/docs/en/plugins.md)、[Discover plugins](https://code.claude.com/docs/en/discover-plugins.md)、[Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)。

---

## 其它 Claude 产品（非 Claude Code 专述）

- **网页对话 Claude：** 代码生成、Artifacts、长上下文等。
- **Claude Cowork：** 团队协作文档与空间类能力（以官网说明为准）。
- **多平台：** Terminal、VS Code、Desktop、Web、JetBrains、iOS 等对 Claude 与 Claude Code 的支持略有差异，以上手册以 **Claude Code** 为主。

---

## 核心特性速览

- **强推理模型**（如 Opus / Sonnet 系列，以当前订阅与文档为准）
- **长上下文**与代码库级理解
- **Git 工作流：** 提交说明、分支、PR 等（见 [Common workflows](https://code.claude.com/docs/en/common-workflows.md)）
- **可编程自动化：** `claude -p`、管道输入、GitHub Actions / GitLab CI 集成等

---

## 最新动态（笔记整理时的参考）

- **Feb 2026** - Opus 4.6 等模型更新（以官方为准）
- 产品与市场活动见 [claude.com](https://claude.com)

---

## 定价（摘录，以官网为准）

- **Free** - 有限额度
- **Pro** - 个人付费档
- **Team / Enterprise** - 团队与企业管理
- **API** - 按量计费，见 [Pricing](https://claude.com/pricing)

---

## 相关链接

- **[Claude Code 命令参考（CLI 与子命令）](./cli-and-commands.md)** — `claude` 全部子命令、启动参数与 `/` 内置命令
- 官网：https://claude.ai
- 产品概览：https://claude.com/product/overview
- API 文档：https://docs.anthropic.com
- 控制台：https://platform.claude.com
- Claude Code 产品页：https://claude.com/product/claude-code
- Claude Code 文档（推荐书签）：https://code.claude.com/docs/llms.txt

