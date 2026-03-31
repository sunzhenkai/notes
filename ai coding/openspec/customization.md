# 自定义

OpenSpec 提供三个级别的自定义：

| 级别 | 它做什么 | 最适合 |
|------|----------|------|
| **项目配置** | 设置默认值、注入上下文/规则 | 大多数团队 |
| **自定义模式** | 定义你自己的工作流工件 | 具有独特流程的团队 |
| **全局覆盖** | 在所有项目之间共享模式 | 高级用户 |

---

## 项目配置

`openspec/config.yaml` 文件是为你的团队自定义 OpenSpec 的最简单方法。它允许你：

- **设置默认模式** - 在每个命令上跳过 `--schema`
- **注入项目上下文** - AI 看到你的技术堆栈、约定等
- **添加每个工件规则** - 特定工件的自定义规则

### 快速设置

```bash
openspec init
```

这会引导你通过交互式创建配置。或手动创建一个：

```yaml
# openspec/config.yaml
schema: spec-driven

context: |
  Tech stack: TypeScript, React, Node.js, PostgreSQL
  API style: RESTful, documented in docs/api.md
  Testing: Jest + React Testing Library
  We value backwards compatibility for all public APIs

rules:
  proposal:
    - Include rollback plan
    - Identify affected teams
  specs:
    - Use Given/When/Then format
    - Reference existing patterns before inventing new ones
```

### 它如何工作

**默认模式：**

```bash
# 无配置
openspec new change my-feature --schema spec-driven

# 使用配置 - 模式是自动的
openspec new change my-feature
```

**上下文和规则注入：**

生成任何工件时，你的上下文和规则被注入到 AI 提示中：

```xml
<context>
Tech stack: TypeScript, React, Node.js, PostgreSQL
...
</context>

<rules>
- Include rollback plan
- Identify affected teams
</rules>

<template>
[模式的内置模板]
</template>
```

- **上下文** 出现在所有工件中
- **规则** 仅出现在匹配的工件中

### 模式解析顺序

当 OpenSpec 需要模式时，它按此顺序检查：

1. CLI 标志：`--schema <name>`
2. 变更元数据（变更文件夹中的 `.openspec.yaml`）
3. 项目配置（`openspec/config.yaml`）
4. 默认（`spec-driven`）

---

## 自定义 Schemas

当项目配置不够时，创建自己的模式并使用完全自定义的工作流。自定义模式位于你项目的 `openspec/schemas/` 目录中，并与你的代码一起版本控制。

```text
your-project/
├── openspec/
│   ├── config.yaml        # 项目配置
│   ├── schemas/           # 自定义模式位于此处
│   │   └── my-workflow/
│   │       ├── schema.yaml
│   │       └── templates/
│   └── changes/           # 你的变更
└── src/
```

### 复制现有模式

自定义的最快方法是复制内置模式：

```bash
openspec schema fork spec-driven my-workflow
```

这将整个 `spec-driven` 模式复制到 `openspec/schemas/my-workflow/`，你可以在其中自由编辑。

**你得到什么：**

```text
openspec/schemas/my-workflow/
├── schema.yaml           # 工作流定义
└── templates/
    ├── proposal.md       # 提案工件模板
    ├── spec.md           # 规范模板
    ├── design.md         # 设计模板
    └── tasks.md          # 任务模板
```

现在编辑 `schema.yaml` 以更改工作流，或编辑模板以更改 AI 生成的内容。

### 从头创建模式

对于完全新鲜的工作流：

```bash
# 交互式
openspec schema init research-first

# 非交互式
openspec schema init rapid \
  --description "Rapid iteration workflow" \
  --artifacts "proposal,tasks" \
  --default
```

### 模式结构

模式定义工作流中的工件及其依赖关系：

