# CLI 参考

OpenSpec CLI（`openspec`）提供用于项目设置、验证、状态检查和管理的终端命令。这些命令补充了 [命令](./commands.md) 中记录的 AI 斜杠命令（如 `/opsx:propose`）。

## 总结

| 类别 | 命令 | 目的 |
|------|------|------|
| **设置** | `init`、`update` | 在项目中初始化和更新 OpenSpec |
| **浏览** | `list`、`view`、`show` | 探索变更和规范 |
| **验证** | `validate` | 检查变更和规范的问题 |
| **生命周期** | `archive` | 完成已完成的变更 |
| **工作流** | `status`、`instructions`、`templates`、`schemas` | 工件驱动的工作流支持 |
| **模式** | `schema init`、`schema fork`、`schema validate`、`schema which` | 创建和管理自定义工作流 |
| **配置** | `config` | 查看和修改设置 |
| **实用** | `feedback`、`completion` | 反馈和 shell 集成 |

---

## 人类 vs 代理命令

大多数 CLI 命令设计用于终端中的**人类使用**。某些命令也通过 JSON 输出支持**代理/脚本使用**。

### 仅限人类的命令

这些命令是交互式的，专为终端使用设计：

| 命令 | 目的 |
|------|------|
| `openspec init` | 初始化项目（交互式提示） |
| `openspec view` | 交互式仪表板 |
| `openspec config edit` | 在编辑器中打开配置 |
| `openspec feedback` | 通过 GitHub 提交反馈 |
| `openspec completion install` | 安装 shell 完成功能 |

### 代理兼容命令

这些命令支持 `--json` 输出，供 AI 代理和脚本以编程方式使用：

| 命令 | 人类使用 | 代理使用 |
|------|---------|---------|
| `openspec list` | 浏览变更/规范 | `--json` 用于结构化数据 |
| `openspec show <item>` | 读取内容 | `--json` 用于解析 |
| `openspec validate` | 检查问题 | `--all --json` 用于批量验证 |
| `openspec status` | 查看工件进度 | `--json` 用于结构化状态 |
| `openspec instructions` | 获取下一步 | `--json` 用于代理指令 |
| `openspec templates` | 查找模板路径 | `--json` 用于路径解析 |
| `openspec schemas` | 列出可用模式 | `--json` 用于模式发现 |

---

## 全局选项

这些选项适用于所有命令：

| 选项 | 描述 |
|------|------|
| `--version`、`-V` | 显示版本号 |
| `--no-color` | 禁用彩色输出 |
| `--help`、`-h` | 显示命令帮助 |

---

## 设置命令

### `openspec init`

在项目中初始化 OpenSpec。创建文件夹结构并配置 AI 工具集成。

默认行为使用全局配置默认值：配置文件 `core`、交付 `both`、工作流 `propose, explore, apply, archive`。

```
openspec init [path] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `path` | 否 | 目标目录（默认：当前目录） |

**选项：**

| 选项 | 描述 |
|------|------|
| `--tools <list>` | 非交互式配置 AI 工具。使用 `all`、`none` 或逗号分隔的列表 |
| `--force` | 自动清理旧文件而不提示 |
| `--profile <profile>` | 为此 init 运行覆盖全局配置文件（`core` 或 `custom`） |

`--profile custom` 使用全局配置中当前选择的任何工作流（`openspec config profile`）。

**支持的工具 ID（`--tools`）：** `amazon-q`、`antigravity`、`auggie`、`claude`、`cline`、`codex`、`codebuddy`、`continue`、`costrict`、`crush`、`cursor`、`factory`、`gemini`、`github-copilot`、`iflow`、`kilocode`、`kiro`、`opencode`、`pi`、`qoder`、`qwen`、`roocode`、`trae`、`windsurf`

**示例：**

```bash
# 交互式初始化
openspec init

# 在特定目录中初始化
openspec init ./my-project

# 非交互式：为 Claude 和 Cursor 配置
openspec init --tools claude,cursor

# 为所有受支持的工具配置
openspec init --tools all

