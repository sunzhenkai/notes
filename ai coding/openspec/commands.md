# 命令参考

这是 OpenSpec 斜杠命令的参考。这些命令在你的 AI 编程助手的聊天界面中调用（例如 Claude Code、Cursor、Windsurf）。

有关工作流模式和何时使用每个命令，请参阅[工作流程](./workflows.md)。有关 CLI 命令，请参阅[CLI 参考](./cli-reference.md)。

## 快速参考

### 默认快速路径（`core` 配置）

| 命令 | 目的 |
|------|------|
| `/opsx:propose` | 创建变更并在一步中生成规划工件 |
| `/opsx:explore` | 在承诺变更之前思考想法 |
| `/opsx:apply` | 从变更实施任务 |
| `/opsx:archive` | 归档已完成的变更 |

### 扩展工作流命令（自定义工作流选择）

| 命令 | 目的 |
|------|------|
| `/opsx:new` | 开始新的变更脚手架 |
| `/opsx:continue` | 基于依赖关系创建下一个工件 |
| `/opsx:ff` | 快速前进：一次性创建所有规划工件 |
| `/opsx:verify` | 验证实现与工件匹配 |
| `/opsx:sync` | 将 delta 规范合并到主规范 |
| `/opsx:bulk-archive` | 一次性归档多个变更 |
| `/opsx:onboard` | 通过完整工作流的引导教程 |

默认全局配置是 `core`。要启用扩展工作流命令，请运行 `openspec config profile`，选择工作流，然后在你的项目中运行 `openspec update`。

---

## 命令参考

### `/opsx:propose`

创建新变更并在一步中生成规划工件。这是 `core` 配置中的默认启动命令。

**语法：**
```text
/opsx:propose [change-name-or-description]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `change-name-or-description` | 否 | Kebab-case 名称或纯语言变更描述 |

**它做什么：**
- 创建 `openspec/changes/<change-name>/`
- 生成实施前所需的工件（对于 `spec-driven`：proposal、specs、design、tasks）
- 在变更准备好 `/opsx:apply` 时停止

**示例：**
```text
You: /opsx:propose add-dark-mode

AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md
     ✓ specs/ui/spec.md
     ✓ design.md
     ✓ tasks.md
     准备实施。运行 /opsx:apply。
```

**提示：**
- 使用此命令获得最快的端到端路径
- 如果你想要逐步工件控制，请启用扩展工作流并使用 `/opsx:new` + `/opsx:continue`

---

### `/opsx:explore`

思考想法、调查问题，并在承诺变更之前澄清需求。

**语法：**
```
/opsx:explore [topic]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `topic` | 否 | 你想探索或调查的内容 |

**它做什么：**
- 打开探索性对话，无需结构要求
- 调查代码库以回答问题
- 比较选项和方法
- 创建视觉图表以澄清思维
- 可以在洞察结晶时过渡到 `/opsx:propose`（默认）或 `/opsx:new`（扩展工作流）

**示例：**
```text
You: /opsx:explore

AI:  你想探索什么？

You: 我们应该如何为移动应用处理身份验证？

AI:  让我调查你当前的身份验证设置...
     [分析代码库]

     我看到你正在为 Web 应用使用基于会话的身份验证。
     对于移动应用，我们主要有三个选项：

     1. JWT 令牌（无状态，离线工作）
     2. OAuth2（如果你需要第三方登录）
     3. 扩展当前会话（更简单，但需要连接）

     你的 API 已经配置了 CORS。哪个方向让你感兴趣？

You: 让我们选择 JWT。我们可以开始变更吗？

AI:  准备好了。运行 /opsx:propose add-jwt-auth 开始。
```

**提示：**
- 当需求不明确或需要调查时使用
- 探索期间不创建工件
- 适合在决定之前比较多种方法
- 可以读取文件和搜索代码库

---

### `/opsx:new`

开始新的变更脚手架。创建变更文件夹并等待你使用 `/opsx:continue` 或 `/opsx:ff` 生成工件。

