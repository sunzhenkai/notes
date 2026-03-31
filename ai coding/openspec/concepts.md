# 核心概念

本指南解释了 OpenSpec 的核心思想以及它们如何组合在一起。有关实际用法，请参阅[入门指南](./getting-started.md)和[工作流程](./workflows.md)。

## 哲学

OpenSpec 围绕四个原则构建：

```
流式而非僵化       — 无阶段门控，做有意义的事情
迭代而非瀑布       — 边构建边学习，边进行边完善
简单而非复杂       — 轻量级设置，最小化仪式
棕地优先           — 适用于现有代码库，而不仅是绿地
```

### 这些原则为什么重要

**流式而非僵化。** 传统的规范系统将你锁定在阶段中：先规划，然后实施，然后完成。OpenSpec 更灵活 —— 你可以以对你有意义的方式以任何顺序创建工件。

**迭代而非瀑布。** 需求会变化。理解会加深。一开始看起来像是好的方法在看到代码库之后可能无法成立。OpenSpec 拥抱这个现实。

**简单而非复杂。** 一些规范框架需要大量设置、严格的格式或重量级流程。OpenSpec 不会妨碍你。在几秒钟内初始化，立即开始工作，仅在需要时自定义。

**棕地优先。** 大多数软件工作不是从零开始的 —— 它是修改现有系统。OpenSpec 的基于 delta 的方法使得指定对现有行为的更改变得容易，而不仅仅是描述新系统。

## 全局图景

OpenSpec 将你的工作组织成两个主要区域：

```
┌─────────────────────────────────────────────────────────────────┐
│                        openspec/                                 │
│                                                                  │
│   ┌─────────────────────┐      ┌──────────────────────────────┐ │
│   │       specs/        │      │         changes/              │ │
│   │                     │      │                               │ │
│   │  Source of truth    │◄─────│  Proposed modifications       │ │
│   │  How your system    │ merge│  Each change = one folder     │ │
│   │  currently works    │      │  Contains artifacts + deltas  │ │
│   │                     │      │                               │ │
│   └─────────────────────┘      └──────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Specs** 是信息源 —— 它们描述了系统当前的行为。

**Changes** 是提议的修改 —— 它们存在于单独的文件夹中，直到你准备好合并它们。

这种分离是关键。你可以并行处理多个变更而不冲突。你可以在变更影响主规范之前审查它。当你归档变更时，其 deltas 会干净地合并到信息源中。

## 规范

规范使用结构化的需求和场景描述系统的行为。

### 结构

```
openspec/specs/
├── auth/
│   └── spec.md           # 身份验证行为
├── payments/
│   └── spec.md           # 支付处理
├── notifications/
│   └── spec.md           # 通知系统
└── ui/
    └── spec.md           # UI 行为和主题
```

按域组织规范 —— 对你的系统有意义的逻辑分组。常见模式：

- **按功能区域**：`auth/`、`payments/`、`search/`
- **按组件**：`api/`、`frontend/`、`workers/`
- **按有界上下文**：`ordering/`、`fulfillment/`、`inventory/`

### 规范格式

规范包含需求，每个需求都有场景：

```markdown
# Auth 规范

## Purpose
应用程序的身份验证和会话管理。

## Requirements

### Requirement: 用户身份验证
成功登录后，系统应颁发 JWT 令牌。

#### Scenario: 有效凭据
- Given 拥有有效凭据的用户
- When 用户提交登录表单
- Then 返回 JWT 令牌
- And 用户被重定向到仪表板

#### Scenario: 无效凭据
- Given 无效凭据
- When 用户提交登录表单
- Then 显示错误消息
- And 不颁发令牌

### Requirement: 会话过期
系统应在 30 分钟不活动后使会话过期。

