---
description: 将内容整理归档到笔记库合适位置
---

# /note-ingest

将外部或零散内容整理入库，写入仓库合适目录。

**第一步（必须）**：Read 并严格遵循 `note-ingest` skill（`.cursor/skills/note-ingest/SKILL.md`）。定位目录时 Read [taxonomy.md](.cursor/skills/note-ingest/taxonomy.md)。

**Input**：以下全部透传给 skill 作为 Input：

- `/note-ingest` 后的命令参数
- 用户在对话中粘贴的正文
- `@` 引用的文件
- 提供的 URL

无有效输入时，按 skill 步骤 1 询问用户。

**禁止**：在未 Read skill 前自行推断 workflow；不要在 command 层重复 skill 中的步骤逻辑。
