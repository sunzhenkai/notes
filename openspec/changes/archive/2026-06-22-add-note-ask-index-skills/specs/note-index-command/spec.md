## ADDED Requirements

### Requirement: note-index 命令定义

系统 SHALL 提供 `/note-index` 命令（opencode command + skill），维护笔记库的「分目录索引 + 全局导航索引」两层结构。命令 MUST 指向 `note-index` skill 文件，并透传范围参数（可选：子目录路径或 `--all` 表示全库）。默认范围为全库。

#### Scenario: 指定子目录范围

- **WHEN** 用户执行 `/note-index tools/git`
- **THEN** 系统仅扫描并更新 `tools/git/` 及其相关索引条目，不动其他目录索引

#### Scenario: 默认全库范围

- **WHEN** 用户执行 `/note-index` 不带参数
- **THEN** 系统扫描全库 Markdown 文件并维护两层索引

### Requirement: 分目录索引维护

系统 MUST 为有内容的目录生成或更新分目录索引。命名规则：主题目录用 `README.md`（含概述 + 文章链接 + 摘要）；工具/学习目录优先沿用已有命名（`index.md`/`README.md`/`usage.md`），无索引文件时新建 `README.md`。索引内容 MUST 包含目录内条目的标题、相对链接与一句话摘要。

#### Scenario: 主题目录生成 README 索引

- **WHEN** 某主题目录含多篇文章且无 `README.md`
- **THEN** 系统为其新建 `README.md`，列出每篇文章的标题、相对链接与摘要

#### Scenario: 工具目录沿用已有索引命名

- **WHEN** 工具目录已有 `index.md`（如 `study record/basic/index.md`）
- **THEN** 系统沿用 `index.md` 增量更新，不新建 `README.md`，不重命名既有文件

#### Scenario: 已有索引做增量更新

- **WHEN** 目录已有索引且内容与实际笔记不一致
- **THEN** 系统比对差异，仅追加/修正变化的条目，保留未变化内容与人工编写段落

### Requirement: 全局导航索引维护

系统 MUST 维护单一全局导航索引文件 `ingest/NAV-INDEX.md`，按 taxonomy 顶层目录分组聚合所有分目录索引入口，每条目为相对路径 + 标题 + 一句话摘要。文件 MUST 带 front matter（`title: 笔记导航索引`、`categories: [关于]`）。

#### Scenario: 生成全局导航索引

- **WHEN** 全库扫描完成
- **THEN** 系统按 taxonomy 顶层目录（tools / ai coding / artificial intelligence / study record / basic programming / computer science / play / others）分组写入 `ingest/NAV-INDEX.md`，每目录下列出其分目录索引入口与摘要

#### Scenario: 全局索引增量更新

- **WHEN** `ingest/NAV-INDEX.md` 已存在且仅部分目录变化
- **THEN** 系统仅更新变化目录对应的分组段落，保留其余分组与人工补充内容

### Requirement: 写盘前人工确认

系统 MUST 在写盘前展示索引更新计划（新增/修改的索引文件清单 + diff 预览），等待用户确认后才写盘。禁止未确认直接写盘。

#### Scenario: 展示计划并确认

- **WHEN** 系统完成索引比对生成更新计划
- **THEN** 系统展示待新增/修改的索引文件列表与 diff 预览，等待用户「确认 / 修改范围 / 取消」

#### Scenario: 用户取消

- **WHEN** 用户在确认环节选择取消
- **THEN** 系统终止，不写任何索引文件

### Requirement: 索引产物可被 note-ask 与 note-ingest 读取

系统 MUST 保证生成的索引（分目录索引 + `ingest/NAV-INDEX.md`）可被 `/note-ask` 检索定位与 `/note-ingest` 归档定位读取。索引格式 MUST 为标准 Markdown，链接为相对路径。

#### Scenario: note-ask 读取全局索引定位

- **WHEN** `/note-ask` 执行检索
- **THEN** 系统能读取 `ingest/NAV-INDEX.md` 获取目录分组与入口链接，作为定位起点

#### Scenario: note-ingest 读取全局索引定位

- **WHEN** `/note-ingest` 执行步骤 3 搜库定位
- **THEN** 系统能读取 `ingest/NAV-INDEX.md` 缩小候选目录范围，再 Grep 精确匹配

### Requirement: 保护区域不写入

系统 MUST NOT 向 `index.html`、`openspec/`、`.cache/`、`.git/`、`.opencode/node_modules/` 写入索引，MUST NOT 修改二进制文件。全局导航索引仅写入 `ingest/NAV-INDEX.md`。

#### Scenario: 跳过保护区域

- **WHEN** 扫描遇到 `openspec/`、`index.html` 等保护路径
- **THEN** 系统跳过这些路径，不为其生成或更新索引