#### Scenario: 空闲超时
- Given 已认证的会话
- When 30 分钟没有活动
- Then 会话失效
- And 用户必须重新认证
```

**关键元素：**

| 元素 | 目的 |
|------|------|
| `## Purpose` | 此规范域的高级描述 |
| `### Requirement:` | 系统必须具有的特定行为 |
| `#### Scenario:` | 需求在行动中的具体示例 |
| SHALL/MUST/SHOULD | RFC 2119 关键词，指示需求强度 |

### 为什么这样构建规范

**需求是"什么"** —— 它们说明系统应该做什么，而不指定实现。

**场景是"何时"** —— 它们提供可以验证的具体示例。好的场景：
- 可测试（你可以为它们编写自动化测试）
- 覆盖快乐路径和边缘情况
- 使用 Given/When/Then 或类似的结构化格式

**RFC 2119 关键词**（SHALL、MUST、SHOULD、MAY）传达意图：
- **MUST/SHALL** — 绝对要求
- **SHOULD** — 推荐，但存在例外
- **MAY** — 可选

### 规范是什么（以及不是什么）

规范是**行为契约**，不是实施计划。

好的规范内容：
- 用户或下游系统依赖的可观察行为
- 输入、输出和错误条件
- 外部约束（安全、隐私、可靠性、兼容性）
- 可以测试或显式验证的场景

避免在规范中：
- 内部类/函数名
- 库或框架选择
- 逐步实施细节
- 详细的执行计划（这些属于 `design.md` 或 `tasks.md`）

快速测试：
- 如果实现可以在不改变外部可见行为的情况下更改，则它可能不属于规范。

### 保持轻量：渐进式严谨

OpenSpec 旨在避免官僚主义。使用使变更可验证的最轻量级级别。

**轻量规范（默认）：**
- 短的行为优先需求
- 清晰的范围和非目标
- 几个具体的验收检查

**完整规范（针对更高风险）：**
- 跨团队或跨存储库更改
- API/契约更改、迁移、安全/隐私关注
- 模糊性可能导致昂贵返工的更改

大多数更改应保持在轻量模式。

### 人类 + 代理协作

在许多团队中，人类探索并代理起草工件。预期的循环是：

1. 人类提供意图、上下文和约束。
2. 代理将其转换为行为优先的需求和场景。
3. 代理将实施细节保留在 `design.md` 和 `tasks.md` 中，而不是 `spec.md`。
4. 验证在实施之前确认结构和清晰度。

这使得规范对人类可读，对代理一致。

## 变更

变更是对系统的提议修改，打包为包含理解和实施它所需的所有内容的文件夹。

### 变更结构

```
openspec/changes/add-dark-mode/
├── proposal.md           # 为什么和什么
├── design.md             # 如何（技术方法）
├── tasks.md              # 实施清单
├── .openspec.yaml        # 变更元数据（可选）
└── specs/                # Delta 规范
    └── ui/
        └── spec.md       # ui/spec.md 中的更改
```

每个变更都是自包含的。它有：
- **工件** — 捕获意图、设计和任务的文档
- **Delta 规范** — 指示正在添加、修改或删除什么的规范
- **元数据** — 此特定变更的可选配置

### 为什么变更是文件夹

将变更打包为文件夹有几个好处：

1. **所有内容在一起。** 提案、设计、任务和规范都在一个地方。无需在不同位置搜索。

2. **并行工作。** 多个变更可以同时存在而不冲突。在 `fix-auth-bug` 也在进行的同时处理 `add-dark-mode`。

3. **干净的历史。** 归档时，变更移动到 `changes/archive/` 并保留其完整上下文。你可以回头了解不仅改变了什么，还有为什么。

4. **审查友好。** 变更文件夹易于审查 —— 打开它，阅读提案，检查设计，查看规范 deltas。

## 工件

工件是变更中指导工作的文档。

### 工件流程

```
proposal ──────► specs ──────► design ──────► tasks ──────► implement
    │               │             │              │
   为什么          什么          如何           步骤
 + 范围           更改         方法           采取
```

工件相互构建。每个工件为下一个提供上下文。