此命令是扩展工作流集的一部分（不包含在默认 `core` 配置中）。

**语法：**
```
/opsx:new [change-name] [--schema <schema-name>]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `change-name` | 否 | 变更文件夹名称（如果未提供则提示） |
| `--schema` | 否 | 要使用的工作流模式（默认：来自配置或 `spec-driven`） |

**它做什么：**
- 创建 `openspec/changes/<change-name>/` 目录
- 在变更文件夹中创建 `.openspec.yaml` 元数据文件
- 显示第一个工件模板，准备好创建
- 如果未提供，提示变更名称和模式

**它创建什么：**
```
openspec/changes/<change-name>/
└── .openspec.yaml    # 变更元数据（模式、创建日期）
```

**示例：**
```
You: /opsx:new add-dark-mode

AI:  Created openspec/changes/add-dark-mode/
     模式：spec-driven

     准备创建：proposal
     使用 /opsx:continue 创建它，或 /opsx:ff 创建所有工件。
```

**提示：**
- 使用描述性名称：`add-feature`、`fix-bug`、`refactor-module`
- 避免通用名称，如 `update`、`changes`、`wip`
- 模式也可以在项目配置中设置（`openspec/config.yaml`）

---

### `/opsx:continue`

在依赖链中创建下一个工件。一次创建一个工件以进行增量进度。

**语法：**
```
/opsx:continue [change-name]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `change-name` | 否 | 要继续的变更（如果未提供则从上下文推断） |

**它做什么：**
- 查询工件依赖关系图
- 显示哪些工件准备就绪与被阻塞
- 创建第一个就绪的工件
- 读取依赖文件以获取上下文
- 显示创建后可用的内容

**示例：**
```
You: /opsx:continue

AI:  变更：add-dark-mode

     工件状态：
     ✓ proposal    （完成）
     ◆ specs       （准备就绪）
     ◆ design      （准备就绪）
     ○ tasks       （被阻塞 - 需要：specs）

     正在创建规范...

     [读取 proposal.md，基于需求创建规范]

     ✓ 已创建 openspec/changes/add-dark-mode/specs/ui/spec.md

     现在可用：tasks
     运行 /opsx:continue 创建下一个工件。
```

**提示：**
- 当你想要在继续之前审查每个工件时使用
- 适合你想要控制的复杂变更
- 多个工件可能同时变得就绪
- 你可以在继续之前编辑已创建的工件

---

### `/opsx:ff`

通过工件创建快速前进。一次性创建所有规划工件。

**语法：**
```
/opsx:ff [change-name]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `change-name` | 否 | 要快速前进的变更（如果未提供则从上下文推断） |

**它做什么：**
- 按依赖顺序创建所有工件
- 通过待办事项列表跟踪进度
- 在所有 `apply-required` 工件完成时停止
- 在创建下一个工件之前读取每个依赖项

**示例：**
```
You: /opsx:ff add-dark-mode

AI:  正在快速前进 add-dark-mode...

     ✓ 正在创建 proposal.md
     ✓ 正在创建 specs/ui/spec.md
     ✓ 正在创建 design.md
     ✓ 正在创建 tasks.md

     所有规划工件完成！
     准备实施。运行 /opsx:apply 开始。
```

**提示：**
- 当你对要构建的内容有清晰的了解时使用
- 对于简单的变更，比 `/opsx:continue` 更快
- 你仍可在此后编辑工件
- 适合中小型功能

---

### `/opsx:apply`

从变更实施任务。完成任务清单，编写代码并勾选项目。

**语法：**
```
/opsx:apply [change-name]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `change-name` | 否 | 要实施的变更（如果未提供则从上下文推断） |

**它做什么：**
- 读取 `tasks.md` 并识别未完成的任务
- 逐一完成任务
- 根据需要编写代码、创建文件、运行测试
- 用复选框 `[x]` 标记任务完成

