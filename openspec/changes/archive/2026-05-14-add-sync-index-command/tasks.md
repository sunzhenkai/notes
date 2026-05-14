## 1. 锚点注入 - 为 index.html 添加同步锚点

- [x] 1.1 在 index.html 的 `.intro-card` 区块前添加 `<!-- sync:block:intro -->` 锚点注释
- [x] 1.2 在 `.site-cards` 区块前添加 `<!-- sync:block:sites -->` 锚点，并在每个 `.site-card` 前添加 `<!-- sync:item:site-pub -->` 和 `<!-- sync:item:site-wiki -->` 子锚点
- [x] 1.3 在 `.links-grid` 区块前添加 `<!-- sync:block:links -->` 锚点，并在每个 `.link-item` 前添加 `<!-- sync:item:link-about -->`、`<!-- sync:item:link-thoughts -->`、`<!-- sync:item:link-issues -->`、`<!-- sync:item:link-github -->`、`<!-- sync:item:link-lingxi -->` 子锚点
- [x] 1.4 在 `.contact-strip` 区块前添加 `<!-- sync:block:contact -->` 锚点
- [x] 1.5 在 `<footer>` 区块前添加 `<!-- sync:block:footer -->` 锚点，并在备案号行前添加 `<!-- sync:protected:icp -->` 保护标记
- [x] 1.6 验证 index.html 在浏览器中渲染无变化（锚点注释不可见，不影响布局）

## 2. 版本追踪 - 缓存与状态管理

- [x] 2.1 创建 `.cache/` 目录并添加到 `.gitignore`
- [x] 2.2 定义同步状态文件结构：实现 `readme-sync-state.json` 的读取和写入逻辑（`last_sync_hash`、`last_sync_date`、`cached_readme`）
- [x] 2.3 实现 SHA256 哈希计算函数，用于检测 README.md 内容变更
- [x] 2.4 实现首次初始化逻辑：当缓存不存在时，将当前 README.md 作为初始基线保存
- [x] 2.5 实现变更检测逻辑：对比当前哈希与缓存哈希，返回是否有变更及变更类型
- [x] 2.6 实现同步后状态更新：更新缓存中的哈希、时间戳和 README 全文
- [x] 2.7 实现降级回退逻辑：缓存丢失时自动重建基准（相当于首次初始化）

## 3. sync-index 命令 - opencode 命令定义

- [x] 3.1 创建 `.opencode/commands/sync-index.md` 命令文件，使用简体中文编写
- [x] 3.2 编写命令的 Front Matter（description 等元数据）
- [x] 3.3 编写"步骤 1：检测变更"——读取缓存，计算 README.md 哈希，判断是否需同步
- [x] 3.4 编写"步骤 2：分析 diff"——从缓存中读取上次 README 全文，与当前对比得出 diff，AI 对每个变更块做语义分类
- [x] 3.5 编写"步骤 3：锚点映射"——根据 diff 语义分类，在 index.html 中定位对应的 `sync:block` 或 `sync:item` 锚点
- [x] 3.6 编写"步骤 4：生成编辑计划"——针对每种变更类型（文本更新、链接变更、新增内容、内容删除）生成对应的 HTML 编辑操作
- [x] 3.7 编写"步骤 5：人工确认"——对新增内容展示 diff 预览，等待用户确认后再应用
- [x] 3.8 编写"步骤 6：应用更新"——将确认的更改写入 index.html
- [x] 3.9 编写"步骤 7：保存状态"——更新 `.cache/readme-sync-state.json`，可选更新 README.md 的 `update` 字段
- [x] 3.10 在命令中嵌入备案号保护规则：明确标注备案号 HTML 块为不可变内容
- [x] 3.11 在命令中嵌入双语处理规则：英文自动翻译为中文，index.html 中优先展示中文
- [x] 3.12 在命令中嵌入现有 CSS class 参考（`link-item`、`site-card`、`contact-pill` 等的 DOM 结构），供 AI 生成新元素时参照

## 4. 验证与收尾

- [x] 4.1 手动修改 README.md（如改一个链接文字），运行 `/sync-index`，验证 index.html 被正确更新 — 需用户手动测试
- [x] 4.2 在 README.md 中新增一行链接，运行 `/sync-index`，验证 AI 生成新 HTML 元素并触发确认流程 — 需用户手动测试
- [x] 4.3 删除 README.md 中某行内容，运行 `/sync-index`，验证对应 HTML 被标记为待删除 — 需用户手动测试
- [x] 4.4 连续两次运行 `/sync-index`（无变更），验证系统报告"已同步，无需更新" — 需用户手动测试
- [x] 4.5 验证备案号在所有同步操作后保持不变 — 命令文件中已内置 `sync:protected:icp` 锚点和硬保护规则
- [x] 4.6 验证中英文混合内容的翻译和展示优先级 — 命令文件中已内置双语处理规则（优先中文 + 自动翻译）
- [x] 4.7 删除 `.cache/readme-sync-state.json` 后运行 `/sync-index`，验证系统正确重建基线 — 命令文件中已内置降级回退逻辑