# 为此运行覆盖配置文件
openspec init --profile core

# 跳过提示并自动清理旧文件
openspec init --force
```

**它创建什么：**

```
openspec/
├── specs/              # 你的规范（信息源）
├── changes/            # 提议的更改
└── config.yaml         # 项目配置

.claude/skills/         # Claude Code 技能（如果选择了 claude）
.cursor/skills/         # Cursor 技能（如果选择了 cursor）
.cursor/commands/       # Cursor OPSX 命令（如果交付包括命令）
... (其他工具配置)
```

---

### `openspec update`

在升级 CLI 后更新 OpenSpec 指令文件。使用你当前的全局配置文件、选择的工作流和交付模式重新生成 AI 工具配置文件。

```
openspec update [path] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `path` | 否 | 目标目录（默认：当前目录） |

**选项：**

| 选项 | 描述 |
|------|------|
| `--force` | 即使文件是最新的也强制更新 |

**示例：**

```bash
# npm 升级后更新指令文件
npm update @fission-ai/openspec
openspec update
```

---

## 浏览命令

### `openspec list`

列出项目中的变更或规范。

```
openspec list [options]
```

**选项：**

| 选项 | 描述 |
|------|------|
| `--specs` | 列出规范而非变更 |
| `--changes` | 列出变更（默认） |
| `--sort <order>` | 按 `recent`（默认）或 `name` 排序 |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 列出所有活动变更
openspec list

# 列出所有规范
openspec list --specs

# JSON 输出用于脚本
openspec list --json
```

**输出（文本）：**

```
Active changes:
  add-dark-mode     UI 主题切换支持
  fix-login-bug     会话超时处理