**示例：**
```
You: /opsx:apply

AI:  正在实施 add-dark-mode...

     读取 tasks.md：
     - [ ] 1.1 创建 ThemeContext
     - [ ] 1.2 添加 CSS 自定义属性
     - [ ] 1.3 实现 localStorage 持久化

     正在处理 1.1：创建 ThemeContext...
     [创建 src/context/ThemeContext.tsx]

     ✓ 1.1 完成

     正在处理 1.2：添加 CSS 自定义属性...
     [更新 src/styles/globals.css]

     ✓ 1.2 完成
     ...
```

**提示：**
- 如果中断，可以从中断处恢复
- 通过指定变更名称来处理并行变更
- 完成状态在 `tasks.md` 复选框中跟踪

---

### `/opsx:verify`

验证实现与变更工件匹配。检查完整性、正确性和一致性。

**语法：**
```
/opsx:verify [change-name]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `change-name` | 否 | 要验证的变更（如果未提供则从上下文推断） |

**它做什么：**
- 检查实现质量的三个维度
- 搜索代码库以查找实现证据
- 报告分类为 CRITICAL（关键）、WARNING（警告）或 SUGGESTION（建议）的问题
- 不阻止归档，但显示问题

**验证维度：**

| 维度 | 验证内容 |
|------|---------|
| **完整性** | 所有任务完成，所有需求已实施，场景已覆盖 |
| **正确性** | 实现与规范意图匹配，边缘情况已处理 |
| **一致性** | 设计决策反映在代码中，模式一致 |

**示例：**
```
You: /opsx:verify

AI:  正在验证 add-dark-mode...

     COMPLETENESS
     ✓ tasks.md 中的所有 8 个任务都已检查
     ✓ 规范中的需求有相应的代码
     ⚠ 场景"系统首选项检测"没有测试覆盖

     CORRECTNESS
     ✓ 实现与规范意图匹配
     ✓ 场景中的边缘情况已处理
     ✓ 错误状态与规范定义匹配

     COHERENCE
     ✓ 设计决策反映在代码结构中
     ✓ 命名约定与 design.md 一致
     ⚠ 设计提到"CSS 变量"但实现使用 Tailwind 类

     SUMMARY
     ─────────────────────────────
     关键问题：0
     警告：2
     准备归档：是（有警告）

     建议：
     1. 为系统首选项检测添加测试
     2. 更新 design.md 以反映 Tailwind 使用，或重构为使用 CSS 变量
```

**提示：**
- 在归档前运行以尽早捕获不匹配
     - 警告不阻止归档但指示潜在问题
     - 适合在提交前审查 AI 的工作
     - 可以揭示工件和实现之间的漂移

---

### `/opsx:sync`

**可选命令。** 将变更中的 delta 规范合并到主规范。归档会在需要时提示同步，因此你通常不需要手动运行此命令。

**语法：**
```
/opsx:sync [change-name]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `change-name` | 否 | 要同步的变更（如果未提供则从上下文推断） |

**它做什么：**
- 从变更文件夹读取 delta 规范
- 解析 ADDED/MODIFIED/REMOVED/RENAMED 章节
- 将更改合并到主 `openspec/specs/` 目录
- 保留 delta 中未提及的现有内容
- 不归档变更（保持活动）

**示例：**
```text
You: /opsx:sync

AI:  正在同步 add-dark-mode delta 规范...

     读取：openspec/changes/add-dark-mode/specs/ui/spec.md
     目标：  openspec/specs/ui/spec.md

     要应用的更改：
     ✓ ADDED：主题选择需求（2 个场景）
     ✓ ADDED：无障碍需求（1 个场景）

     正在合并...
     ✓ openspec/specs/ui/spec.md 已更新

     变更保持活动。准备好时运行 /opsx:archive 完成。
```

**何时手动使用：**

| 场景 | 使用同步？ |
|------|-----------|
| 长期变更，希望在归档前将规范放入主规范 | 是 |
| 多个并行变更需要更新的基础规范 | 是 |
| 想要单独预览/审查合并 | 是 |
| 快速变更，直接归档 | 否（归档处理） |

