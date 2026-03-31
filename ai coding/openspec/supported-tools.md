# 支持的工具

OpenSpec 与许多 AI 编程助手一起工作。当你运行 `openspec init` 时，OpenSpec 使用你活动的配置文件/工作流选择和交付模式配置选定的工具。

## 工作原理

对于每个选定的工具，OpenSpec 可以安装：

1. **技能**（如果交付包括技能）：`.../skills/openspec-*/SKILL.md`
2. **命令**（如果交付包括命令）：工具特定的 `opsx-*` 命令文件

默认情况下，OpenSpec 使用 `core` 配置文件，其中包括：
- `propose`
- `explore`
- `apply`
- `archive`

你可以通过 `openspec config profile` 然后运行 `openspec update` 来启用扩展工作流（`new`、`continue`、`ff`、`verify`、`sync`、`bulk-archive`、`onboard`）。

## 工具目录参考

| 工具 (ID) | 技能路径模式 | 命令路径模式 |
|-----------|-------------|--------------|
| Amazon Q Developer (`amazon-q`) | `.amazonq/skills/openspec-*/SKILL.md` | `.amazonq/prompts/opsx-<id>.md` |
| Antigravity (`antigravity`) | `.agent/skills/openspec-*/SKILL.md` | `.agent/workflows/opsx-<id>.md` |
| Auggie (`auggie`) | `.augment/skills/openspec-*/SKILL.md` | `.augment/commands/opsx-<id>.md` |
| Claude Code (`claude`) | `.claude/skills/openspec-*/SKILL.md` | `.claude/commands/opsx/<id>.md` |
| Cline (`cline`) | `.cline/skills/openspec-*/SKILL.md` | `.clinerules/workflows/opsx-<id>.md` |
| CodeBuddy (`codebuddy`) | `.codebuddy/skills/openspec-*/SKILL.md` | `.codebuddy/commands/opsx/<id>.md` |
| Codex (`codex`) | `.codex/skills/openspec-*/SKILL.md` | `$CODEX_HOME/prompts/opsx-<id>.md`\* |
| Continue (`continue`) | `.continue/skills/openspec-*/SKILL.md` | `.continue/prompts/opsx-<id>.prompt` |
| CoStrict (`costrict`) | `.cospec/skills/openspec-*/SKILL.md` | `.cospec/openspec/commands/opsx-<id>.md` |
| Crush (`crush`) | `.crush/skills/openspec-*/SKILL.md` | `.crush/commands/opsx/<id>.md` |
| Cursor (`cursor`) | `.cursor/skills/openspec-*/SKILL.md` | `.cursor/commands/opsx-<id>.md` |
| **Cursor 注意** | - 默认使用 `core` profile，提供4个命令：`propose`、`explore`、`apply`、`archive`<br>- 使用连字符格式：`/opsx-propose`、`/opsx-apply`（区别于冒号格式）<br>- 详见 [Cursor IDE 专用指南](./cursor-guide.md) | |
| Factory Droid (`factory`) | `.factory/skills/openspec-*/SKILL.md` | `.factory/commands/opsx-<id>.md` |
| Gemini CLI (`gemini`) | `.gemini/skills/openspec-*/SKILL.md` | `.gemini/commands/opsx/<id>.toml` |
| GitHub Copilot (`github-copilot`) | `.github/skills/openspec-*/SKILL.md` | `.github/prompts/opsx-<id>.prompt.md`\*\* |
| iFlow (`iflow`) | `.iflow/skills/openspec-*/SKILL.md` | `.iflow/commands/opsx-<id>.md` |
| Kilo Code (`kilocode`) | `.kilocode/skills/openspec-*/SKILL.md` | `.kilocode/workflows/opsx-<id>.md` |
| Kiro (`kiro`) | `.kiro/skills/openspec-*/SKILL.md` | `.kiro/prompts/opsx-<id>.prompt.md` |
| OpenCode (`opencode`) | `.opencode/skills/openspec-*/SKILL.md` | `.opencode/commands/opsx-<id>.md` |
| Pi (`pi`) | `.pi/skills/openspec-*/SKILL.md` | `.pi/prompts/opsx-<id>.md` |
| Qoder (`qoder`) | `.qoder/skills/openspec-*/SKILL.md` | `.qoder/commands/opsx/<id>.md` |
| Qwen Code (`qwen`) | `.qwen/skills/openspec-*/SKILL.md` | `.qwen/commands/opsx-<id>.toml` |
| RooCode (`roocode`) | `.roo/skills/openspec-*/SKILL.md` | `.roo/commands/opsx-<id>.md` |
| Trae (`trae`) | `.trae/skills/openspec-*/SKILL.md` | 未生成（无命令适配器；使用基于技能的 `/openspec-*` 调用） |
| Windsurf (`windsurf`) | `.windsurf/skills/openspec-*/SKILL.md` | `.windsurf/workflows/opsx-<id>.md` |

\* Codex 命令安装在全局 Codex 主目录（如果设置 `$CODEX_HOME/prompts/`，否则 `~/.codex/prompts/`），而不是你的项目目录。

\*\* GitHub Copilot 提示文件在 IDE 扩展（VS Code、JetBrains、Visual Studio）中被识别为自定义斜杠命令。Copilot CLI 当前不直接使用 `.github/prompts/*.prompt.md`。

## 非交互式设置

对于 CI/CD 或脚本设置，使用 `--tools`（以及可选的 `--profile`）：

```bash
# 配置特定工具
openspec init --tools claude,cursor

# 配置所有受支持的工具
openspec init --tools all

# 跳过工具配置
openspec init --tools none

# 为此运行覆盖配置文件
openspec init --profile core
```

**可用工具 ID（`--tools`）：** `amazon-q`、`antigravity`、`auggie`、`claude`、`cline`、`codex`、`codebuddy`、`continue`、`costrict`、`crush`、`cursor`、`factory`、`gemini`、`github-copilot`、`iflow`、`kilocode`、`kiro`、`opencode`、`pi`、`qoder`、`qwen`、`roocode`、`trae`、`windsurf`

## 依赖于工作流的安装

OpenSpec 根据选择的工作流安装工作流工件：

- **核心配置文件（默认）：** `propose`、`explore`、`apply`、`archive`
- **自定义选择：** 所有工作流 ID 的任何子集：
  `propose`、`explore`、`new`、`continue`、`apply`、`ff`、`sync`、`archive`、`bulk-archive`、`verify`、`onboard`

换句话说，技能/命令数量依赖于配置文件和交付，而不是固定的。

## 生成的技能名称

当由配置文件/工作流配置选择时，OpenSpec 生成这些技能：

- `openspec-propose`
- `openspec-explore`
- `openspec-new-change`
- `openspec-continue-change`
- `openspec-apply-change`
- `openspec-ff-change`
- `openspec-sync-specs`
- `openspec-archive-change`
- `openspec-bulk-archive-change`
- `openspec-verify-change`
- `openspec-onboard`

请参阅[命令](./commands.md)了解命令行为和[CLI 参考](./cli-reference.md)了解 `init`/`update` 选项。

## 相关

- [CLI 参考](./cli-reference.md) — 终端命令
- [命令](./commands.md) — 斜杠命令和技能
- [入门指南](./getting-started.md) — 首次设置
