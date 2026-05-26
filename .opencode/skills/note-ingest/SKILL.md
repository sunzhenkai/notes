---
name: note-ingest
description: >-
  分析并归档笔记内容到仓库合适目录。用于 /note-ingest、整理文章/对话/剪贴内容、
  决定新建或合并 Markdown 文件、生成 front matter 与目录索引。
disable-model-invocation: true
---

# Note Ingest — 笔记归档

将外部或零散内容整理入库，写入合适目录。执行前 Read [taxonomy.md](taxonomy.md) 获取目录决策规则。

## Input

以下来源之一或组合（由 command 透传）：

- `/note-ingest` 后的命令参数
- 用户粘贴的正文
- `@filepath` 引用的文件
- URL（用 WebFetch 抓取）

无有效输入时，询问：

> 要归档什么内容？可粘贴正文、提供 URL，或 @ 引用文件。

---

## 工作流

复制 checklist 跟踪进度：

```
- [ ] 步骤 1：收集输入
- [ ] 步骤 2：理解内容
- [ ] 步骤 3：搜库 + 定位
- [ ] 步骤 4：生成归档计划（展示，不写盘）
- [ ] 步骤 5：人工确认
- [ ] 步骤 6：执行写入
```

### 步骤 1 — 收集输入

1. 合并 command 透传的所有输入为一份待归档正文
2. URL → WebFetch 抓取正文，保留原始 URL 供来源标注
3. `@file` → Read 文件；若本身是仓库内 md，确认用户是要**搬迁**还是**复制摘要**
4. 内容为空或过短（< 20 字且无 URL）→ 追问补充

### 步骤 2 — 理解内容

提取并记录：

| 字段 | 说明 |
|------|------|
| `topic` | 核心主题（1 句话） |
| `type` | 工具用法 / 学习笔记 / AI 工程 / 源码阅读 / 生活杂项 等 |
| `language` | 中文 / 英文 / 混合 |
| `is_external` | 是否外部文章（需来源 blockquote） |
| `source_url` | 原文链接（若有） |
| `source_title` | 原文标题（若有） |

整理风格参考：`ai coding/harness-engineering/`（README 索引 + 独立文章 + 来源标注）。

### 步骤 3 — 搜库 + 定位

1. 用 Grep/Glob 按 `topic` 关键词搜索已有文件/目录
2. 按 [taxonomy.md](taxonomy.md) 决策树确定目标目录
3. 选定动作：

| 动作 | 条件 |
|------|------|
| `append_section` | 目标目录已有 `usage.md` 或高度相关的同名主题文件 |
| `update_existing` | 用户明确要更新某文件，或内容与已有文件高度重叠 |
| `new_file` | 新主题、新工具目录、或独立长文 |

4. 确定目标路径与文件名（见 taxonomy 文件名惯例）

### 步骤 4 — 生成归档计划

**必须完整展示计划，禁止直接写盘。**

计划模板：

```markdown
## 归档计划

**动作**：new_file | append_section | update_existing
**目标路径**：`path/to/file.md`
**理由**：…

### Front matter 草案
（见下方模板）

### 正文结构预览
- H1 标题
- 来源 blockquote（若 is_external）
- 章节大纲 …

### 索引更新（若有）
- [ ] 更新 `同级/README.md` 的「进一步阅读」链接

### 相关已有文件
- `path/to/existing.md` — 关系说明
```

#### Front matter 模板

工具类（有 categories）：

```yaml
---
title: {标题}
categories:
  - 工具
  - {tool}
tags:
  - {tool}
date: "{ISO8601+08:00，新建用当前时间}"
update: "{ISO8601+08:00}"
---
```

主题/学习类：

```yaml
---
title: {标题}
categories:
  - {大类}
tags:
  - {标签}
date: "{ISO8601+08:00}"
update: "{ISO8601+08:00}"
---
```

索引 README（无 front matter 或极简）参照 `ai coding/harness-engineering/README.md`。

#### 外部文章来源块

```markdown
> 来源：[{source_title}]({source_url})
> 原文地址：<{source_url}>
```

#### 正文要求

- 用户可见内容优先简体中文；术语可保留英文
- 保留代码块、表格、链接结构
- 适当加 H2/H3，避免整墙文字
- 不臆造原文没有的技术细节

### 步骤 5 — 人工确认

展示计划后等待用户：

- **确认** → 步骤 6
- **修改路径/文件名** → 更新计划并再次展示
- **取消** → 终止，不写盘

`append_section` / `update_existing` 时展示 diff 预览（将追加/修改的段落），明确不会改动计划外内容。

### 步骤 6 — 执行写入

1. 创建目录（若不存在）
2. 写入或编辑 Markdown 文件
3. 若计划含索引更新：编辑同级 `README.md`，在「进一步阅读」或文末追加链接
4. 汇报：

```markdown
## 归档完成

- **路径**：`…`
- **动作**：…
- **摘要**：…

**后续建议**（按需提及）：
- 若修改了根 `README.md` 且需同步站点 → 运行 `/sync-index`
```

---

## Guardrails

- **不修改**：`index.html`、`openspec/`、`.cache/`、`.git/`、二进制文件
- **不覆盖**已有大段内容；合并只追加或精确替换用户确认的部分
- **外部文章**必须保留来源 URL
- **路径含空格**时保持仓库既有风格（`ai coding/`、`study record/`）
- **无确认不写盘**——步骤 4 与步骤 6 之间必须有用户确认
- 不确定分类时，在计划中列出 2 个候选路径供用户选择

---

## 示例

### 示例 A：外部 AI 工程长文 → 新建文件

```
Input: 粘贴一篇 Harness Engineering 译文 + URL

步骤 3: 搜到 ai coding/harness-engineering/ 已存在
动作: new_file → ai coding/harness-engineering/foo-bar-harness.md
步骤 4: 展示计划 + 提议更新 README.md 索引
步骤 5: 用户确认
步骤 6: 创建文件并更新 README
```

### 示例 B：Git 技巧片段 → 合并 usage.md

```
Input: 粘贴 git worktree 用法笔记

步骤 3: 存在 tools/git/usage.md
动作: append_section
步骤 4: 展示将追加的 ## git worktree 章节 diff
步骤 5: 用户确认
步骤 6: 追加到 usage.md，更新 front matter 的 update 字段
```