### 工件类型

#### Proposal（`proposal.md`）

提案在高层次上捕获**意图**、**范围**和**方法**。

```markdown
# Proposal: 添加暗模式

## Intent
用户要求提供暗模式选项，以减少夜间使用时的眼睛疲劳并匹配系统首选项。

## Scope
范围内：
- 设置中的主题切换
- 系统首选项检测
- 在 localStorage 中持久化首选项

范围外：
- 自定义颜色主题（未来工作）
- 每页主题覆盖

## Approach
使用 CSS 自定义属性进行主题设置，使用 React 上下文进行状态管理。首次加载时检测系统首选项，允许手动覆盖。
```

**何时更新提案：**
- 范围变更（缩小或扩展）
- 意图澄清（更好地理解问题）
- 方法根本转变

#### Specs（`specs/` 中的 delta 规范）

Delta 规范描述**相对于当前规范正在改变什么**。请参阅下面的 [Delta Specs](#delta-specs)。

#### Design（`design.md`）

设计捕获**技术方法**和**架构决策**。

````markdown
# Design: 添加暗模式

## Technical Approach
通过 React Context 管理主题状态以避免 prop drilling。CSS 自定义属性支持运行时切换而无需类切换。

## Architecture Decisions

### Decision: Context over Redux
使用 React Context 进行主题状态，因为：
- 简单的二进制状态（明/暗）
- 无复杂的状态转换
- 避免添加 Redux 依赖

### Decision: CSS 自定义属性
使用 CSS 变量而不是 CSS-in-JS，因为：
- 与现有样式表一起工作
- 无运行时开销
- 浏览器原生解决方案

## Data Flow
```
ThemeProvider (context)
       │
       ▼
ThemeToggle ◄──► localStorage
       │
       ▼
CSS Variables (applied to :root)
```

## File Changes
- `src/contexts/ThemeContext.tsx`（新）
- `src/components/ThemeToggle.tsx`（新）
- `src/styles/globals.css`（修改）
````

**何时更新设计：**
- 实现显示方法不起作用
- 发现更好的解决方案
- 依赖项或约束发生变化

#### Tasks（`tasks.md`）

任务是**实施清单** —— 带有复选框的具体步骤。

```markdown
# Tasks

## 1. 主题基础设施
- [ ] 1.1 创建带有明暗状态的 ThemeContext
- [ ] 1.2 添加颜色的 CSS 自定义属性
- [ ] 1.3 实现 localStorage 持久化
- [ ] 1.4 添加系统首选项检测

## 2. UI 组件
- [ ] 2.1 创建 ThemeToggle 组件
- [ ] 2.2 将切换添加到设置页面
- [ ] 2.3 更新 Header 以包含快速切换

## 3. 样式
- [ ] 3.1 定义暗主题调色板
- [ ] 3.2 更新组件以使用 CSS 变量
- [ ] 3.3 测试对比度以实现无障碍
```

**任务最佳实践：**
- 在标题下对相关任务进行分组
- 使用分层编号（1.1、1.2 等）
- 保持任务足够小，以便在一个会话中完成
     - 完成任务时勾选它们

## Delta 规范

Delta 规范是使 OpenSpec 适用于棕地开发的关键概念。它们描述**正在改变什么**而不是重述整个规范。

### 格式

```markdown
# Auth 的 Delta

## ADDED Requirements

### Requirement: 双因素认证
系统必须支持基于 TOTP 的双因素认证。

#### Scenario: 2FA 注册
- Given 未启用 2FA 的用户
- When 用户在设置中启用 2FA
- Then 显示用于身份验证器应用程序设置的 QR 码
- And 用户必须在激活之前通过代码验证

#### Scenario: 2FA 登录
- Given 启用了 2FA 的用户
- When 用户提交有效凭据
- Then 显示 OTP 挑战
     - And 仅在有效 OTP 后登录完成

## MODIFIED Requirements

### Requirement: 会话过期
系统应在 15 分钟不活动后使会话过期。
（之前：30 分钟）

#### Scenario: 空闲超时
- Given 已认证的会话
- When 15 分钟没有活动
- Then 会话失效

## REMOVED Requirements

### Requirement: 记住我
（已弃用，改用 2FA。用户应每次重新认证。）
```

### Delta 章节

| 章节 | 含义 | 归档时发生什么 |
|------|------|----------------|
| `## ADDED Requirements` | 新行为 | 附加到主规范 |
| `## MODIFIED Requirements` | 改变的行为 | 替换现有需求 |
| `## REMOVED Requirements` | 弃用的行为 | 从主规范中删除 |

### 为什么使用 Delta 而非完整规范

**清晰度。** Delta 显示 exactly 正在改变什么。阅读完整规范，你必须与当前版本进行心理差异。

**避免冲突。** 两个变更可以触及相同的规范文件而不冲突，只要它们修改不同的需求。

**审查效率。** 审查者看到变更，而不是未更改的上下文。专注于重要内容。

**棕地适配。** 大多数工作修改现有行为。Deltas 使修改成为一等公民，而不是事后诸葛亮。

## Schemas

模式定义工作流的工件类型及其依赖关系。

### Schemas 如何工作

```yaml
# openspec/schemas/spec-driven/schema.yaml
name: spec-driven
artifacts:
  - id: proposal
    generates: proposal.md
    requires: []              # 无依赖关系，可以先创建

  - id: specs
    generates: specs/**/*.md
    requires: [proposal]      # 创建规范之前需要提案

  - id: design
    generates: design.md
    requires: [proposal]      # 可以与规范并行创建

  - id: tasks
    generates: tasks.md
    requires: [specs, design] # 首先需要规范和设计
```

**工件形成依赖关系图：**

```
                    proposal
                   (根节点)
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
      specs                       design
   (requires:                  (requires:
    proposal)                   proposal)
         │                           │
         └─────────────┬─────────────┘
                       │
                       ▼
                    tasks
                (requires:
                specs, design)
```

**依赖关系是赋能者，而不是门控。** 它们显示可以创建什么，而不是必须下一步创建什么。如果不需要，你可以跳过设计。你可以在设计之前或之后创建规范 —— 两者都只依赖于提案。

### 内置 Schemas

**spec-driven**（默认）

规范驱动开发的标准工作流：

```
proposal → specs → design → tasks → implement
```

最适合：大多数你想要在实施之前就规范达成一致的功能工作。

### 自定义 Schemas

为你的团队工作流创建自定义模式：

```bash
# 从头创建
openspec schema init research-first

# 或复制现有的
openspec schema fork spec-driven research-first
```

**自定义模式示例：**

```yaml
# openspec/schemas/research-first/schema.yaml
name: research-first
artifacts:
  - id: research
    generates: research.md
    requires: []           # 先做研究

  - id: proposal
    generates: proposal.md
    requires: [research]   # 提案由研究告知

  - id: tasks
    generates: tasks.md
    requires: [proposal]   # 跳过规范/设计，直接进入任务
```

请参阅[自定义](./customization.md)了解创建和使用自定义模式的完整详细信息。

## 归档

归档通过将其 delta 规范合并到主规范并为历史记录保存变更来完成变更。

### 归档时发生什么

```

Before archive:

openspec/
├── specs/
│   └── auth/
│       └── spec.md ◄────────────────┐
└── changes/                         │
    └── add-2fa/                     │
        ├── proposal.md              │
        ├── design.md                │ merge
        ├── tasks.md                 │
        └── specs/                   │
            └── auth/                │
                └── spec.md ─────────┘


After archive:

openspec/
├── specs/
│   └── auth/
│       └── spec.md        # 现在包括 2FA 需求
└── changes/
    └── archive/
        └── 2025-01-24-add-2fa/    # 为历史记录保留
            ├── proposal.md
            ├── design.md
            ├── tasks.md
            └── specs/
                └── auth/
                    └── spec.md
```

### 归档过程

1. **合并 deltas。** 每个 delta 规范章节（ADDED/MODIFIED/REMOVED）应用于相应的主规范。

2. **移动到归档。** 变更文件夹移动到带有日期前缀的 `changes/archive/` 以进行按时间顺序排序。

3. **保留上下文。** 所有工件在归档中保持完整。你可以随时回头了解做出变更的原因。

### 为什么归档很重要

**干净的状态。** 活动变更（`changes/`）仅显示进行中的工作。已完成的工作移出路径。

**审计轨迹。** 归档保留每个变更的完整上下文 —— 不仅改变了什么，还有解释为什么的提案、解释如何的设计，以及显示工作的任务。

**规范演进。** 当归档变更时，规范有机地增长。每个归档合并其 deltas，随时间建立全面的规范。

## 一切如何组合在一起

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OPENSPEC FLOW                                   │
│                                                                              │
│   ┌────────────────┐                                                         │
│   │  1. START      │  /opsx:propose (core) or /opsx:new (expanded)          │
│   │     CHANGE     │                                                         │
│   └───────┬────────┘                                                         │
│           │                                                                  │
│           ▼                                                                  │
│   ┌────────────────┐                                                         │
│   │  2. CREATE     │  /opsx:ff or /opsx:continue (expanded workflow)         │
│   │     ARTIFACTS  │  Creates proposal → specs → design → tasks              │
│   │                │  (based on schema dependencies)                         │
│   └───────┬────────┘                                                         │
│           │                                                                  │
│           ▼                                                                  │
│   ┌────────────────┐                                                         │
│   │  3. IMPLEMENT  │  /opsx:apply                                            │
│   │     TASKS      │  Work through tasks, checking them off                  │
│   │                │◄──── Update artifacts as you learn                      │
│   └───────┬────────┘                                                         │
│           │                                                                  │
│           ▼                                                                  │
│   ┌────────────────┐                                                         │
│   │  4. VERIFY     │  /opsx:verify (optional)                                │
│   │     WORK       │  Check implementation matches specs                     │
│   └───────┬────────┘                                                         │
│           │                                                                  │
│           ▼                                                                  │
│   ┌────────────────┐     ┌──────────────────────────────────────────────┐   │
│   │  5. ARCHIVE    │────►│  Delta specs merge into main specs           │   │
│   │     CHANGE     │     │  Change folder moves to archive/             │   │
│   └────────────────┘     │  Specs are now the updated source of truth   │   │
│                          └──────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**良性循环：**

1. 规范描述当前行为
2. 变更提议修改（作为 deltas）
3. 实施使更改成为现实
4. 归档将 deltas 合并到规范中
5. 规范现在描述新的行为
6. 下一个变更建立在更新的规范之上

## 术语表

| 术语 | 定义 |
|------|------|
| **工件** | 变更中的文档（proposal、design、tasks 或 delta 规范） |
| **归档** | 完成变更并将其 deltas 合并到主规范的过程 |
| **变更** | 对系统的提议修改，打包为带有工件的文件夹 |
| **Delta 规范** | 描述相对于当前规范的更改（ADDED/MODIFIED/REMOVED）的规范 |
| **域** | 规范的逻辑分组（例如 `auth/`、`payments/`） |
| **需求** | 系统必须具有的特定行为 |
| **场景** | 需求的具体示例，通常在 Given/When/Then 格式中 |
| **模式** | 工件类型及其依赖关系的定义 |
| **规范** | 描述系统行为的规范，包含需求和场景 |
| **信息源** | `openspec/specs/` 目录，包含当前一致同意的行为 |

## 下一步

- [入门指南](./getting-started.md) - 实用的第一步
- [工作流程](./workflows.md) - 常见模式和何时使用每个
- [命令](./commands.md) - 完整命令参考
- [自定义](./customization.md) - 创建自定义模式