```

---

### `openspec view`

显示用于探索规范和变更的交互式仪表板。

```
openspec view
```

打开一个基于终端的界面，用于导航项目的规范和变更。

---

### `openspec show`

显示变更或规范的详细信息。

```
openspec show [item-name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `item-name` | 否 | 变更或规范的名称（如果省略则提示） |

**选项：**

| 选项 | 描述 |
|------|------|
| `--type <type>` | 指定类型：`change` 或 `spec`（如果不明确则自动检测） |
| `--json` | 输出为 JSON |
| `--no-interactive` | 禁用提示 |

**变更特定选项：**

| 选项 | 描述 |
|------|------|
| `--deltas-only` | 仅显示 delta 规范（JSON 模式） |

**规范特定选项：**

| 选项 | 描述 |
|------|------|
| `--requirements` | 仅显示需求，排除场景（JSON 模式） |
| `--no-scenarios` | 排除场景内容（JSON 模式） |
| `-r, --requirement <id>` | 按 1 索引显示特定需求（JSON 模式） |

**示例：**

```bash
# 交互式选择
openspec show

# 显示特定变更
openspec show add-dark-mode

# 显示特定规范
openspec show auth --type spec

# JSON 输出用于解析
openspec show add-dark-mode --json
```

---

## 验证命令

### `openspec validate`

验证变更和规范是否存在结构问题。

```
openspec validate [item-name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `item-name` | 否 | 要验证的特定项目（如果省略则提示） |

**选项：**

| 选项 | 描述 |
|------|------|
| `--all` | 验证所有变更和规范 |
| `--changes` | 验证所有变更 |
| `--specs` | 验证所有规范 |
| `--type <type>` | 当名称不明确时指定类型：`change` 或 `spec` |
| `--strict` | 启用严格验证模式 |
| `--json` | 输出为 JSON |
| `--concurrency <n>` | 最大并行验证（默认：6，或 `OPENSPEC_CONCURRENCY` 环境变量） |
| `--no-interactive` | 禁用提示 |

**示例：**

```bash
# 交互式验证
openspec validate

# 验证特定变更
openspec validate add-dark-mode

# 验证所有变更
openspec validate --changes

# 使用 JSON 输出验证所有内容（用于 CI/脚本）
openspec validate --all --json

# 增加并行性的严格验证
openspec validate --all --strict --concurrency 12
```

**输出（文本）：**

```
Validating add-dark-mode...
  ✓ proposal.md valid
  ✓ specs/ui/spec.md valid
  ⚠ design.md: 缺少"技术方法"章节

发现 1 个警告
```

**输出（JSON）：**

```json
{
  "version": "1.0.0",
  "results": {
    "changes": [
      {
        "name": "add-dark-mode",
        "valid": true,
        "warnings": ["design.md: 缺少'技术方法'章节"]
      }
    ]
  },
  "summary": {
    "total": 1,
    "valid": 1,
    "invalid": 0
  }
}
```

---

## 生命周期命令

### `openspec archive`

归档已完成的变更并将 delta 规范合并到主规范。

```
openspec archive [change-name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `change-name` | 否 | 要归档的变更（如果省略则提示） |

**选项：**

| 选项 | 描述 |
|------|------|
| `-y, --yes` | 跳过确认提示 |
| `--skip-specs` | 跳过规范更新（用于基础设施/工具/仅文档更改） |
| `--no-validate` | 跳过验证（需要确认） |

**示例：**

```bash
# 交互式归档
openspec archive

# 归档特定变更
openspec archive add-dark-mode

# 无提示归档（CI/脚本）
openspec archive add-dark-mode --yes

# 归档不影响规范的工具更改
openspec archive update-ci-config --skip-specs
```

**它做什么：**

1. 验证变更（除非 `--no-validate`）
2. 提示确认（除非 `--yes`）
3. 将 delta 规范合并到 `openspec/specs/`
4. 将变更文件夹移动到 `openspec/changes/archive/YYYY-MM-DD-<name>/`

---

## 工作流命令

这些命令支持工件驱动的 OPSX 工作流。它们对于人类检查进度和代理确定下一步都很有用。

### `openspec status`

显示变更的工件完成状态。

```
openspec status [options]
```

**选项：**

| 选项 | 描述 |
|------|------|
| `--change <id>` | 变更名称（如果省略则提示） |
| `--schema <name>` | 模式覆盖（从变更配置自动检测） |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 交互式状态检查
openspec status

# 特定变更的状态
openspec status --change add-dark-mode

# 用于代理使用的 JSON
openspec status --change add-dark-mode --json
```

**输出（文本）：**

```
Change: add-dark-mode
Schema: spec-driven
Progress: 2/4 工件完成

[x] proposal
[ ] design
[x] specs
[-] tasks（被设计阻塞）
```

**输出（JSON）：**

```json
{
  "changeName": "add-dark-mode",
  "schemaName": "spec-driven",
  "isComplete": false,
  "applyRequires": ["tasks"],
  "artifacts": [
    {"id": "proposal", "outputPath": "proposal.md", "status": "done"},
    {"id": "design", "outputPath": "design.md", "status": "ready"},
    {"id": "specs", "outputPath": "specs/**/*.md", "status": "done"},
    {"id": "tasks", "outputPath": "tasks.md", "status": "blocked", "missingDeps": ["design"]}
  ]
}
```

---

### `openspec instructions`

获取创建工件或应用任务的丰富说明。被 AI 代理用于了解接下来要创建什么。

```
openspec instructions [artifact] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `artifact` | 否 | 工件 ID：`proposal`、`specs`、`design`、`tasks` 或 `apply` |

**选项：**

| 选项 | 描述 |
|------|------|
| `--change <id>` | 变更名称（在非交互模式下必需） |
| `--schema <name>` | 模式覆盖 |
| `--json` | 输出为 JSON |

**特殊情况：** 使用 `apply` 作为工件以获取任务实施说明。

**示例：**

```bash
# 获取下一个工件的说明
openspec instructions --change add-dark-mode

# 获取特定工件说明
openspec instructions design --change add-dark-mode

# 获取应用/实施说明
openspec instructions apply --change add-dark-mode

# 用于代理消费的 JSON
openspec instructions design --change add-dark-mode --json
```

**输出包括：**

- 工件的模板内容
- 来自配置的项目上下文
- 来自依赖工件的内容
- 来自配置的每个工件规则

---

### `openspec templates`

显示模式中所有工件的已解析模板路径。

```
openspec templates [options]
```

**选项：**

| 选项 | 描述 |
|------|------|
| `--schema <name>` | 要检查的模式（默认：`spec-driven`） |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 显示默认模式的模板路径
openspec templates

# 显示自定义模式的模板
openspec templates --schema my-workflow

# 用于程序化使用的 JSON
openspec templates --json
```

**输出（文本）：**

```
Schema: spec-driven

Templates:
  proposal  → ~/.openspec/schemas/spec-driven/templates/proposal.md
  specs     → ~/.openspec/schemas/spec-driven/templates/specs.md
  design    → ~/.openspec/schemas/spec-driven/templates/design.md
  tasks     → ~/.openspec/schemas/spec-driven/templates/tasks.md
```

---

### `openspec schemas`

列出可用的工作流模式及其描述和工件流程。

```
openspec schemas [options]
```

**选项：**

| 选项 | 描述 |
|------|------|
| `--json` | 输出为 JSON |

**示例：**

```bash
openspec schemas
```

**输出：**

```
Available schemas:

  spec-driven (package)
    默认的规范驱动开发工作流
    流程：proposal → specs → design → tasks

  my-custom (project)
    此项目的自定义工作流
    流程：research → proposal → tasks
```

---

## 模式命令

用于创建和管理自定义工作流模式的命令。

### `openspec schema init`

创建新的项目本地模式。

```
openspec schema init <name> [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `name` | 是 | 模式名称（kebab-case） |

**选项：**

| 选项 | 描述 |
|------|------|
| `--description <text>` | 模式描述 |
| `--artifacts <list>` | 逗号分隔的工件 ID（默认：`proposal,specs,design,tasks`） |
| `--default` | 设置为项目默认模式 |
| `--no-default` | 不提示设置为默认 |
| `--force` | 覆盖现有模式 |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 交互式模式创建
openspec schema init research-first

# 非交互式并带有特定工件
openspec schema init rapid \
  --description "快速迭代工作流" \
  --artifacts "proposal,tasks" \
  --default
```

**它创建什么：**

```
openspec/schemas/<name>/
├── schema.yaml           # 模式定义
└── templates/
    ├── proposal.md       # 每个工件的模板
    ├── specs.md
    ├── design.md
    └── tasks.md
```

---

### `openspec schema fork`

将现有模式复制到你的项目以进行自定义。

```
openspec schema fork <source> [name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `source` | 是 | 要复制的模式 |
| `name` | 否 | 新模式名称（默认：`<source>-custom`） |

**选项：**

| 选项 | 描述 |
|------|------|
| `--force` | 覆盖现有目标 |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 复制内置的 spec-driven 模式
openspec schema fork spec-driven my-workflow
```

---

### `openspec schema validate`

验证模式的结构和模板。

```
openspec schema validate [name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `name` | 否 | 要验证的模式（如果省略则验证所有） |

**选项：**

| 选项 | 描述 |
|------|------|
| `--verbose` | 显示详细的验证步骤 |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 验证特定模式
openspec schema validate my-workflow

# 验证所有模式
openspec schema validate
```

---

### `openspec schema which`

显示模式从哪里解析（对于调试优先级很有用）。

```
openspec schema which [name] [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `name` | 否 | 模式名称 |

**选项：**

| 选项 | 描述 |
|------|------|
| `--all` | 列出所有模式及其来源 |
| `--json` | 输出为 JSON |

**示例：**

```bash
# 检查模式来自哪里
openspec schema which spec-driven
```

**输出：**

```
spec-driven resolves from: package
  Source: /usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven
```

**模式优先级：**

1. 项目：`openspec/schemas/<name>/`
2. 用户：`~/.local/share/openspec/schemas/<name>/`
3. 包：内置模式

---

## 配置命令

### `openspec config`

查看和修改全局 OpenSpec 配置。

```
openspec config <subcommand> [options]
```

**子命令：**

| 子命令 | 描述 |
|--------|------|
| `path` | 显示配置文件位置 |
| `list` | 显示所有当前设置 |
| `get <key>` | 获取特定值 |
| `set <key> <value>` | 设置值 |
| `unset <key>` | 移除键 |
| `reset` | 重置为默认值 |
| `edit` | 在 `$EDITOR` 中打开 |
| `profile [preset]` | 交互式或通过预设配置工作流配置文件 |

**示例：**

```bash
# 显示配置文件路径
openspec config path

# 列出所有设置
openspec config list

# 获取特定值
openspec config get telemetry.enabled

# 设置值
openspec config set telemetry.enabled false

# 显式设置字符串值
openspec config set user.name "My Name" --string

# 移除自定义设置
openspec config unset user.name

# 重置所有配置
openspec config reset --all --yes

# 在编辑器中编辑配置
openspec config edit

# 使用基于动作的向导配置配置文件
openspec config profile

# 快速预设：将工作流切换到 core（保持交付模式）
openspec config profile core
```

`openspec config profile` 从当前状态摘要开始，然后让你选择：
- 更改交付 + 工作流
- 仅更改交付
- 仅更改工作流
- 保持当前设置（退出）

如果你保持当前设置，则不会写入任何更改，也不会显示更新提示。如果没有配置更改但当前项目文件与你的全局配置文件/交付不同步，OpenSpec 将显示警告并建议运行 `openspec update`。按 `Ctrl+C` 也会干净地取消流程（无堆栈跟踪）并以代码 `130` 退出。在工作流检查列表中，`[x]` 表示工作流在全局配置中选中。要将这些选择应用到项目文件，请运行 `openspec update`（或在项目内提示时选择"立即将更改应用到该项目？"）。

**交互式示例：**

```bash
# 仅交付更新
openspec config profile
# 选择：仅更改交付
# 选择交付：仅技能

# 仅工作流更新
openspec config profile
# 选择：仅更改工作流
# 在检查列表中切换工作流，然后确认
```

---

## 实用命令

### `openspec feedback`

提交关于 OpenSpec 的反馈。创建 GitHub 问题。

```
openspec feedback <message> [options]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `message` | 是 | 反馈消息 |

**选项：**

| 选项 | 描述 |
|------|------|
| `--body <text>` | 详细描述 |

**要求：** 必须安装并验证 GitHub CLI（`gh`）。

**示例：**

```bash
openspec feedback "添加对自定义工件类型的支持" \
  --body "我想定义内置工件之外的自己的工件类型。"
```

---

### `openspec completion`

管理 OpenSpec CLI 的 shell 完成功能。

```
openspec completion <subcommand> [shell]
```

**子命令：**

| 子命令 | 描述 |
|--------|------|
| `generate [shell]` | 将完成脚本输出到 stdout |
| `install [shell]` | 为你的 shell 安装完成 |
| `uninstall [shell]` | 移除已安装的完成 |

**支持的 shell：** `bash`、`zsh`、`fish`、`powershell`

**示例：**

```bash
# 安装完成（自动检测 shell）
openspec completion install

# 为特定 shell 安装
openspec completion install zsh

# 生成脚本用于手动安装
openspec completion generate bash > ~/.bash_completion.d/openspec

# 卸载
openspec completion uninstall
```

---

## 退出代码

| 代码 | 含义 |
|------|------|
| `0` | 成功 |
| `1` | 错误（验证失败、缺少文件等） |

---

## 环境变量

| 变量 | 描述 |
|------|------|
| `OPENSPEC_CONCURRENCY` | 批量验证的默认并发性（默认：6） |
| `EDITOR` 或 `VISUAL` | 用于 `openspec config edit` 的编辑器 |
| `NO_COLOR` | 设置时禁用彩色输出 |

---

## 相关文档

- [命令](./commands.md) - AI 斜杠命令（`/opsx:propose`、`/opsx:apply` 等）
- [工作流程](./workflows.md) - 常见模式和何时使用每个命令
- [自定义](./customization.md) - 创建自定义模式和模板
- [入门指南](./getting-started.md) - 首次设置指南
