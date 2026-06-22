---
description: 维护笔记库两层索引（分目录 + 全局导航），供 note-ask/note-ingest 定位
---

# /note-index

维护笔记库「分目录索引（README.md/index.md）+ 全局导航索引（ingest/NAV-INDEX.md）」两层结构。

**第一步（必须）**：Read 并严格遵循 `note-index` skill（`.opencode/skills/note-index/SKILL.md`）。

**Input（范围参数，透传给 skill）**：

- `/note-index <子目录>` —— 仅扫描该目录及子目录，如 `/note-index tools/git`
- `/note-index` 或 `/note-index --all` —— 全库扫描（默认）

**禁止**：在未 Read skill 前自行推断 workflow；不要在 command 层重复 skill 中的索引生成/确认逻辑。
