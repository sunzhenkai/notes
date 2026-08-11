---
name: note-ask
description: >-
  在笔记库内检索相关内容并归纳总结作答。用于 /note-ask、根据笔记回答问题、
  优先借助 note-index 索引定位、强制引用笔记路径、库内无内容时如实说明。
disable-model-invocation: true
---

# Note Ask — 笔记检索问答

针对用户问题，在笔记库内检索相关内容，归纳总结后作答。**全程只读，不写盘。**

## Input

以下来源之一或组合（由 command 透传）：

- `/note-ask` 后的问题（自然语言）
- 用户粘贴的正文/上下文
- `@filepath` 引用的文件
- URL（用 WebFetch 抓取，仅作为问题背景）

无有效输入时，询问：

> 要查什么？请描述你的问题，我会在笔记库内检索并作答。

---

## 工作流

复制 checklist 跟踪进度：

```
- [ ] 步骤 1：收集问题
- [ ] 步骤 2：索引优先定位
- [ ] 步骤 3：Grep 回退（索引不足时）
- [ ] 步骤 4：归纳总结作答
- [ ] 步骤 5：引用标注 + 过期提示
```

### 步骤 1 — 收集问题

1. 合并 command 透传的所有输入，提炼出**核心问题**（1 句话）
2. 提取检索关键词（中英文、术语、工具名等）
3. 无有效问题（空或 < 3 字）→ 追问补充

### 步骤 2 — 索引优先定位

1. 读取全局导航索引 `ingest/NAV-INDEX.md`
   - 若存在 → 按问题所属 taxonomy 顶层目录，定位候选目录
   - 读候选目录的分目录索引（`README.md`/`index.md`），缩小到具体笔记
2. 命中候选笔记 → 记录路径列表，进入步骤 4

### 步骤 3 — Grep 回退（索引不足时）

当索引不存在、未命中、或命中不足时，回退关键词搜索：

1. 用 Grep 按关键词搜索全库 Markdown（排除保护目录：`openspec/`、`.cache/`、`.git/`、`.opencode/node_modules/`、`node_modules/`）
2. 用 Glob 按工具名/主题名匹配目录与文件名
3. 读取命中文件的相关片段（标题、相关章节）
4. **记录索引状态**：若索引缺失或明显未覆盖命中目录 → 标记「索引过期」，步骤 5 提示更新

### 步骤 4 — 归纳总结作答

基于命中的笔记片段作答：

1. 综合多份片段，归纳总结成连贯回答（优先简体中文，术语可保留英文）
2. 保留代码块、命令、配置等关键细节
3. 不臆造原文没有的技术细节
4. 库内无任何相关内容 → 如实声明：「库内未找到与「{问题}」相关的内容」，可建议运行 `/note-ingest` 补充，**不引入外部知识编造**

### 步骤 5 — 引用标注 + 过期提示

#### 引用规则（强制）

回答中**每个事实性结论** MUST 标注至少一个引用的笔记相对路径，格式：

```
（见 ai coding/openspec/README.md）
```

- 路径为相对路径，**保留仓库既有命名（含空格不转义）**，如 `（见 study record/basic/index.md）`
- 多来源用顿号或换行分隔：`（见 tools/git/usage.md、tools/git/gitignore.md）`
- **纯通用常识**（如语言语法、公开标准）可不引用，但须标注「库内未收录」
- 整段回答末尾汇总「参考笔记」清单（去重，按相关性排序）

#### 索引过期提示

若步骤 3 标记了「索引过期」（`ingest/NAV-INDEX.md` 缺失，或索引未覆盖命中的目录且该目录含多份笔记），在回答末尾追加：

```
> ⚠️ 笔记索引可能过期，建议运行 /note-index 更新，以提升后续检索准确性。
```

---

## Guardrails

- **只读不写盘**：全程不调用 Write/Edit 等写盘工具，不创建、修改、删除任何文件
- **不臆造**：库内无相关内容时如实声明，不引入外部知识编造；引用必须对应真实存在的库内笔记
- **不触碰**：不读取/不修改 `index.html`、`openspec/`、`.cache/`、`.git/`、`.opencode/node_modules/`
- **路径原样**：引用路径保留空格（如 `ai coding/`），不转义、不改 kebab-case
- **与 sync-index 职责隔离**：本命令不处理 `README.md → index.html` 同步

---

## 示例

### 示例 A：命中笔记，归纳 + 引用作答

```
问题：git worktree 怎么用？

步骤 2: 读 ingest/NAV-INDEX.md → 命中 tools/git/
步骤 2: 读 tools/git/usage.md → 命中 git worktree 章节
步骤 4: 归纳用法作答

回答：
git worktree 用于在同一仓库下签出多个工作树……（见 tools/git/usage.md）

参考笔记：
- tools/git/usage.md
```

### 示例 B：索引缺失，Grep 回退 + 过期提示

```
问题：openspec 怎么用？

步骤 2: ingest/NAV-INDEX.md 不存在 → 回退
步骤 3: Grep "openspec" → 命中 ai coding/openspec/README.md
步骤 4: 归纳作答

回答：
OpenSpec 是……（见 ai coding/openspec/README.md）

> ⚠️ 笔记索引可能过期，建议运行 /note-index 更新……

参考笔记：
- ai coding/openspec/README.md
```

### 示例 C：库内无内容，如实声明

```
问题：Kubernetes Pod 调度算法细节

步骤 2-3: 检索无命中

回答：
库内未找到与「Kubernetes Pod 调度算法」相关的内容。如需补充，可运行 /note-ingest 归档相关资料。
```
