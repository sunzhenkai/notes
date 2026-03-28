# Claude Code：核心功能与配置域

精简说明常用能力：**做什么、怎么用**。细节与版本差异以 [code.claude.com](https://code.claude.com/docs/llms.txt) 与本地 `claude --help` 为准。

---

## 三种权限模式

**作用：** 控制 Claude 执行工具（读写文件、Bash 等）前是否询问你。

| 模式（设置键） | 描述 | 典型用法 |
|----------------|------|----------|
| **default** | 多数敏感操作需确认 | 日常、不信任目录 |
| **acceptEdits** | 自动接受编辑类权限，减少打断 | 大批量改代码 |
| **plan** | 先只读分析与出方案，再让你批准改动 | 重构、摸陌生代码库 |
| **dontAsk** / **bypassPermissions** | 预批准或跳过权限（高风险） | 仅隔离沙箱、自动化流水线 |

**使用方式：**

- **CLI：** 启动时 `claude --permission-mode plan`；会话中 **`Shift+Tab`** 循环切换（是否含 `auto` 等取决于版本与订阅）。
- **VS Code / Desktop / Web：** 提示框旁的模式选择器（名称与上述键对应）。

---

## 后台任务管理

**作用：** 长任务不阻塞你离开；多会话并行。

**使用方式：**

- **CLI：** `/tasks` 查看与管理后台任务（以当前版本列表为准）。
- **云端：** `claude --remote "…"`（若本版 CLI 支持）或网页 [claude.ai/code](https://claude.ai/code) 发起任务，稍后查看。
- **并行本地：** `claude -w <worktree名>` 在独立 git worktree 里开会话；桌面端可多窗口会话。

---

## 回滚（Checkpoint / Rewind）

**作用：** 按「轮」撤销 Claude **编辑工具**造成的文件变更，或同时回退对话；也可从某条消息起做**摘要**以省上下文。**不跟踪**纯 Bash 改盘、会话外手工改文件。

**使用方式：**

- 连按 **`Esc` `Esc`**，或输入 **`/rewind`**（别名 `/checkpoint`）。
- 在列表中选检查点：**恢复代码+对话 / 仅对话 / 仅代码**，或 **Summarize from here**（从该点起压缩对话，不动磁盘文件）。

---

## 添加 MCP Server

**作用：** 通过 Model Context Protocol 连接外部工具与数据（Figma、DB、Slack 等）。

**使用方式：**

- **CLI：** `claude mcp add --transport http <名> <URL>`；stdio：`claude mcp add -e KEY=val <名> -- npx …`；JSON：`claude mcp add-json <名> '<json>'`；管理：`claude mcp list | get | remove`；会话内 **`/mcp`** 做连接与 OAuth。
- **作用域：** `-s local|user|project`（CLI 默认多为 **local**；**project** 常写入 `.mcp.json`，团队共享，首次使用往往需单独批准）。

---

## 恢复会话

**作用：** 接着上次对话与上下文继续。

**使用方式：**

- `claude -c` / `claude --continue`：当前目录**最近一次**会话。
- `claude -r` / `claude --resume [id或名]`：指定会话或打开选择器。
- 会话内：`/resume`、`/continue`。
- 分支尝试：`--fork-session` 与 `--resume` 同用，保留原会话 ID。

---

## 上下文压缩

**作用：** 对话过长时**保留要点、丢掉逐字历史**，腾出 token。

**使用方式：**

- **`/compact [可选说明]`**：按你的侧重点生成摘要替换尾部消息。
- **`/rewind` → Summarize from here**：从选中消息起向前压缩，前面细节保留更完整。

---

## 清空上下文

**作用：** **丢弃当前对话历史**（不等价于撤销文件）；释放上下文，从零开聊。

**使用方式：**

- **`/clear`**，或别名 **`/reset`**、**`/new`**。

---

## CLAUDE.md 与 `/memory`

**作用：** **项目级长期说明**（栈、命令、禁忌、架构），每次会话自动注入；可配 **auto-memory** 让 Claude 自动记下构建命令等。

**使用方式：**

- 在项目根（及子目录）放 **`CLAUDE.md`**；复杂项目可拆 **`.claude/rules/`** 按路径加载。
- **`/memory`**：编辑记忆文件、开关 auto-memory、查看自动记忆条目；**`/init`** 可生成初始 `CLAUDE.md`。

---

## Hook

**作用：** 在固定生命周期（如工具执行前后）跑**确定性脚本**（格式化、Lint、通知），**不经过模型**。

**使用方式：**

- 配置写在项目 **`.claude/`**（或用户级 `~/.claude/`）的 hooks 定义中；会话内 **`/hooks`** 查看。
- 详见 [Hooks](https://code.claude.com/docs/en/hooks.md)。

---

## Agent Skills（Skills）

**作用：** 可复用的**说明 / 流程 / 知识**；可 **`/命令名`** 触发，也可由模型按描述自动选用（可配置为仅手动触发以省上下文）。

**使用方式：**

- 放在 **`.claude/skills/`** 等约定目录；插件可带 **命名空间** 命令（如 `/plugin:cmd`）。
- 会话内 **`/skills`** 列出；官方 [Skills](https://code.claude.com/docs/en/skills.md)。

---

## Agents（Subagents）

**作用：** **独立上下文**里的子代理：大量读文件、专项任务只把**摘要**写回主会话，避免主对话被撑爆。

**使用方式：**

- 配置在 **`.claude/`** 下 agent 定义；`claude agents` 列出；会话内 **`/agents`** 管理；启动时可用 `--agents '<json>'` 临时注入。

---

## Skills vs Agents（对比）

| 维度 | **Skills** | **Agents（Subagents）** |
|------|------------|-------------------------|
| 本质 | 知识 + 可触发工作流 | 单独一轮 agent 循环的工人 |
| 上下文 | 进入**当前**会话（或 skill 指定 fork） | **隔离**上下文，主会话只看到结果摘要 |
| 适合 | 规范、检查清单、`/deploy` 类重复流程 | 大范围检索、并行子任务、只要结论不要过程 |
| 组合 | Skill 可描述何时 spawn；子代理可 **预载** 指定 skills | 主代理分配子任务并合并摘要 |

---

## Plugin

**作用：** 把 **skills、agents、hooks、MCP** 等打成**可安装包**，经 marketplace 分发，团队统一环境。

**使用方式：**

- `claude plugin install <名>[@marketplace]`；`list` / `enable` / `disable` / `update` / `uninstall`；`plugin marketplace` 管理源；会话内 **`/plugin`**、**`/reload-plugins`**。
- 详见 [Plugins](https://code.claude.com/docs/en/plugins.md)。

---

## 配置文件与保存域（Scope）

配置会落在 **用户全局 / 项目 / 本地（常 gitignore）** 等不同层级，合并与覆盖规则以官方为准；下列便于自查「改的是哪一台、哪一个仓库」。

| 内容 | 常见位置 / 机制 | 域说明 |
|------|-----------------|--------|
| **用户全局** | `~/.claude/`（如 `settings.json`、全局 skills、hooks） | 当前用户所有项目可见 |
| **项目** | 仓库内 **`.claude/settings.json`**、**`CLAUDE.md`**、**`.mcp.json`**、项目级插件列表 | 随 Git 分享（勿提交密钥） |
| **本地（local）** | 同仓库下本地覆盖配置、**`claude mcp add -s local`** 等 | 仅本机，常不提交 |
| **MCP 服务器** | `claude mcp add -s user|project|local` | **user** 跨项目；**project** 写入 `.mcp.json`；**local** 仅当前工作区习惯用法 |
| **插件** | `claude plugin install -s user|project|local` | **user** 个人；**project** 团队克隆即用；**local** 个人试装 |
| **设置加载** | 启动标志 `--setting-sources user,project,local` | 控制本次会话读哪些来源 |
| **托管/企业** | 组织下发的 managed 策略 | 可能覆盖部分用户/项目项 |

**实用建议：** 密钥用环境变量或 **local** scope；团队共识放 **project**；个人偏好放 **user**。

---

## 另见

- [命令全集（CLI + `/`）](./cli-and-commands.md)
- [使用手册（分章教程向）](./README.md)
