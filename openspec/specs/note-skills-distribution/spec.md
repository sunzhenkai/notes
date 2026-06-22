## Purpose

以 `.opencode/` 为 note-* skills/commands 的单一事实源，定义跨工具（cursor/codebuddy/qoder）的分发同步与 note-* 系列集成规范。

## Requirements

### Requirement: opencode 为单一事实源

系统 SHALL 以 `.opencode/` 为 note-* skills/commands 的唯一编辑源（single source of truth）。所有 note-* skill 与 command 内容 MUST 先在 `.opencode/` 编辑，再分发到其他工具目录。其余工具目录的 note-* 文件 MUST 视为只读副本。

#### Scenario: 编辑 note-* 只在 opencode 进行

- **WHEN** 任何 note-* skill/command 内容需要修改
- **THEN** 修改 MUST 发生在 `.opencode/skills/note-*/` 或 `.opencode/commands/note-*.md`，随后触发分发同步

### Requirement: 跨工具目录映射

系统 MUST 维护各工具 skills/commands 目录映射：opencode → `.opencode/`（源）；cursor → `.cursor/`；codebuddy → `.codebuddy/`；qoder → `.qoder/`（具体路径以各工具官方约定为准，实现时核对并固化）。每个目标工具 MUST 包含 `skills/` 与 `commands/` 两个子目录。

#### Scenario: 映射覆盖四个工具

- **WHEN** note-* 内容更新后执行同步
- **THEN** 系统将更新分发到 cursor、codebuddy、qoder 三个目标工具的对应 skills/commands 目录

### Requirement: 同步命令 note-sync

系统 MUST 提供同步入口（`/note-sync` 命令或 Makefile target `note-sync`），将 `.opencode/skills/note-*`（含子文件，如 `taxonomy.md`、`SKILL.md`）与 `.opencode/commands/note-*.md` 同步到三个目标工具目录。同步策略 MUST 为「仅覆盖 note-* 前缀的文件/目录」，不得触碰非 note 文件。

#### Scenario: 同步 note-* 到所有工具

- **WHEN** 用户执行 `/note-sync`（或 `make note-sync`）
- **THEN** 系统将所有 `.opencode/` 下 `note-*` 的 skill 与 command 复制到 cursor、codebuddy、qoder 对应目录，覆盖旧副本

#### Scenario: 同步不触碰非 note 文件

- **WHEN** 目标工具目录存在非 note 前缀文件（如 opsx-* 命令）
- **THEN** 同步 MUST 不修改、不删除这些文件

### Requirement: front matter 最小公共子集

note-* skill/command 的 front matter MUST 保持最小公共子集（`name`、`description`）以兼容四个工具。同步时若某工具需要额外字段或不同字段名，MUST 按适配规则转换，且不得丢失 `name`/`description`。

#### Scenario: 四工具 front matter 兼容

- **WHEN** 同步 note-* 到任一工具
- **THEN** 目标文件 front matter 至少包含 `name` 与 `description` 字段，保证该工具能正确识别 skill/command

### Requirement: note-ingest 与系列集成

note-ingest skill MUST 与 note-index、note-ask 形成系列集成：归档后（步骤 6 之后）MUST 增加索引联动步骤，提示用户更新相关索引；其步骤 3「搜库定位」MUST 优先读取 `ingest/NAV-INDEX.md` 缩小候选范围。note-* 系列的命名、检查清单、确认流程风格 MUST 保持一致。

#### Scenario: 归档后联动索引

- **WHEN** note-ingest 完成步骤 6 写入
- **THEN** 系统提示用户是否更新相关分目录索引与 `ingest/NAV-INDEX.md`（默认建议运行 `/note-index <目标目录>`），由用户确认后执行

#### Scenario: note-ingest 优先读全局索引定位

- **WHEN** note-ingest 执行步骤 3 搜库定位
- **THEN** 系统先读 `ingest/NAV-INDEX.md` 缩小候选目录，再 Grep 精确匹配目标路径

#### Scenario: 系列风格一致

- **WHEN** 检查 note-ingest / note-ask / note-index 三个 skill
- **THEN** 三者的命名、front matter 字段、检查清单格式、写盘前人工确认流程风格保持一致