**提示：**
- 同步是智能的，不是复制粘贴
- 可以向现有需求添加场景而不重复
- 同步后变更保持活动（未归档）
- 大多数用户永远不需要直接调用此命令 —— 如果需要，归档会提示

---

### `/opsx:archive`

归档已完成的变更。完成变更并将其移动到归档文件夹。

**语法：**
```
/opsx:archive [change-name]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `change-name` | 否 | 要归档的变更（如果未提供则从上下文推断） |

**它做什么：**
- 检查工件完成状态
- 检查任务完成（如果不完整则警告）
- 如果尚未同步，则提供同步 delta 规范
- 将变更文件夹移动到 `openspec/changes/archive/YYYY-MM-DD-<name>/`
- 为审计跟踪保留所有工件

**示例：**
```text
You: /opsx:archive

AI:  正在归档 add-dark-mode...

     工件状态：
     ✓ proposal.md 存在
     ✓ specs/ 存在
     ✓ design.md 存在
     ✓ tasks.md 存在（8/8 任务完成）

     Delta 规范：尚未同步
     → 现在同步？（推荐）

You: 是

AI:  ✓ 已将规范同步到 openspec/specs/ui/spec.md
     ✓ 移动到 openspec/changes/archive/2025-01-24-add-dark-mode/

     变更归档成功。
```

**提示：**
- 归档不会因未完成的任务而阻止，但会警告
- Delta 规范可以在归档期间或之前同步
- 归档的更改保留用于历史
- 首先使用 `/opsx:verify` 捕获问题

---

### `/opsx:bulk-archive`

一次性归档多个已完成的变更。处理变更之间的规范冲突。

**语法：**
```
/opsx:bulk-archive [change-names...]
```

**参数：**
| 参数 | 必需 | 描述 |
|------|------|------|
| `change-names` | 否 | 要归档的特定变更（如果未提供则提示选择） |

**它做什么：**
- 列出所有已完成的变更
- 在归档之前验证每个变更
- 检测跨变更的规范冲突
- 通过检查实际实施的内容来解决冲突
- 按时间顺序归档

**示例：**
```
You: /opsx:bulk-archive

AI:  发现 3 个完成的变更：
     - add-dark-mode (8/8 任务完成)
     - fix-login-bug (3/3 任务完成)
     - update-footer (2/2 任务完成)

     检查规范冲突...
     ⚠ add-dark-mode 和 update-footer 都触及 specs/ui/

     检查代码库以解决...
     两个变更都已实现。将按时间顺序合并：
     1. add-dark-mode（创建于 1 月 20 日）
     2. update-footer（创建于 1 月 22 日）

     归档所有 3 个变更？

You: 是

AI:  ✓ 已归档 add-dark-mode
     ✓ 已归档 fix-login-bug
     ✓ 已归档 update-footer
     规范合并：add-dark-mode → update-footer
```

**提示：**
- 适合并行工作流
- 冲突解决是基于代理的（检查代码库）
- 变更按创建顺序归档
     - 在覆盖规范内容之前提示

---

### `/opsx:onboard`

通过完整的 OpenSpec 工作流进行引导入门。使用你的实际代码库的交互式教程。

**语法：**
```
/opsx:onboard
```

**它做什么：**
- 带着旁白完成完整的工作流周期
- 扫描你的代码库以查找实际改进机会
     - 创建一个具有真实工件的真正变更
     - 实施实际工作（小而安全的更改）
     - 归档已完成的变更
     - 解释每一步

**阶段：**
1. 欢迎和代码库分析
2. 寻找改进机会
3. 创建变更（`/opsx:new`）
4. 编写提案
5. 创建规范
6. 编写设计
7. 创建任务
8. 实施任务（`/opsx:apply`）
9. 验证实现
10. 归档变更
11. 总结和下一步

**示例：**
```
You: /opsx:onboard

