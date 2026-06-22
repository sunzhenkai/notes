---
description: 将 note-* skills/commands 从 opencode 同步到 cursor/codebuddy/qoder
---

# /note-sync

以 `.opencode/` 为单一事实源，将 `note-*` 系列 skills 与 commands 同步到 cursor、codebuddy、qoder 三个工具目录，保证行为一致。

## 执行

1. **运行同步**：执行 `make note-sync`（Makefile target 完成实际复制）
2. **汇报结果**：列出每个工具目录接收到的 skills（目录）与 commands（文件）

## 单一事实源与映射

| 工具 | skills 目录 | commands 目录 | 角色 |
|------|------------|--------------|------|
| opencode | `.opencode/skills/` | `.opencode/commands/` | **源（唯一编辑入口）** |
| cursor | `.cursor/skills/` | `.cursor/commands/` | 只读副本 |
| codebuddy | `.codebuddy/skills/` | `.codebuddy/commands/` | 只读副本 |
| qoder | `.qoder/skills/` | `.qoder/commands/` | 只读副本 |

> 四个工具均遵循 Agent Skills 标准（`SKILL.md` + front matter `name`/`description`），目录映射源自各工具官方文档。

## 同步策略

- **仅覆盖 `note-*` 前缀**：只复制 `.opencode/skills/note-*/`（含 `SKILL.md`、`taxonomy.md` 等子文件）与 `.opencode/commands/note-*.md`
- **不触碰非 note 文件**：`opsx-*`、`sync-index.md` 等其他 skills/commands 不受影响
- **整目录覆盖**：目标工具的 `note-*` skill 目录先清除再复制，避免残留已删除的文件
- **front matter 最小公共子集**：`note-*` 的 front matter 保持 `name`+`description`（+`disable-model-invocation`）以兼容四个工具，同步时不改写

## 约定

- **所有 note-* 内容修改 MUST 在 `.opencode/` 进行**，修改后运行 `/note-sync`（或 `make note-sync`）分发
- 其余工具目录的 note-* 文件视为只读副本，不直接编辑