```yaml
# openspec/schemas/my-workflow/schema.yaml
name: my-workflow
version: 1
description: My team's custom workflow

artifacts:
  - id: proposal
    generates: proposal.md
    description: Initial proposal document
    template: proposal.md
    instruction: |
      创建一个解释为什么需要此更改的提案。
      专注于问题，而不是解决方案。
    requires: []

  - id: design
    generates: design.md
    description: Technical design
    template: design.md
    instruction: |
      创建一个解释如何实施的设计文档。
    requires:
      - proposal    # 不能在提案存在之前创建设计

  - id: tasks
    generates: tasks.md
    description: Implementation checklist
    template: tasks.md
    requires:
      - design

apply:
  requires: [tasks]
  tracks: tasks.md
```

**关键字段：**

| 字段 | 目的 |
|------|------|
| `id` | 唯一标识符，用于命令和规则 |
| `generates` | 输出文件名（支持 glob 如 `specs/**/*.md`） |
| `template` | `templates/` 目录中的模板文件 |
| `instruction` | 用于创建此工件的 AI 说明 |
| `requires` | 必须先存在的依赖工件 |

### 模板

模板是指导 AI 的 markdown 文件。创建该工件时，它们被注入到提示中。

```markdown
<!-- templates/proposal.md -->
## Why

<!-- 解释此更改的动机。这解决了什么问题？ -->

## What Changes

<!-- 描述将要改变什么。具体说明新功能或修改。 -->

## Impact

<!-- 受影响的代码、API、依赖项、系统 -->
```

模板可以包括：
- AI 应该填充的章节标题
- 具有 AI 指导的 HTML 注释
- 显示预期结构的示例格式

### 验证你的模式

在使用自定义模式之前，验证它：

```bash
openspec schema validate my-workflow
```

这检查：
- `schema.yaml` 语法正确
- 所有引用的模板存在
- 无循环依赖
- 工件 ID 有效

### 使用你的自定义模式

一旦创建，使用你的模式：

```bash
# 在命令上指定
openspec new change feature --schema my-workflow

# 或在 config.yaml 中设置为默认
schema: my-workflow
```

### 调试模式解析

不确定正在使用哪个模式？用以下方法检查：

```bash
# 查看特定模式从哪里解析
openspec schema which my-workflow

# 列出所有模式及其来源
openspec schema which --all
```

输出显示它是来自你的项目、用户目录还是包：

```text
Schema: my-workflow
Source: project
Path: /path/to/project/openspec/schemas/my-workflow
```

---

> **注意：** OpenSpec 还支持在 `~/.local/share/openspec/schemas/` 的用户级模式，用于跨项目共享，但推荐项目级模式在 `openspec/schemas/` 中，因为它们与你的代码版本控制。

---

## 示例

### 快速迭代工作流

用于快速迭代的最小工作流：

```yaml
# openspec/schemas/rapid/schema.yaml
name: rapid
version: 1
description: Fast iteration with minimal overhead

artifacts:
  - id: proposal
    generates: proposal.md
    description: Quick proposal
    template: proposal.md
    instruction: |
      为此更改创建一个简短的提案。
      专注于什么和为什么，跳过详细的规范。
    requires: []

  - id: tasks
    generates: tasks.md
    description: Implementation checklist
    template: tasks.md
    requires: [proposal]

apply:
  requires: [tasks]
  tracks: tasks.md
```

### 添加审查工件

复制默认值并添加审查步骤：

```bash
openspec schema fork spec-driven with-review
```

然后编辑 `schema.yaml` 以添加：

```yaml
  - id: review
    generates: review.md
    description: Pre-implementation review checklist
    template: review.md
    instruction: |
      基于设计创建审查清单。
      包括安全、性能和测试考虑。
    requires:
      - design

  - id: tasks
    # ... 现有任务配置 ...
    requires:
      - specs
      - design
      - review    # 现在任务也需要审查
```

---

## 另请参阅

- [CLI 参考：模式命令](./cli-reference.md#模式命令) - 完整命令文档
- [命令](./commands.md) - 斜杠命令
- [工作流程](./workflows.md) - 工作流模式
- [概念](./concepts.md) - 核心概念
