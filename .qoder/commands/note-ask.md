---
description: 在笔记库内检索相关内容并归纳总结作答
---

# /note-ask

针对问题，在笔记库内检索相关内容并归纳总结作答。全程只读，不写盘。

**第一步（必须）**：Read 并严格遵循 `note-ask` skill（`.opencode/skills/note-ask/SKILL.md`）。

**Input**：以下全部透传给 skill 作为 Input：

- `/note-ask` 后的问题或命令参数
- 用户在对话中粘贴的正文/上下文
- `@` 引用的文件
- 提供的 URL（仅作为问题背景）

无有效输入时，按 skill 步骤 1 询问用户。

**禁止**：在未 Read skill 前自行推断 workflow；不要在 command 层重复 skill 中的检索/作答逻辑。
