## Context

笔记库目前只有 `note-ingest`（归档写入）一个能力，且其 skill/command 以手工复制方式同时存在于 `.opencode/` 与 `.cursor/`（已验证两处内容完全一致）。现状的几个缺口：

- **只能写不能查**：内容归档后没有专门检索入口，提问只能临时 Grep，召回率和准确性不稳定。
- **没有索引**：库内仅零星存在 `study record/basic/index.md`、`computer science/engineering architecture/index.md`，无统一全局导航索引，AI 定位目标目录主要靠 `taxonomy.md` 的决策树 + 关键词搜索。
- **系列不闭环**：写入（ingest）与检索（ask）、维护（index）未成套，命名、检查清单、确认流程风格不统一。
- **分发靠手工复制**：`.cursor/` 是 `.opencode/` 的手工镜像，无同步保障；codebuddy、qoder 完全没有配置。

约束：
- 宿主为 opencode/cursor/codebuddy/qoder 等 AI 编码工具，能力以 skill/command 的 Markdown 指令形式存在，依赖各工具的 AI 执行。
- 仓库目录名含空格（`ai coding/`、`study record/`），路径风格须保持。
- 已有 `sync-index` 命令负责 `README.md → index.html`，与本变更职责不同，须互不干扰。

## Goals / Non-Goals

**Goals:**
- 补齐 note-ask、note-index 两个能力，与 note-ingest 组成「写 / 查 / 维护」闭环。
- note-index 维护「分目录索引 + 全局导航索引」两层结构，note-ask 与 note-ingest 均可读取定位。
- 统一 note-* 系列的命名、front matter、检查清单、确认流程风格。
- 建立 note-* 跨工具分发机制，以 opencode 为单一事实源，覆盖 cursor、codebuddy、qoder。

**Non-Goals:**
- 不做向量化/嵌入检索引擎，检索基于现有索引 + Grep/Glob 的关键词召回 + AI 语义归纳。
- 不修改 `index.html` 或接管 `sync-index` 的职责。
- 不自动触发（如 git hook），全部由用户对话式调用命令。
- 不改变仓库现有目录结构与命名风格。
- 本变更不为 note-ingest 单独新建 openspec spec（其与索引联动、风格统一的要求作为集成需求约束在新能力 spec 中）。

## Decisions

### D1: note-* 系列三命令闭环（ingest / ask / index）

**选型**：将笔记能力组织为三个对等命令——`note-ingest`（写入归档）、`note-ask`（检索问答）、`note-index`（索引维护），各自有独立 skill + command，共享一致的命名、front matter、检查清单、确认流程风格。
**替代方案**：合并为单一 mega-command（如 `/note` 带子命令）。被拒绝原因：单文件过长、关注点混杂，且各工具 command 触发更直观。
**闭环关系**：ingest 写入后触发/提示 index 更新；ask 优先读 index 定位；index 维护的对象也被 ingest 的「搜库+定位」步骤复用。

### D2: note-ask 检索策略——索引优先 + Grep 回退 + 智能总结 + 强制引用

**选型**：note-ask 执行「①读全局导航索引缩小范围 → ②读候选目录分索引/文件 → ③不足时 Grep/Glob 回退 → ④归纳总结作答 → ⑤每条结论标注引用的笔记相对路径」。库内无相关内容时如实声明，不引入外部知识臆造。
**替代方案 A**：纯 Grep 关键词匹配。被拒绝原因：无索引时召回噪声大、定位慢。
**替代方案 B**：引入向量检索。被拒绝原因：超出当前工具栈，维护成本高（见 Non-Goals）。
**引用要求**：回答中出现的每个事实性结论 MUST 附带至少一个笔记路径引用（如 `（见 ai coding/openspec/README.md）`）；纯通用常识（如语言语法）可不引用但须标注「库内未收录」。

### D3: note-index 两层索引结构

**选型**：维护两层：
1. **分目录索引**：对有内容的目录生成/更新 `README.md`（主题目录，含概述 + 文章链接 + 摘要）或 `index.md`（工具/学习目录，含条目列表），沿用 `ai coding/harness-engineering/README.md` 既有风格。
2. **全局导航索引**：单一全局文件，按 taxonomy 顶层分类聚合所有分目录索引入口 + 一句话摘要，供 note-ask / note-ingest 快速定位。

**替代方案**：仅分目录索引，无全局文件。被拒绝原因：note-ask 需扫描多个 README 才能定位，效率低、易漏。

### D4: 全局导航索引的位置与格式

