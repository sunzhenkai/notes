## ADDED Requirements

### Requirement: note-ask 命令定义

系统 SHALL 提供 `/note-ask` 命令（opencode command + skill），接收自然语言问题，在笔记库内检索相关内容并归纳总结作答。命令 MUST 指向 `note-ask` skill 文件，并在 command 层将所有输入（命令参数、对话正文、`@file`、URL）透传给 skill，不在 command 层重复 skill 逻辑。

#### Scenario: 命令透传输入给 skill

- **WHEN** 用户执行 `/note-ask 如何用 git worktree` 并附带正文或 `@file`
- **THEN** command 将问题与所有附加输入透传给 `note-ask` skill，由 skill 执行检索问答流程

#### Scenario: 无有效输入时追问

- **WHEN** 用户执行 `/note-ask` 但未提供任何问题或正文
- **THEN** 系统追问用户要查询什么内容，不直接作答

### Requirement: 索引优先的检索流程

系统 MUST 按以下顺序检索：①优先读取全局导航索引（`ingest/NAV-INDEX.md`）缩小候选范围；②读取候选目录的分目录索引（`README.md`/`index.md`）；③当索引不存在或不足以定位时，回退到 Grep/Glob 关键词搜索；④读取命中笔记的相关片段作为作答素材。

#### Scenario: 索引存在时优先使用索引

- **WHEN** 用户提问且 `ingest/NAV-INDEX.md` 存在
- **THEN** 系统先读全局导航索引定位候选目录，再读对应分目录索引，命中后再读取具体笔记片段

#### Scenario: 索引缺失时回退 Grep

- **WHEN** 全局导航索引不存在或未命中候选目录
- **THEN** 系统回退使用 Grep/Glob 按问题关键词搜索全库 Markdown 文件，并记录「索引缺失/过期」状态以提示后续

### Requirement: 归纳总结作答并强制引用

系统 MUST 在回答中对每个事实性结论标注至少一个引用的笔记相对路径。引用格式为 `（见 <相对路径>）`，路径保留仓库既有命名（含空格不转义）。纯通用常识可不引用，但 MUST 标注「库内未收录」。

#### Scenario: 命中笔记时引用路径作答

- **WHEN** 检索到与问题相关的笔记片段
- **THEN** 系统归纳总结片段后作答，且每条事实性结论附带引用的笔记相对路径

#### Scenario: 库内无相关内容

- **WHEN** 检索后未命中任何相关笔记
- **THEN** 系统如实声明「库内未找到相关内容」，不引入外部知识臆造，可建议用户运行 `/note-ingest` 补充

### Requirement: 检测索引过期并提示

系统 MUST 在检索时判断全局导航索引是否与实际库内容明显不符（如索引未收录的目录已存在大量笔记）。当判定索引过期时，系统 MUST 在回答末尾提示用户运行 `/note-index` 更新索引。

#### Scenario: 索引过期时提示更新

- **WHEN** 检索发现索引未覆盖的目录存在多份笔记
- **THEN** 系统正常作答（基于回退检索结果），并在末尾追加提示「索引可能过期，建议运行 /note-index 更新」

### Requirement: note-ask 为只读不写盘

系统 MUST 保证 `/note-ask` 不修改任何文件。检索、读取、作答全程只读，不创建或编辑笔记与索引。

#### Scenario: 问答过程不产生任何写操作

- **WHEN** 用户执行一次完整的 `/note-ask` 问答
- **THEN** 全程不调用任何写盘/编辑工具，不创建、修改、删除任何文件
