---
name: note-index
description: >-
  维护笔记库的两层索引：分目录索引（README.md/index.md）与全局导航索引（ingest/NAV-INDEX.md）。
  用于 /note-index、扫描笔记生成/更新索引、供 note-ask 检索与 note-ingest 定位读取。
disable-model-invocation: true
---

# Note Index — 笔记索引维护

维护笔记库「分目录索引 + 全局导航索引」两层结构，供 `/note-ask` 检索定位、`/note-ingest` 归档定位读取。**写盘前必须人工确认。**

## Input

- `/note-index` 后的范围参数（可选）：
  - 子目录路径，如 `tools/git`、`ai coding/` —— 仅扫描该范围
  - 省略或 `--all` —— 全库扫描
- 由 command 透传，无范围参数时默认全库

---

## 工作流

复制 checklist 跟踪进度：

```
- [ ] 步骤 1：解析范围
- [ ] 步骤 2：扫描笔记
- [ ] 步骤 3：生成索引更新计划（展示，不写盘）
- [ ] 步骤 4：人工确认
- [ ] 步骤 5：执行写盘
```

### 步骤 1 — 解析范围

1. 解析范围参数：子目录路径 → 仅扫描该目录及子目录；省略/`--all` → 全库
2. 确定扫描根目录与排除集合（见 Guardrails 保护区域）

### 步骤 2 — 扫描笔记

1. 用 Glob 列出范围内所有 `*.md` 文件（排除保护区域）
2. 对每个目录归类：是否为「主题目录」（含多篇文章）或「工具/学习目录」（条目列表）
3. 读取每个 Markdown 文件提取索引要素：
   - **标题**：front matter `title`，否则首个 H1，否则文件名
   - **摘要**：文件首段（H1/概述后的第一段），或 front matter 描述，限一句话
4. 跳过本身是索引的文件（`README.md`/`index.md`/`usage.md` 作为索引载体时，不作为被索引条目）

### 步骤 3 — 生成索引更新计划

**必须完整展示计划，禁止直接写盘。**

#### 分目录索引命名规则

| 目录类型 | 索引文件 | 说明 |
|---------|---------|------|
| 主题目录（多篇文章） | `README.md` | 概述 + 文章链接列表 + 摘要 |
| 工具/学习目录 | **沿用已有**（`index.md`/`README.md`/`usage.md`），无则新建 `README.md` | 不重命名既有文件 |
| 单文件目录 | 不强制建索引 | 内容少时全局索引直接指向该文件 |

#### 分目录索引内容结构

```markdown
# {目录主题名}

> {一句话概述该目录主题}（可选，主题目录建议）

## 文章 / 条目

- [{标题}]({相对路径}) — {一句话摘要}
- [{标题}]({相对路径}) — {一句话摘要}
```

- 链接用**相对路径**（相对仓库根，如 `tools/git/gitignore.md`）
- 摘要限一句话，取自文件首段或 front matter
- 保留人工编写的概述段落（增量更新时见步骤「增量更新逻辑」）

#### 全局导航索引（`ingest/NAV-INDEX.md`）

按 taxonomy 顶层目录分组聚合所有分目录索引入口：

```markdown
---
title: 笔记导航索引
categories:
  - 关于
tags:
  - 索引
date: "{ISO8601+08:00，首次创建用当前时间}"
update: "{ISO8601+08:00}"
---

# 笔记导航索引

> 本索引由 /note-index 维护，供 /note-ask 检索与 /note-ingest 定位读取。请勿手动大幅改动结构，可补充摘要。

## 工具（tools/）

- [git](tools/git/README.md) — Git 用法与技巧
- [vim](tools/vim/README.md) — Vim 编辑器配置与操作

## AI 编程（ai coding/）

- [Harness Engineering](ai%20coding/harness-engineering/README.md) — AI Agent 约束与质量保障工程
- [OpenSpec](ai%20coding/openspec/README.md) — 规格驱动开发流程

## 研习录（study record/）
...
```

- 分组顺序参照 [taxonomy.md](../note-ingest/taxonomy.md) 顶层目录映射
- 含空格的路径在 Markdown 链接中用 `%20` 转义（仅链接 URL 部分，显示文字不变）
- 每条目 = 分目录索引入口的相对路径 + 标题 + 一句话摘要
- 无分目录索引的目录，可直接指向代表性文件

#### 增量更新逻辑

- **比对已有索引与实际笔记**：仅追加新增条目、修正变化条目、移除已删除条目
- **保留未变化内容**与**人工编写段落**（如概述、blockquote 来源）—— 不做全量重写
- 全局索引：仅更新变化目录对应的分组段落，保留其余分组与人工补充

#### 计划模板

```markdown
## 索引更新计划

**范围**：{全库 | tools/git/}

### 分目录索引
| 动作 | 路径 | 说明 |
|------|------|------|
| new_file | tools/git/README.md | 新建，3 个条目 |
| update | ai coding/harness-engineering/README.md | 追加 1 条目 |
| skip | study record/basic/index.md | 沿有，无变化 |

### 全局导航索引
- ingest/NAV-INDEX.md：{首次创建 | 更新 tools/、ai coding/ 分组}

### diff 预览
（展示将新增/修改的具体段落）
```

### 步骤 4 — 人工确认

展示计划与 diff 预览后等待用户：

- **确认** → 步骤 5
- **修改范围/条目** → 更新计划并再次展示
- **取消** → 终止，不写盘

### 步骤 5 — 执行写盘

1. 创建目录（若不存在）
2. 写入或编辑分目录索引文件（Write 新建 / Edit 增量更新）
3. 写入或编辑 `ingest/NAV-INDEX.md`
4. 汇报：

```markdown
## 索引更新完成

- **范围**：…
- **分目录索引**：新建 X 个，更新 Y 个，跳过 Z 个
- **全局索引**：ingest/NAV-INDEX.md（{首次创建|已更新}）

**后续建议**：
- 运行 /note-ask 验证检索准确性
- 归档新内容后运行 /note-index 增量更新
```

---

## Guardrails

- **保护区域（不写入索引，不作为条目）**：`index.html`、`openspec/`、`.cache/`、`.git/`、`.opencode/node_modules/`、`node_modules/`、二进制文件
- **全局索引唯一落点**：`ingest/NAV-INDEX.md`，不在其他位置创建全局索引
- **不重命名**既有索引文件（`index.md`/`README.md`/`usage.md`），只增量更新
- **无确认不写盘**——步骤 3 与步骤 5 之间必须有人工确认
- **不触碰 `index.html`**：本命令与 `sync-index`（README→index.html）职责不同，互不干扰
- **链接相对路径**：分目录索引与全局索引的链接均为相对仓库根的路径
- **路径含空格**：保留仓库既有风格（`ai coding/`、`study record/`），Markdown 链接 URL 部分用 `%20` 转义

---

## 示例

### 示例 A：首次全库扫描，创建全局索引

```
范围：--all

步骤 2: 扫描全库，识别 tools/、ai coding/、study record/ 等目录
步骤 3: 计划 = 新建多个分目录 README + 首次创建 ingest/NAV-INDEX.md
步骤 4: 用户确认
步骤 5: 写盘，汇报「全局索引首次创建」
```

### 示例 B：指定子目录增量更新

```
范围：tools/git

步骤 2: 扫描 tools/git/，发现新增 gitignore.md
步骤 3: 计划 = update tools/git/README.md（追加 1 条目）+ update ingest/NAV-INDEX.md（tools/ 分组无变化则跳过）
步骤 4: 展示追加的 diff
步骤 5: 增量写入
```
