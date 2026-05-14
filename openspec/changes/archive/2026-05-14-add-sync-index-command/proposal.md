## Why

`README.md` 和 `index.html` 是本仓库的两个"门面"文件，承载着相同语义的内容（自我介绍、站点入口、链接、联系方式等），但格式不同——前者是 Markdown，后者是带 CSS 美化的独立 HTML。目前两者手动维护，已经出现描述不一致（如 wii.pub 的技术栈在 README 写的是 MdServe，在 index.html 写的是 Hexo）。每次修改 README.md 后需要手工同步 index.html，容易遗漏、出错。需要一个自动化的同步机制，利用 AI 语义理解能力，在 README.md 变更时精准更新 index.html。

## What Changes

- **新增** opencode 命令 `/sync-index`：检测 README.md 变更，通过 AI 分析 diff 语义，增量更新 index.html 对应区块
- **新增** 版本追踪机制：在 `.cache/readme-sync-state.json` 中保存 README.md 内容指纹，用于判断是否需要同步
- **新增** index.html 中的隐藏锚点注释（`<!-- sync:block:xxx -->`），为 AI 提供精确的映射目标
- **新增** 对 README.md 新增内容块的智能推断 + 人工确认流程，AI 按现有 HTML 样式创建新元素
- 非破坏性变更：不影响现有的 Markdown/HTML 手动编辑流程，锚点注释对浏览器完全不可见；备案号在任何操作下不得更改
- **新增** 双语内容处理：保留中英文内容，英文自动翻译为中文，优先展示中文

## Capabilities

### New Capabilities
- `sync-index-command`: opencode 命令，读取 README.md 的 git diff 或内容 diff，通过 AI 语义分析识别变更类型（文本更新、链接变更、结构变化、新增内容），将变更精准映射到 index.html 中的对应锚点区块，生成编辑计划并在人工确认后应用
- `version-tracking`: 基于内容哈希的版本追踪，在 `.cache/readme-sync-state.json` 中记录上次同步状态（README.md 的 SHA256 哈希、同步时间、缓存的 README 全文用于 diff 计算），支持首次初始化和后续增量同步

### Modified Capabilities
<!-- No existing capabilities are modified. -->

## Impact

- **新增文件**：`.opencode/commands/sync-index.md`（命令定义）、`.cache/readme-sync-state.json`（版本追踪状态，首次运行时自动创建）
- **修改文件**：`index.html`（注入 `<!-- sync:block:xxx -->` 和 `<!-- sync:item:xxx -->` 锚点注释）
- **可能修改**：`README.md`（可选，同步完成后更新 Front Matter 的 `update` 字段）
- **依赖**：依赖 opencode 的 AI 能力进行语义分析和 HTML 编辑，无需新增第三方库
- **与现有关联**：不改变现有 Makefile 或 mdserve 配置
