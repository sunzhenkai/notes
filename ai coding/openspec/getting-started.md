# 入门指南

本指南解释了在安装和初始化 OpenSpec 之后的工作原理。关于安装说明，请参阅[主 README](./README.md)。

## OpenSpec 如何工作

OpenSpec 帮助你和你的 AI 编程助手在编写任何代码之前就对要构建的内容达成一致。

**默认快速路径（核心配置）：**

```text
/opsx:propose ──► /opsx:apply ──► /opsx:archive
```

**扩展路径（自定义工作流选择）：**

```text
/opsx:new ──► /opsx:ff 或 /opsx:continue ──► /opsx:apply ──► /opsx:verify ──► /opsx:archive
```

默认的全局配置是 `core`，它包含 `propose`、`explore`、`apply` 和 `archive`。你可以使用 `openspec config profile` 然后运行 `openspec update` 来启用扩展的工作流命令。

## OpenSpec 创建的内容

运行 `openspec init` 后，你的项目将具有以下结构：

```
openspec/
├── specs/              # 信息源（系统的行为）
│   └── <domain>/
│       └── spec.md
├── changes/            # 提议的更新（每个变更一个文件夹）
│   └── <change-name>/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       └── specs/      # Delta 规范（正在改变什么）
│           └── <domain>/
│               └── spec.md
└── config.yaml         # 项目配置（可选）
```

**两个关键目录：**

- **`specs/`** - 信息源。这些规范描述了系统当前的行为。按域组织（例如 `specs/auth/`、`specs/payments/`）。

- **`changes/`** - 提议的修改。每个变更都有自己的文件夹，包含所有相关的工件。当变更完成后，其规范会合并到主 `specs/` 目录中。

## 理解工件

每个变更文件夹都包含指导工作的工件：

| 工件 | 目的 |
|------|------|
| `proposal.md` | "为什么"和"什么" - 捕获意图、范围和方法 |
| `specs/` | Delta 规范，显示添加/修改/删除的需求 |
| `design.md` | "如何" - 技术方法和架构决策 |
| `tasks.md` | 带有复选框的实现清单 |

**工件相互构建：**

```
proposal ──► specs ──► design ──► tasks ──► implement
   ▲           ▲          ▲                    │
   └───────────┴──────────┴────────────────────┘
            在学习时更新
```

你可以在实现过程中随时回到早期工件并完善它们。

## Delta 规范如何工作

Delta 规范是 OpenSpec 的关键概念。它们显示了相对于当前规范正在改变什么。

### 格式

Delta 规范使用章节来指示变更类型：

```markdown
# Auth 的 Delta

## ADDED Requirements

### Requirement: 双因素认证
系统必须在登录期间要求第二个因素。

#### Scenario: OTP 必需
- Given 一个启用了 2FA 的用户
- When 用户提交有效凭据
- Then 显示 OTP 挑战

## MODIFIED Requirements

### Requirement: 会话超时
系统应在 30 分钟不活动后使会话过期。
（之前：60 分钟）

#### Scenario: 空闲超时
- Given 一个已认证的会话
- When 30 分钟没有活动
- Then 会话失效

## REMOVED Requirements

### Requirement: 记住我
（已弃用，改用 2FA）
```

### 归档时发生什么

当你归档变更时：

1. **ADDED** 需求附加到主规范
2. **MODIFIED** 需求替换现有版本
3. **REMOVED** 需求从主规范中删除

变更文件夹移动到 `openspec/changes/archive/` 用于审计历史。

## 示例：你的第一个变更

让我们通过添加暗模式来演示。

### 1. 开始变更（默认）

```text
You: /opsx:propose add-dark-mode

AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md — 为什么要这样做，正在改变什么
     ✓ specs/       — 需求和场景
     ✓ design.md    — 技术方法
     ✓ tasks.md     — 实现清单
     准备好实施！
```

如果你启用了扩展的工作流配置，你也可以分两步进行：`/opsx:new` 然后 `/opsx:ff`（或 `/opsx:continue` 增量进行）。

### 2. 创建的内容

**proposal.md** - 捕获意图：

```markdown
# Proposal: 添加暗模式

## Intent
用户要求提供暗模式选项，以减少夜间使用时的眼睛疲劳。

## Scope
- 在设置中添加主题切换
- 支持系统首选项检测
- 在 localStorage 中持久化首选项

## Approach
使用 CSS 自定义属性进行主题设置，使用 React 上下文进行状态管理。
```

**specs/ui/spec.md** - 显示新需求的 Delta：

```markdown
# UI 的 Delta

## ADDED Requirements

### Requirement: 主题选择
系统应允许用户在明暗主题之间选择。

#### Scenario: 手动切换
- Given 用户在任何页面上
- When 用户点击主题切换
- Then 主题立即切换
- And 首选项在会话之间持久化

#### Scenario: 系统首选项
- Given 没有保存首选项的用户
- When 应用程序加载
- Then 使用系统的首选配色方案
```

**tasks.md** - 实现清单：

```markdown
# Tasks

## 1. 主题基础设施
- [ ] 1.1 创建带有明暗状态的 ThemeContext
- [ ] 1.2 添加颜色的 CSS 自定义属性
- [ ] 1.3 实现 localStorage 持久化

## 2. UI 组件
- [ ] 2.1 创建 ThemeToggle 组件
- [ ] 2.2 将切换添加到设置页面
- [ ] 2.3 更新 Header 以包含快速切换

## 3. 样式
- [ ] 3.1 定义暗主题调色板
- [ ] 3.2 更新组件以使用 CSS 变量
```

### 3. 实施

```
You: /opsx:apply

AI:  正在完成任务...
     ✓ 1.1 创建了带有明暗状态的 ThemeContext
     ✓ 1.2 将 CSS 自定义属性添加到 globals.css
     ✓ 1.3 实现了 localStorage 持久化
     ✓ 2.1 创建了 ThemeToggle 组件
     ...
     所有任务完成！
```

在实施过程中，如果你发现设计需要调整，只需更新工件并继续。

### 4. 归档

```
You: /opsx:archive

AI:  正在归档 add-dark-mode...
     ✓ 将规范合并到 openspec/specs/ui/spec.md
     ✓ 移动到 openspec/changes/archive/2025-01-24-add-dark-mode/
     完成！准备下一个功能。
```

你的 delta 规范现在是主规范的一部分，记录了你的系统如何工作。

## 验证和审查

使用 CLI 检查你的变更：

```bash
# 列出活动变更
openspec list

# 查看变更详情
openspec show add-dark-mode

# 验证规范格式
openspec validate add-dark-mode

# 交互式仪表板
openspec view
```

## 下一步

- [工作流程](./workflows.md) - 常见模式和何时使用每个命令
- [命令](./commands.md) - 所有斜杠命令的完整参考
- [概念](./concepts.md) - 深入了解规范、变更和模式
- [自定义](./customization.md) - 让 OpenSpec 按你的方式工作
