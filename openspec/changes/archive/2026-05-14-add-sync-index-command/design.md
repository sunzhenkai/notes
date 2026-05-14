## Context

当前仓库有两个"门面"文件：`README.md`（Markdown 格式，用于 GitHub 和 mdserve 展示）和 `index.html`（独立 HTML 页面，带 CSS 美化，作为 landing page）。两者承载相同语义内容（简介、站点入口、链接、联系方式），但手动维护导致不一致。需要建立一个基于 AI 语义理解的自动化同步机制。

约束条件：
- 运行在 opencode 环境中，AI 可用
- `index.html` 有手工打磨的 CSS 样式和 HTML 结构，不能完全从模板生成
- 用户希望增量更新（保留手工调整），而非全量重新生成
- 仓库已在 GitHub 上，`git diff` 可用

## Goals / Non-Goals

**Goals:**
- 实现 `/sync-index` opencode 命令，让用户对话式触发 README.md → index.html 的同步
- 通过内容哈希追踪 README.md 变更状态，避免重复同步
- 使用隐藏 HTML 锚点注释实现精确的区块级映射
- 存量变更（文本、链接修改）自动处理；增量变更（新增内容块）AI 推断 + 人工确认
- 保留 index.html 中手工调整的 CSS 和 HTML 结构

**Non-Goals:**
- 不支持 index.html → README.md 的反向同步
- 不是 git hook 自动触发（仅人工运行命令触发）
- 不改变 README.md 或 index.html 的现有格式约定
- 不引入额外的模板引擎或构建工具
- 绝不可更改 index.html 中的 ICP 备案号

## Decisions

### D1: 增量语义更新，而非全量重新生成

**选型**：AI 读取 README.md 的 diff，理解语义变化，只更新 index.html 中受影响的区块。
**替代方案**：从 README.md 全量重新生成 index.html。被拒绝原因：index.html 有大量手工调整的 CSS 和 HTML 细节（emoji、布局、动画），全量生成会丢失这些细节，且模板维护成本高。
**权衡**：增量方案对 AI 语义理解要求更高，但有锚点加持可降低错误率。

### D2: 隐藏 HTML 锚点注释

**选型**：在 index.html 中注入 `<!-- sync:block:xxx -->`（区块级）和 `<!-- sync:item:xxx -->`（条目级）HTML 注释作为映射锚点。AI 根据 diff 所属的 README 区块，直接定位到对应的 HTML 锚点进行更新。
**替代方案**：纯 AI 自然语言匹配，无锚点。被拒绝原因：容易匹配错误，尤其在结构变化时。
**锚点设计**：

```
<!-- sync:block:intro -->      ← 对应 README 简介段落
<!-- sync:block:sites -->      ← 对应站点入口（wii.pub / wii.wiki）
  <!-- sync:item:site-pub -->  ← wii.pub 卡片
  <!-- sync:item:site-wiki --> ← wii.wiki 卡片
<!-- sync:block:links -->      ← 对应链接列表
  <!-- sync:item:link-about -->
  <!-- sync:item:link-thoughts -->
  <!-- sync:item:link-issues -->
  <!-- sync:item:link-github -->
  <!-- sync:item:link-lingxi -->
<!-- sync:block:contact -->     ← 对应联系方式
<!-- sync:block:footer -->      ← 对应页脚
```

**权衡**：需要一次性给 index.html 加好锚点，但这是一次性成本。后续同步精准度显著提高。

### D3: 基于内容哈希的版本追踪

**选型**：使用 `.cache/readme-sync-state.json` 存储：
- `last_sync_hash`: README.md 内容的 SHA256 哈希
- `last_sync_date`: 同步时间戳
- `cached_readme`: 完整 README.md 文本（用于 diff 计算）
- `synced_to_commit`: 可选的 git commit SHA

首次运行时若缓存不存在，进行初始同步（建立锚点映射关系并保存初始状态）。后续运行通过对比 SHA256 判断是否有变更，无需依赖 README.md Front Matter 的 `update` 字段。

**替代方案**：仅依赖 Front Matter `update` 字段。被拒绝原因：日期字符串非内容指纹，两个不同内容可以有相同日期。但可在同步完成后可选更新 `update` 字段作为人类可读的标记。

### D4: 新增内容 AI 推断 + 人工确认

**选型**：当 README.md 新增内容时（如新链接、新描述段落），AI 推断其语义类型（文本更新/链接/站点卡片），按照 index.html 现有 CSS 样式创建对应 HTML 元素，展示 diff 预览后由用户确认。
**替代方案**：AI 自行决定不确认直接写入。被拒绝原因：HTML 结构生成有出错风险，人工确认是安全网。或跳过新增只处理已有锚点——过于保守，减少了自动化的价值。

### D5: 命令形式为 opencode 自定义命令

**选型**：创建 `.opencode/commands/sync-index.md` 文件，包含完整的执行步骤指令。用户通过 opencode 对话 `/sync-index` 触发，AI 按指令逐步执行。
**替代方案**：作为 Makefile target 或独立 CLI 脚本。被拒绝原因：CLI 脚本无法利用 AI 语义理解能力。opencode 命令可以利用 AI 做 diff 分析和 HTML 编辑。

### D6: 备案号硬保护

**选型**：在命令执行逻辑中明确备案号为不可变内容。系统在更新 index.html 时，对 footer 中 `<a href="https://beian.miit.gov.cn/">` 块做跳过保护，任何情况下不修改、不删除。
**理由**：备案号是法定的，与内容无关，不应随文档同步而变化。在命令定义中显式标注该约束。

### D7: 中英双语优先展示中文

**选型**：当 README.md 中同时存在中英文内容时，保留两种语言，但 index.html 中优先展示中文。英文部分由 AI 自动翻译为中文作为主要展示文本。
**理由**：项目的主要受众是中文用户。自动翻译避免手动维护双语内容。
**权衡**：自动翻译可能存在语义偏差，但当前 index.html 已经是纯中文展示，此规则保持一致性。

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| AI 语义分析错误，更新了错误的 HTML 区块 | 锚点注释精确限定映射范围；更新前展示完整 diff 预览 |
| 新增内容时 AI 生成的 HTML 样式不一致 | 人工确认环节；命令中嵌入现有 CSS class 和 DOM 结构作为参考 |
| 缓存状态文件丢失或被误删 | 首次运行检测到缺失时自动重建（相当于全量重新分析） |
| index.html 被手动大幅修改导致锚点丢失 | 命令中增加锚点完整性检查，缺失时告警并提示修复 |
| README.md 大规模重构导致 diff 过大 | 分批展示 diff，关键变更优先处理 |

## Open Questions

- 当 `README.md` 的 Front Matter 变更时（如 title、categories），是否需要同步到 index.html 的 `<title>` 或 hero section？当前设计暂不处理 Front Matter 同步，仅处理正文内容。
- 是否需要 `--dry-run` 模式？当前通过编辑计划预览已实现类似效果，但可考虑增加显式的 dry-run flag。
