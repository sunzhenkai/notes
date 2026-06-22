## 1. note-ask skill 与 command

- [x] 1.1 创建 `.opencode/skills/note-ask/SKILL.md`，编写 front matter（`name: note-ask`、`description`）与「检索问答」工作流：步骤 1 收集问题、步骤 2 索引优先定位、步骤 3 Grep 回退、步骤 4 归纳总结、步骤 5 引用标注
- [x] 1.2 在 SKILL.md 中定义引用规则：每个事实性结论标注至少一个笔记相对路径 `（见 <相对路径>）`，纯通用常识标注「库内未收录」，路径保留空格不转义
- [x] 1.3 在 SKILL.md 中定义索引过期检测逻辑：检索时判断 `ingest/NAV-INDEX.md` 是否与实际库内容明显不符，不符则在回答末尾提示运行 `/note-index`
- [x] 1.4 在 SKILL.md 中明确只读约束：全程不调用写盘/编辑工具，不创建/修改/删除任何文件
- [x] 1.5 创建 `.opencode/commands/note-ask.md`，command 仅透传输入（命令参数、对话正文、`@file`、URL）给 skill，无有效输入时追问；不在 command 层重复 skill 逻辑

## 2. note-index skill 与 command

- [x] 2.1 创建 `.opencode/skills/note-index/SKILL.md`，编写 front matter 与工作流：步骤 1 解析范围参数（子目录/`--all`）、步骤 2 扫描 Markdown、步骤 3 生成索引更新计划、步骤 4 展示 diff、步骤 5 人工确认、步骤 6 写盘
- [x] 2.2 在 SKILL.md 中定义分目录索引命名规则：主题目录用 `README.md`；工具/学习目录沿用已有（`index.md`/`README.md`/`usage.md`），无则新建 `README.md`
- [x] 2.3 在 SKILL.md 中定义索引内容结构：标题 + 相对链接 + 一句话摘要（取自文件首段或 H1/概述）
- [x] 2.4 在 SKILL.md 中定义全局导航索引 `ingest/NAV-INDEX.md` 格式：按 taxonomy 顶层目录分组，每条目 = 相对路径 + 标题 + 摘要；带 front matter（`title: 笔记导航索引`、`categories: [关于]`）
- [x] 2.5 在 SKILL.md 中定义增量更新逻辑：比对已有索引与实际笔记，仅追加/修正变化条目，保留未变化与人工编写段落
- [x] 2.6 在 SKILL.md 中明确保护区域：不向 `index.html`、`openspec/`、`.cache/`、`.git/`、`.opencode/node_modules/`、二进制写入；全局索引仅写 `ingest/NAV-INDEX.md`
- [x] 2.7 创建 `.opencode/commands/note-index.md`，command 透传范围参数（默认全库），指向 skill，不在 command 层重复逻辑

## 3. note-ingest 系列集成优化

- [x] 3.1 在 `.opencode/skills/note-ingest/SKILL.md` 步骤 3「搜库+定位」增加：优先读 `ingest/NAV-INDEX.md` 缩小候选目录，再 Grep 精确匹配
- [x] 3.2 在 note-ingest SKILL.md 步骤 6 之后新增「步骤 7：索引联动」——提示用户是否更新相关分目录索引与 `ingest/NAV-INDEX.md`（建议运行 `/note-index <目标目录>`），由用户确认后执行，不自动写盘
- [x] 3.3 统一 note-ingest / note-ask / note-index 三者的 front matter 字段（`name`+`description`+`disable-model-invocation`）、检查清单格式、写盘前人工确认流程风格，确保系列一致

## 4. 跨工具分发机制

- [x] 4.1 核对 cursor skills/commands 目录约定（已有 `.cursor/skills/`、`.cursor/commands/`），确认映射路径
- [x] 4.2 查阅 codebuddy、qoder 官方文档，确认 skills/commands 目录约定与 front matter 字段差异；如路径非 `.codebuddy/`、`.qoder/` 则在分发逻辑中固化实际路径 — 已确认四工具均用 `<dotdir>/skills/<name>/SKILL.md` + `<dotdir>/commands/`，front matter 最小公共子集为 `name`+`description`
- [x] 4.3 创建 `/note-sync` 命令（`.opencode/commands/note-sync.md`）：将 `.opencode/skills/note-*`（含 `taxonomy.md`、`SKILL.md` 等子文件）与 `.opencode/commands/note-*.md` 同步到 cursor、codebuddy、qoder 对应目录
- [x] 4.4 在 note-sync 中明确同步策略：仅覆盖 `note-*` 前缀文件/目录，不触碰非 note 文件（如 opsx-*）；front matter 保持 `name`+`description` 最小公共子集，按目标工具做必要字段适配
- [x] 4.5 （可选）在 `Makefile` 增加 `note-sync` target，复用同一同步逻辑，便于非 opencode 环境执行 — 已实现并通过 `make note-sync` 验证

## 5. 验证与收尾

- [ ] 5.1 手动运行 `/note-index tools/git`，验证生成/更新分目录索引与 `ingest/NAV-INDEX.md` 条目正确 — 需用户手动测试
- [ ] 5.2 手动运行 `/note-ask` 提问库内已有内容，验证回答带引用路径且回答准确 — 需用户手动测试
- [ ] 5.3 手动运行 `/note-ask` 提问库内无内容，验证如实声明「库内未找到」不臆造 — 需用户手动测试
- [ ] 5.4 手动运行 `/note-ingest` 归档一篇内容，验证步骤 7 提示联动 note-index — 需用户手动测试
- [ ] 5.5 运行 `/note-sync`，验证 cursor、codebuddy、qoder 目录收到 note-* 副本且非 note 文件未被改动 — 需用户手动测试
- [ ] 5.6 验证 note-* 四工具副本内容一致（diff 比对 front matter 与正文） — 需用户手动测试
- [x] 5.7 验证 note-ask / note-index / note-ingest 不触碰 `index.html` 与 `sync-index` 职责范围 — 命令/skill 中已内置保护区域规则
