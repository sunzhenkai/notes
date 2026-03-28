# Claude Code 命令参考（`claude` CLI）

本文档整理 **Claude Code** 命令行程序 `claude` 的用法：顶层子命令、启动参数（flags）、以及 **交互会话内**以 `/` 开头的内置命令。

**校验说明：** 已在当前环境执行 **`claude --version` / `claude --help`** 及主要子命令的 `--help` 做核对。下文 **第 3～4 节**以该校验时的 **Claude Code 2.1.62** 输出为准；你本机版本不同请以 `claude --help` 为准。官方在线文档（[CLI reference](https://code.claude.com/docs/en/cli-reference.md)）可能包含更新版本的额外子命令或标志，已收在 **附录 A**。

---

## 1. 快速对照

| 类别 | 说明 |
|------|------|
| **可执行名** | `claude` |
| **交互会话** | 在项目目录执行 `claude`，在提示符下输入自然语言或 `/命令` |
| **非交互（打印模式）** | `claude -p "…"` 或 `claude --print`（`-p` 会跳过工作区信任对话框，仅在你信任的目录使用） |
| **续聊 / 恢复** | `-c` / `--continue`，`-r` / `--resume`（均可带可选参数，见下） |
| **子命令（2.1.62 `claude --help` 所列）** | `agents`、`auth`、`doctor`、`install`、`mcp`、`plugin`、`setup-token`、`update`（与 `upgrade` 同义） |

在会话中输入 **`/`** 可浏览当前环境可用的全部命令；部分命令随平台、订阅或功能开关隐藏（见 [Built-in commands](https://code.claude.com/docs/en/commands.md)）。

---

## 2. 启动方式与会话形态

### 2.1 基本调用

| 形式 | 说明 |
|------|------|
| `claude` | 进入当前目录的交互会话 |
| `claude "初始提示"` | 启动时附带第一条用户消息（作为 `prompt` 参数） |
| `claude -p "查询"` | 打印模式：执行后退出，无交互 TUI |
| `cat file \| claude -p "查询"` | 将管道 stdin 作为输入（配合 `--input-format` 等） |

### 2.2 续聊与恢复（与 2.1.62 一致）

| 形式 | 说明 |
|------|------|
| `claude -c` / `claude --continue` | 继续**当前目录**最近一次会话 |
| `claude -c -p "查询"` | 在同一延续会话上执行单次打印查询 |
| `claude -r <会话ID或名称>` | 恢复指定会话 |
| `claude -r` / `claude --resume` | 无参数：打开交互式会话选择器；亦可传可选搜索词（见 `--help` 中 `resume [value]`） |
| `claude --resume … --fork-session` | 恢复时**新建**会话 ID，不覆盖原会话 |
| `claude --from-pr [值]` | 按 PR 号/URL 恢复关联会话；无参时可打开选择器 |

会话显示名可在会话内用 **`/rename`** 设置（本机 2.1.62 的 `claude --help` **未**列出 `-n` / `--name` 启动参数；若你版本中有，见附录 A）。

### 2.3 打印模式（`-p` / `--print`）常用搭配（2.1.62）

| 标志 | 说明 |
|------|------|
| `--output-format text\|json\|stream-json` | 输出结构 |
| `--input-format text\|stream-json` | 输入格式；`stream-json` 为实时流式输入 |
| `--include-partial-messages` | 流式输出局部片段（需 `--print` 且 `--output-format=stream-json`） |
| `--replay-user-messages` | 将 stdin 中的用户消息再输出到 stdout 做确认（需 `stream-json` 输入与输出） |
| `--max-budget-usd <金额>` | API 花费上限（美元） |
| `--no-session-persistence` | 不持久化会话，不可恢复 |
| `--json-schema '<schema>'` | 结构化输出 JSON Schema 校验 |
| `--fallback-model <model>` | 主模型过载时自动降级（**仅**与 `--print` 一起生效） |

---

## 3. 顶层子命令（2.1.62）

### 3.1 `claude update` / `claude upgrade`

检查并安装更新（`update` 与 `upgrade` 为同一命令）。

### 3.2 `claude install [options] [target]`

安装 Claude Code **原生构建**。`[target]` 可为 `stable`、`latest` 或具体版本号。`--force`：即使已安装也强制重装。

### 3.3 `claude doctor`

检查 **自动更新器**健康状态（与交互里 `/doctor` 的全面诊断不同侧重时，以各自输出为准）。

### 3.4 `claude setup-token`

配置长期认证令牌（需 Claude 订阅；详见交互提示）。

### 3.5 `claude auth`

| 子命令 | 说明 |
|--------|------|
| `claude auth login` | 登录。**2.1.62 帮助列出：** `--email`、 `--sso`。若需 Console/API 计费账号等流程，以 [Authentication](https://code.claude.com/docs/en/authentication.md) 为准 |
| `claude auth logout` | 登出 |
| `claude auth status` | 认证状态（`--text` 人类可读等选项见 `claude auth status --help`） |

会话内快捷方式：`/login`、`/logout`。

### 3.6 `claude agents [options]`

列出已配置的 agents。**选项：** `--setting-sources <sources>`（与顶层同名参数含义一致）。

### 3.7 `claude mcp`

管理 MCP 服务器。

**`claude mcp add [options] <name> <commandOrUrl> [args...]`**

- **传输：** `-t, --transport <stdio|sse|http>`，未指定时默认为 **stdio**。
- **HTTP 示例：** `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp`
- **Header：** `-H, --header`（帮助文案称可用于 WebSocket 等场景，按提示格式传递）
- **stdio 与环境变量：** `-e, --env KEY=value`（可多次）
- **作用域：** `-s, --scope local|user|project`，**默认 `local`**
- **OAuth：** `--callback-port`、`--client-id`、`--client-secret`（或通过环境变量 `MCP_CLIENT_SECRET`）

**`--` 用法：** 所有 `claude mcp add` 的选项须出现在 **`<name>` 之前**；`--` 之后为子进程命令与参数。

**其它子命令：**

| 子命令 | 说明 |
|--------|------|
| `add-json [options] <name> <json>` | 用 JSON 字符串添加（帮助中描述为 stdio 或 SSE） |
| `add-from-claude-desktop [options]` | 从 Claude Desktop 导入（**Mac 与 WSL**） |
| `list` | 列出已配置服务器 |
| `get <name>` | 查看单个服务器详情 |
| `remove [options] <name>` | 删除 |
| `reset-project-choices` | 重置本项目中对已批准/拒绝的 **project 级** `.mcp.json` 服务器的选择 |
| `serve [options]` | 启动 Claude Code 作为 MCP server（`-d`/`--debug`、`--verbose`） |

会话内管理：`/mcp`。

### 3.8 `claude plugin`

| 子命令 | 说明 |
|--------|------|
| `install` / `i` | `claude plugin install [options] <plugin>`；`-s user|project|local`，默认 **user** |
| `uninstall` / `remove` | `claude plugin uninstall [options] <plugin>`；`-s` 默认 **user**（**2.1.62 无** `--keep-data`，若新版本增加见附录） |
| `enable` / `disable` | 启用或禁用插件 |
| `update` | 更新到最新版（提示可能需重启生效） |
| `list` | 列出已安装插件；`--json`；`--available` 需与 `--json` 同用 |
| `validate <path>` | 校验插件或 marketplace 的 manifest |
| `marketplace` | 子命令：`add <source>`、`list`、`remove|rm`、`update [name]` |

会话内：`/plugin`、`/reload-plugins`。

### 3.9 `claude remote-control`（未出现在 2.1.62 的 `claude --help` 列表中）

本机执行 `claude remote-control --help` 在未登录时会提示需 **claude.ai 订阅**并先登录。说明二进制内**包含**该命令，但 **`claude --help` 的 Commands 表未列出**（可能是隐藏或帮助滞后）。用途与参数以登录后帮助或 [Remote Control](https://code.claude.com/docs/en/remote-control.md) 为准。

---

## 4. 启动标志一览（与 Claude Code 2.1.62 `claude --help` 对齐）

下列为顶层 `claude [options] [command] [prompt]` 的 **Options**；说明为中文摘要。

### 4.1 工作目录、会话、IDE、工作树

| 标志 | 说明 |
|------|------|
| `--add-dir <directories...>` | 额外允许工具访问的目录 |
| `-c`, `--continue` | 继续当前目录最近会话 |
| `-r`, `--resume [value]` | 按 ID 恢复，或打开选择器（可选搜索词） |
| `--fork-session` | 与 `--resume` / `--continue` 联用，新建会话 ID |
| `--session-id <uuid>` | 固定会话 UUID |
| `--from-pr [value]` | 按 PR 恢复或 PR 选择器 |
| `--ide` | 仅当检测到唯一可用 IDE 时自动连接 |
| `-w`, `--worktree [name]` | 新建 git worktree 并在其中会话 |
| `--tmux` / `--tmux=classic` | 依赖 `--worktree`；iTerm2 原生分屏或经典 tmux |

### 4.2 权限与工具

| 标志 | 说明 |
|------|------|
| `--permission-mode <mode>` | **可选值（2.1.62）：** `acceptEdits`、`bypassPermissions`、`default`、`dontAsk`、`plan` |
| `--allow-dangerously-skip-permissions` | 允许选用「跳过权限」类模式，但不默认开启；仅建议隔离/无网络沙箱 |
| `--dangerously-skip-permissions` | 绕过权限检查；高风险，同上 |
| `--allowedTools` / `--allowed-tools <tools...>` | 允许的工具列表（逗号或空格分隔，示例见 `--help`） |
| `--disallowedTools` / `--disallowed-tools <tools...>` | 禁止的工具列表 |
| `--tools <tools...>` | 内置工具子集；`""` 全关，`default` 全部，或 `Bash,Edit,Read` 形式 |

### 4.3 模型与其它行为

| 标志 | 说明 |
|------|------|
| `--model <model>` | 模型别名（如 `sonnet`、`opus`）或完整 ID |
| `--effort <level>` | **2.1.62 帮助仅列出：** `low`、`medium`、`high`（会话级；是否与在线文档的 `max` 等一致取决于版本） |
| `--betas <betas...>` | API key 用户的 beta 请求头 |
| `--fallback-model <model>` | 与 `--print` 联用，主模型过载时回退 |
| `--agent <agent>` | 覆盖设置中的 `agent` |
| `--agents <json>` | JSON 动态定义自定义 agents |
| `--chrome` / `--no-chrome` | 启用 / 禁用 Claude in Chrome |
| `--system-prompt <prompt>` | 替换本会话系统提示（覆盖默认） |
| `--append-system-prompt <prompt>` | 在默认系统提示后追加 |

### 4.4 MCP 与插件

| 标志 | 说明 |
|------|------|
| `--mcp-config <configs...>` | 从 JSON 文件或字符串加载 MCP（可多个） |
| `--strict-mcp-config` | 仅使用上述配置中的 MCP |
| `--mcp-debug` | **已弃用**，请用 `--debug` |
| `--plugin-dir <paths...>` | 本会话仅从指定目录加载插件（可重复） |

### 4.5 配置、调试、通用

| 标志 | 说明 |
|------|------|
| `--settings <file-or-json>` | 额外加载设置 JSON 文件或字符串 |
| `--setting-sources <sources>` | `user,project,local` 逗号分隔 |
| `-d`, `--debug [filter]` | 调试类别过滤，如 `api,hooks` 或 `!1p,!file` |
| `--debug-file <path>` | 将调试日志写入文件（隐式开启 debug） |
| `--verbose` | 详细输出 |
| `--disable-slash-commands` | **2.1.62 描述为：** 禁用全部 **skills**（slash 能力） |
| `-h`, `--help` | 帮助 |
| `-v`, `--version` | 版本号 |

### 4.6 打印模式专用

| 标志 | 说明 |
|------|------|
| `-p`, `--print` | 打印结果后退出 |
| `--output-format` | `text`（默认）、`json`、`stream-json` |
| `--input-format` | `text`（默认）、`stream-json` |
| `--include-partial-messages` | 流式输出增量消息块 |
| `--replay-user-messages` | 流式下回显用户消息到 stdout |
| `--json-schema <schema>` | 结构化输出校验 |
| `--max-budget-usd <amount>` | 花费上限 |
| `--no-session-persistence` | 不写入磁盘、不可恢复 |

### 4.7 其它顶层标志（2.1.62）

| 标志 | 说明 |
|------|------|
| `--file <specs...>` | 启动时下载文件资源，格式 `file_id:relative_path` |

### 4.8 System prompt 补充

**2.1.62** 顶层帮助仅列出 `--system-prompt` 与 `--append-system-prompt`，**未**列出 `--system-prompt-file` / `--append-system-prompt-file`；若你版本中有，见附录 A。在线文档建议：优先用 **append** 以保留内置能力。

---

## 5. 交互式内置命令（`/…`）

在 Claude Code 提示符下输入。表中 `<arg>` 表示必填，`[arg]` 表示可选。以下为 [Built-in commands](https://code.claude.com/docs/en/commands.md) 的整理译意；**以你本机输入 `/` 补全为准**。

| 命令 | 用途 |
|------|------|
| `/add-dir <路径>` | 向当前会话增加工作目录 |
| `/agents` | 管理 subagent 配置 |
| `/btw <问题>` | 侧车式快速提问，不写入主对话历史 |
| `/chrome` | 配置 Claude in Chrome |
| `/clear` | 清空对话释放上下文；别名 `/reset`、`/new` |
| `/color [颜色\|default]` | 提示条颜色 |
| `/compact [说明]` | 压缩对话 |
| `/config` | 打开设置；别名 `/settings` |
| `/context` | 上下文占用可视化 |
| `/copy [N]` | 复制最近第 N 条助手回复 |
| `/cost` | Token 使用统计 |
| `/desktop` | 转到桌面端继续（macOS / Windows）；别名 `/app` |
| `/diff` | 交互 diff |
| `/doctor` | 诊断安装与配置 |
| `/effort [low\|medium\|high\|max\|auto]` | 调整 effort |
| `/exit` | 退出；别名 `/quit` |
| `/export [文件名]` | 导出对话 |
| `/extra-usage` | 超额用量配置 |
| `/fast [on\|off]` | fast mode |
| `/feedback [内容]` | 反馈；别名 `/bug` |
| `/branch [名称]` | 对话分支；别名 `/fork` |
| `/help` | 帮助 |
| `/hooks` | Hook 配置 |
| `/ide` | IDE 集成 |
| `/init` | 初始化 `CLAUDE.md` 等 |
| `/insights` | 使用分析报告 |
| `/install-github-app` | GitHub Actions 应用 |
| `/install-slack-app` | Slack 应用 |
| `/keybindings` | 快捷键配置 |
| `/login`、`/logout` | 登录 / 登出 |
| `/mcp` | MCP 与 OAuth |
| `/memory` | `CLAUDE.md` 与 auto-memory |
| `/mobile` | 移动端二维码；别名 `/ios`、`/android` |
| `/model [模型]` | 选择模型 |
| `/passes` | 邀请体验（视账号） |
| `/permissions` | 权限；别名 `/allowed-tools` |
| `/plan [描述]` | 规划模式 |
| `/plugin` | 插件 |
| `/pr-comments [PR]` | GitHub PR 评论（常需 `gh`） |
| `/privacy-settings` | 隐私（Pro / Max） |
| `/release-notes` | 变更日志 |
| `/reload-plugins` | 重载插件 |
| `/remote-control` | 遥控；别名 `/rc` |
| `/remote-env` | `--remote` 类云端会话的环境默认值 |
| `/rename [名称]` | 会话重命名 |
| `/resume [会话]` | 恢复；别名 `/continue` |
| `/review` | 已弃用，改用 code-review 插件 |
| `/rewind` | 检查点；别名 `/checkpoint` |
| `/sandbox` | 沙箱模式 |
| `/schedule [描述]` | 云定时任务 |
| `/security-review` | 安全审查当前分支变更 |
| `/skills` | 列出 skills |
| `/stats` | 使用统计可视化 |
| `/status` | Status 页 |
| `/statusline` | 状态行配置 |
| `/stickers` | 贴纸 |
| `/tasks` | 后台任务 |
| `/terminal-setup` | 终端快捷键 |
| `/theme` | 主题 |
| `/upgrade` | 订阅升级页 |
| `/usage` | 用量与限流 |
| `/vim` | Vim 模式切换 |
| `/voice` | 语音听写 |

### 5.1 MCP 动态命令

格式常为 `/mcp__<服务器>__<prompt>`，以连接后补全为准，见 [MCP 文档](https://code.claude.com/docs/en/mcp.md)。

### 5.2 捆绑技能

如 `/simplify`、`/batch`、`/debug`、`/loop` 等与 `/` 命令并列出现，以当前版本与 [Skills](https://code.claude.com/docs/en/skills.md) 为准。

---

## 6. 相关官方文档

- [CLI reference](https://code.claude.com/docs/en/cli-reference.md)  
- [Built-in commands](https://code.claude.com/docs/en/commands.md)  
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md)  
- [MCP](https://code.claude.com/docs/en/mcp.md)  
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)  
- [Settings](https://code.claude.com/docs/en/settings.md)  
- [Environment variables](https://code.claude.com/docs/en/env-vars.md)

---

## 7. 说明

- 终端下的「Claude 程序」多指 **`claude`（Claude Code）**；API、网页客户端命令集不同。  
- **权威核对方式：** 定期执行 `claude --help`、`claude <子命令> --help`。

---

## 附录 A：在线文档或更新版本中可能出现、Claude Code 2.1.62 顶层 `--help` 未列出的项

下列来自 [code.claude.com CLI reference](https://code.claude.com/docs/en/cli-reference.md) 等，**在你本机未必存在**；升级 CLI 后请用 `--help` 复查。

| 类型 | 示例 |
|------|------|
| 子命令 | `claude auto-mode defaults`、`claude auto-mode config` |
| 启动标志 | `--name` / `-n`、`--teleport`、`--remote`、`--remote-control` / `--rc`、`--enable-auto-mode`、`--max-turns`、`--bare`、`--permission-prompt-tool`、`--init`、`--init-only`、`--maintenance`、`--channels`、`--dangerously-load-development-channels`、`--teammate-mode`、`--append-system-prompt-file`、`--system-prompt-file` |
| 权限模式 | 文档中的 `auto` 模式与 `Shift+Tab` 循环；**2.1.62** 的 `--permission-mode` 可选值未在帮助中列出 `auto`，以交互 UI 与新版 CLI 为准 |
| 其它 | `claude auth login --console`（2.1.62 的 `login --help` 未显示） |
| 插件卸载 | `plugin uninstall --keep-data`（2.1.62 无） |

若你希望附录随本机版本自动对齐，可在仓库中保留一行当前校验版本号，并在升级后重新运行 `claude --help` 更新本文。
