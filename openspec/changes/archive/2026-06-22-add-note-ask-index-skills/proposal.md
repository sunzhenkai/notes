## Why

笔记库已有 `note-ingest`（归档写入）能力，但缺少配套的「检索问答」与「索引维护」能力，三者无法形成闭环：内容写进库后难以被快速提问检索，也没有统一索引供 AI 定位，全靠逐文件 Grep，召回率与准确性不稳。同时 `note-ingest` 目前仅在 opencode 与 cursor 两处以手工复制方式存在，路径/约定分散，codebuddy、qoder 等工具无法直接使用。需要补齐 note-* 系列（ask/index）并建立跨工具分发机制，让笔记能力在 cursor、opencode、codebuddy、qoder 中一致可用。

## What Changes

- **新增** opencode skill + command `/note-ask`：在笔记库内做语义检索，将相关片段归纳总结后作答，并在回答中标注引用的笔记路径；找不到相关内容时如实说明，不臆造。读取 note-index 维护的索引以提升定位准确性。
- **新增** opencode skill + command `/note-index`：维护「分目录索引 + 全局导航索引」两层结构——为有内容的目录生成/更新 `README.md` 或 `index.md`（标题、链接、摘要），并生成/更新全局导航索引供 note-ask 与 note-ingest 快速定位。
- **优化** 现有 `note-ingest`：统一 note-* 系列命名、front matter、检查清单风格；note-ingest 在归档后调用/提示更新相关索引，与 note-index 形成联动。
- **新增** note-* 跨工具分发机制：以 `.opencode/` 为单一事实源，建立向 cursor（`.cursor/`）、codebuddy、qoder 同步分发 skills/commands 的约定与脚本/命令，保证 4 个工具中 note-* 行为一致。
- 非破坏性变更：不影响现有笔记内容、`index.html`、`sync-index` 命令。

## Capabilities

### New Capabilities

- `note-ask-command`: 笔记库内检索 + 智能总结问答命令。接收自然语言问题，优先借助 note-index 索引定位候选笔记，读取相关片段，归纳总结作答并引用笔记路径；库内无相关内容时如实声明，不引入外部知识臆造。
- `note-index-command`: 笔记索引维护命令。维护两层索引：分目录 `README.md`/`index.md`（标题、链接、摘要）与全局导航索引文件；支持扫描指定范围（子目录或全库）、增量更新（基于已有索引比对）、人工确认后写盘。供 note-ask 检索、note-ingest 归档定位读取。
- `note-skills-distribution`: note-* 系列 skills/commands 的跨工具分发机制。以 opencode 为单一事实源，定义 cursor/codebuddy/qoder 的目录映射与文件适配规则，提供同步命令/脚本保证 4 个工具中 note-* 行为一致。

### Modified Capabilities

<!-- note-ingest 当前无对应 spec（openspec/specs/ 下不存在），其与索引联动、命名一致性的要求将在上述新能力的 spec 中以集成需求形式约束。 -->

## Impact

- **新增文件**：
  - `.opencode/skills/note-ask/SKILL.md`、`.opencode/commands/note-ask.md`
  - `.opencode/skills/note-index/SKILL.md`（含索引生成规则）、`.opencode/commands/note-index.md`
  - note-* 分发约定与同步命令/脚本（位置见 design）
- **修改文件**：
  - `.opencode/skills/note-ingest/SKILL.md`：补充「归档后更新索引/联动 note-index」「统一系列风格」步骤
  - 跨工具镜像目录 `.cursor/`（及新建的 codebuddy/qoder 目录）：note-* 同步副本
- **可能新增**：全局导航索引文件（位置与命名见 design 决策）
- **依赖**：依赖宿主工具的 AI 检索/编辑能力，无需新增第三方库
- **与现有关联**：与 `sync-index`（README→index.html 同步）职责不同，互不干扰；note-index 的全局索引独立于 index.html