AI:  欢迎使用 OpenSpec！

     我将使用你的实际代码库引导你完成完整的工作流。
     我们会找到一些小改进，为此创建一个适当的变更，
     实施它，并将其归档。

     让我扫描你的代码库寻找机会...

     [分析代码库]

     我发现了一些我们可以做的事情：
     1. 为联系表单添加输入验证
     2. 改进身份验证流程中的错误消息
     3. 为异步按钮添加加载状态

     哪个让你感兴趣？（或建议其他内容）
```

**提示：**
- 最适合学习工作流的新用户
- 使用真实代码，而不是玩具示例
- 创建一个你可以保留或丢弃的真正变更
     - 需要 15-30 分钟完成

---

## 不同 AI 工具的命令语法

不同的 AI 工具使用略有不同的命令语法。使用与你的工具匹配的格式：

| 工具 | 语法示例 |
|------|---------|
| Claude Code | `/opsx:propose`、`/opsx:apply` |
| Cursor | `/opsx-propose`、`/opsx-apply` |
| Windsurf | `/opsx-propose`、`/opsx-apply` |
| Copilot (IDE) | `/opsx-propose`、`/opsx-apply` |
| Trae | 基于技能的调用，如 `/openspec-propose`、`/openspec-apply-change`（不生成 `opsx-*` 命令文件） |

意图在所有工具中都是相同的，但命令的显示方式可能因集成而异。

> **注意：** GitHub Copilot 命令（`.github/prompts/*.prompt.md`）仅在 IDE 扩展（VS Code、JetBrains、Visual Studio）中可用。GitHub Copilot CLI 当前不支持自定义提示文件 — 有关详细信息和变通方法，请参阅[支持的工具](./supported-tools.md)。

---

## 旧命令

这些命令使用较旧的"一次性"工作流。它们仍然有效，但推荐使用 OPSX 命令。

| 命令 | 它做什么 |
|------|---------|
| `/openspec:proposal` | 一次性创建所有工件（proposal、specs、design、tasks） |
| `/openspec:apply` | 实施变更 |
| `/openspec:archive` | 归档变更 |

**何时使用旧命令：**
- 使用旧工作流的现有项目
- 不需要增量工件创建的简单更改
- 偏好全有或全无的方法

**迁移到 OPSX：**
可以使用 OPSX 命令继续旧变更。工件结构是兼容的。

---

## 故障排除

### "未找到变更"

命令无法识别要处理哪个变更。

**解决方案：**
- 明确指定变更名称：`/opsx:apply add-dark-mode`
- 检查变更文件夹是否存在：`openspec list`
- 验证你在正确的项目目录中

### "没有准备就绪的工件"

所有工件要么完成，要么被缺少的依赖项阻塞。

**解决方案：**
- 运行 `openspec status --change <name>` 以查看正在阻塞的内容
- 检查所需的工件是否存在
- 首先创建缺少的依赖工件

### "未找到模式"

指定的模式不存在。

**解决方案：**
- 列出可用模式：`openspec schemas`
- 检查模式名称的拼写
- 如果它是自定义的，则创建模式：`openspec schema init <name>`

### 命令未被识别

AI 工具无法识别 OpenSpec 命令。

**解决方案：**
- 确保 OpenSpec 已初始化：`openspec init`
- 重新生成技能：`openspec update`
- 检查 `.claude/skills/` 目录是否存在（对于 Claude Code）
- 重启你的 AI 工具以获取新技能

### 工件未正确生成

AI 创建不完整或不正确的工件。

**解决方案：**
- 在 `openspec/config.yaml` 中添加项目上下文
- 为特定指导添加每个工件的规则
     - 在更改描述中提供更多细节
- 使用 `/opsx:continue` 而不是 `/opsx:ff` 以获得更多控制

---

## 下一步

- [工作流程](./workflows.md) - 常见模式和何时使用每个命令
- [CLI 参考](./cli-reference.md) - 用于管理和验证的终端命令
- [自定义](./customization.md) - 创建自定义模式和工作流