**选型**：全局导航索引放 `ingest/NAV-INDEX.md`（`ingest/` 目录已存在且语义上属于笔记库的元数据/工作区）。
**格式**：按 taxonomy 顶层目录分组的链接树，每条目 = `相对路径` + 标题 + 一句话摘要（取自分目录索引或文件首段）。带 front matter（`title: 笔记导航索引`、`categories: [关于]`）。
**替代方案 A**：放仓库根目录 `INDEX.md`。被拒绝原因：根目录是门面区，且会与 `index.html` 概念混淆。
**替代方案 B**：放 `.opencode/` 内。被拒绝原因：索引是笔记内容资产，不应藏在工具配置目录；且 codebuddy/qoder 可能不识别 `.opencode/`。
**权衡**：`ingest/` 已有内容，复用该目录减少新增顶层路径。

### D5: note-ingest ↔ note-index 联动

**选型**：在 note-ingest 步骤 6（执行写入）后增加「步骤 7：索引联动」——提示用户是否更新相关分目录索引与全局导航索引（默认调用 note-index 的增量逻辑，仍需人工确认）。
**替代方案**：归档即自动写索引。被拒绝原因：与 note-ingest「无确认不写盘」一致原则冲突。
**复用**：note-ingest 步骤 3「搜库+定位」改为优先读 `ingest/NAV-INDEX.md` 缩小范围，再 Grep 精确匹配。

### D6: 跨工具分发——opencode 为单一事实源 + 同步命令

**选型**：以 `.opencode/` 为唯一编辑源，定义各工具目录映射：

| 工具 | skills 目录 | commands 目录 | 备注 |
|------|------------|--------------|------|
| opencode | `.opencode/skills/` | `.opencode/commands/` | 源 |
| cursor | `.cursor/skills/` | `.cursor/commands/` | 已存在，沿用 |
| codebuddy | `.codebuddy/skills/` | `.codebuddy/commands/` | 新建（路径以工具实际约定为准，实现时确认） |
| qoder | `.qoder/skills/` | `.qoder/commands/` | 新建（路径以工具实际约定为准，实现时确认） |

提供同步命令 `/note-sync`（或 Makefile target `note-sync`）：将 `.opencode/skills/note-*` 与 `.opencode/commands/note-*.md` 复制到其余三个工具目录，保证内容一致。同步策略为整目录覆盖（note-* 前缀的文件）。
**替代方案**：各工具独立维护。被拒绝原因：内容易漂移（现状 cursor 即手工镜像，无保障）。
**适配差异**：若某工具 front matter 字段不同（如 cursor skill 用 `description`、opencode 用 `name`+`description`），在同步时按适配规则转换；note-* 的 front matter 字段保持最小公共子集（`name`、`description`）。

### D7: 写盘前人工确认（全系列一致）

**选型**：note-index 与 note-ingest 一样执行「生成计划 → 展示 → 人工确认 → 写盘」四段式，note-ask 为只读不写盘故无需确认。note-index 的增量更新基于已有索引比对，仅展示 diff。
**理由**：与现有 note-ingest 一致原则对齐，避免索引被误改。

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| 全局索引与实际笔记内容漂移（归档后忘更新） | note-ingest 步骤 7 默认提示联动 note-index；note-ask 检测索引过期时可建议运行 note-index |
| 分目录索引命名 `README.md` vs `index.md` 混乱 | note-index skill 明确规则：主题目录用 `README.md`，工具/学习目录优先沿用已有命名（`index.md`/`README.md`/`usage.md`），无则新建 `README.md` |
| 跨工具目录路径与 codebuddy/qoder 实际约定不符 | D6 标注「实现时确认」；首次同步前核对各工具官方目录约定，必要时在同步命令中做路径映射 |
| note-ask 引用路径因含空格难以复制 | 引用统一用相对路径并保留空格（与仓库风格一致），不做转义 |
| 索引文件被误纳入 `sync-index` 处理范围 | `sync-index` 仅处理根 `README.md → index.html`；note-index 产物在子目录与 `ingest/`，互不重叠 |
| 同步命令覆盖工具目录时丢失工具专属调整 | 同步只覆盖 `note-*` 前缀文件，非 note 文件不动；front matter 保持最小公共子集 |

## Open Questions

- codebuddy、qoder 的 skills/commands 目录约定需在实现阶段核对官方文档确认（D6 已标注）。
- 全局导航索引是否需要生成可点击的 HTML 版本？当前 Non-Goal，仅维护 Markdown；如未来需要可由独立命令处理，不复用 `sync-index`。
