---
description: 检测 README.md 的变更，通过 AI 语义分析 diff 增量更新 index.html
---

# /sync-index

检测 `README.md` 的变更，通过 AI 语义分析 diff，增量更新 `index.html` 对应区块。保留版权、样式等手动内容不变。

---

## 概述

本命令比较当前 `README.md` 内容与上次同步时缓存的版本，使用 diff 分析语义变化，将变更精确映射到 `index.html` 中带 `<!-- sync:block:* -->` / `<!-- sync:item:* -->` 锚点注释的对应区块。

## 执行步骤

### 步骤 1: 检测变更

1. **读取状态文件** `.cache/readme-sync-state.json`：
   - 若文件不存在 → 这是**首次运行**，跳到步骤 2 进行全量分析（无 diff，直接分析完整 README.md）
   - 若文件存在 → 读取 `last_sync_hash` 和 `cached_readme` 字段

2. **计算当前 README.md 的 SHA256 哈希**：
   - 使用 `sha256sum README.md` 或等价的 Python/Node 方法计算
   - 若 README.md 为空或不存在 → 报错终止

3. **比较哈希**：
   - 若 `当前哈希 == last_sync_hash` → 报告 "✅ README.md 没有变更，index.html 已是最新状态" 并退出
   - 若 `当前哈希 != last_sync_hash` → 继续步骤 2

### 步骤 2: 分析 diff

1. **获取内容差异**：
   - 若有 `cached_readme`：对比当前 README.md 与 `cached_readme`，逐一标注 diff 块
   - 若首次运行（无缓存）：无需 diff，将整个 README.md 内容视为分析对象

2. **对每个 diff 块做语义分类**，识别变更类型：

   | 变更类型 | 说明 | 示例 |
   |---------|------|------|
   | `text_update` | 段落文字修改 | "基于 MdServe" → "基于 Hexo" |
   | `link_update` | 链接 URL 或文字变更 | 修改 about.md 路径或描述 |
   | `content_add` | 新增内容（段落/链接/站点） | 新增一个推荐站点链接 |
   | `content_remove` | 内容被删除 | 删除某个链接 |
   | `meta_only` | 仅 Front Matter 变更 | 修改 date/tags 字段 |
   | `no_impact` | 不影响 index.html 的变更 | 纯格式化、空格调整 |

3. **对非 `no_impact` 的变更**，进一步判断其属于 README.md 的哪个逻辑区块：
   - 简介段落 → 对应 `sync:block:intro`
   - 站点描述（wii.pub / wii.wiki）→ 对应 `sync:block:sites`
   - 链接列表 → 对应 `sync:block:links`（需进一步区分是哪个具体 link）
   - 联系方式 → 对应 `sync:block:contact`
   - 页脚 → 对应 `sync:block:footer`

### 步骤 3: 锚点映射

1. **读取 index.html**，验证所有必要的锚点是否存在：
   ```
   sync:block:intro
   sync:block:sites → sync:item:site-pub, sync:item:site-wiki
   sync:block:links → sync:item:link-about, sync:item:link-thoughts,
                      sync:item:link-issues, sync:item:link-github, sync:item:link-lingxi
   sync:block:contact
   sync:block:footer → sync:protected:icp (保护标记，不可修改)
   ```
   若某锚点缺失，输出警告并跳过该区块的更新。

2. **将每个语义变更映射到锚点**：
   - `text_update`：定位到对应 `sync:block` 内的文字内容
   - `link_update`：定位到对应 `sync:item` 的 `<a>` 标签和子元素
   - `content_add`：确定插入位置（在哪个 `sync:block` 内，在哪个 `sync:item` 之后或之前）
   - `content_remove`：定位到对应 `sync:item`，标记待删除

### 步骤 4: 生成编辑计划

针对每种变更类型，按以下规则生成 HTML 编辑操作：

#### 4a. 文本更新 (text_update)
- 在锚点区块内，查找与变更文本语义匹配的 HTML 内容
- 使用**精确替换**（oldString → newString），仅替换变化的文字
- 保留周围的 HTML 标签、CSS class、emoji

#### 4b. 链接更新 (link_update)
- 定位到对应 `sync:item` 的 `<a>` 元素
- 若 URL 变更 → 修改 `href` 属性
- 若链接文字变更 → 同时修改 `.label` 和/或 `.sublabel` 内容
- 保留 `target="_blank" rel="noopener"` 等属性

#### 4c. 新增内容 (content_add)
- 推断新增内容的语义类型（链接/描述/站点卡片）
- 按照 index.html 中**同类元素的 CSS class 和 DOM 结构**生成新 HTML
- 参考下方 CSS 参考 中的模板
- 生成 `<!-- sync:item:* -->` 锚点注释，命名规则: `sync:item:type-description`（kebab-case）
- **注意**：对于新增的站点卡片，需在 `sync:block:sites` 内的 `<div class="site-cards">` 中添加

#### 4d. 内容删除 (content_remove)
- 标记对应的 `sync:item` 及其内部 HTML 为待删除
- 在下方的**人工确认**环节中展示，**不直接删除**

### 步骤 5: 人工确认

1. **展示编辑计划摘要**：
   - 多少项文本更新 → 自动应用
   - 多少项链接更新 → 自动应用
   - 多少项新增内容 → 需要确认
   - 多少项内容删除 → 需要确认

2. **对自动应用项**（文本更新、链接更新）：
   - 展示即将修改的 index.html diff 预览
   - 提示 "以上变更将自动应用。继续？"
   - 等待用户确认

3. **对需确认项**（新增内容、内容删除）：
   - 逐条展示：
     - 新增项：展示 README 中新增的原文 + 生成的 HTML diff
     - 删除项：展示将被删除的 HTML 片段
   - 每条等待用户选择：接受 / 跳过 / 手动修改

### 步骤 6: 应用更新

1. 将确认通过的变更写入 `index.html`
2. 使用 `edit` 工具做精确替换，每次替换保持上下文唯一性
3. **关键约束**：对于 `sync:block:footer` 区块，只更新 `sync:protected:icp` 标记**之外**的内容
4. 验证：应用后重新计数锚点，确保数量一致或合法增加/减少

### 步骤 7: 保存状态

1. 重新计算更新后 README.md 的 SHA256 哈希
2. 将状态写入 `.cache/readme-sync-state.json`：

```json
{
  "last_sync_hash": "<SHA256>",
  "last_sync_date": "<ISO 8601 timestamp>",
  "cached_readme": "<完整的 README.md 文本>",
  "synced_to_commit": "<可选的 git commit SHA>"
}
```

3. **可选**：更新 README.md Front Matter 中的 `update` 字段为当前日期时间（格式: `YYYY-MM-DDTHH:mm:ss+08:00`）。此项操作**不触发**新的同步。
4. 报告同步完成：
   - "✅ 同步完成。index.html 已更新。"

---

## 重要约束

### 🔒 备案号保护（绝对不可触犯）

以下 HTML 内容在任何情况下**禁止修改、删除、或替换**：
```html
<!-- sync:protected:icp -->
<p style="margin-top: 6px; font-size: 0.8rem;">
  <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener">京ICP备2026013364号-2</a>
</p>
```
- 即使用户要求更新备案号，也必须拒绝并提示备案号不可通过此命令更改
- 若 README.md 中包含备案号相关内容，不应将其同步到 index.html

### 🌐 双语内容处理

- README.md 中同时存在中英文时，保留两种语言
- index.html 中**优先展示中文**
- 若某段落仅有英文 → AI 自动翻译为中文作为 index.html 中的主要展示文本
- 若某段落仅有中文 → 直接使用，无需翻译
- 翻译要求：保持原文语义，符合中文技术文档表达习惯

### 📐 样式一致性

- 新增 HTML 元素必须使用 index.html 中已有的 CSS class 和 DOM 结构
- 不要引入新的 class 或内联样式（除非现有代码中已存在）
- 链接项使用 `link-item` 结构，站点卡片使用 `site-card` 结构

---

## CSS class 和 DOM 结构参考

以下为 index.html 中各类元素的 DOM 结构，新增元素时严格参照：

### 链接项 (link-item)
```html
<!-- sync:item:link-xxx -->
<a href="URL" class="link-item" target="_blank" rel="noopener">
  <span class="emoji">🔗</span>
  <span class="label">链接名称</span>
  <span class="sublabel">可选的副标题</span>
  <span class="arrow">→</span>
</a>
```
- 内部链接（如 `./about.md`）不需要 `target="_blank" rel="noopener"`
- `class="sublabel"` 是可选的，仅在有副标题时添加

### 站点卡片 (site-card)
```html
<!-- sync:item:site-xxx -->
<a href="URL" class="site-card" target="_blank" rel="noopener">
  <div class="site-name">
    <span class="icon pub">X</span>
    站点名称
  </div>
  <p class="site-desc">站点描述</p>
  <span class="site-tech">技术栈标签</span>
</a>
```
- `.icon` 使用 `.pub` 或 `.wiki` class（已定义渐变色），或根据需要新增 class（需同步 CSS）

### 联系方式 (contact-pill)
```html
<a href="URL" class="contact-pill">
  ✉️ 文字
</a>
<span class="contact-pill">
  💬 文字
</span>
```

---

## 示例场景

### 场景 A: 修改简介文字

```
README.md diff:
- 整理了一些文档，一部分是笔记，一部分是文章，绝大多数是 Markdown 格式
+ 这里是我整理的笔记和文章，全部使用 Markdown 编写

AI 分析:
  类型: text_update, 区块: intro

编辑计划:
  index.html sync:block:intro 内
  替换 .intro-card p 中的对应文字

→ 自动应用
```

### 场景 B: 新增一个链接

```
README.md diff:
+ - [我的项目](https://example.com) - 一个开源项目

AI 分析:
  类型: content_add, 区块: links

编辑计划:
  在 sync:block:links 内，最后一个 sync:item:link-lingxi 之后
  新增:
    <!-- sync:item:link-my-project -->
    <a href="https://example.com" class="link-item" target="_blank" rel="noopener">
      <span class="emoji">🚀</span>
      <span class="label">我的项目</span>
      <span class="sublabel">一个开源项目</span>
      <span class="arrow">→</span>
    </a>

→ 展示 diff，等待用户确认
```

---

## 错误处理

| 错误情况 | 处理方式 |
|---------|---------|
| README.md 不存在或为空 | 报错终止，提示用户检查 README.md |
| `.cache/` 目录不存在 | 自动创建并进入首次初始化流程 |
| `index.html` 缺少必要锚点 | 输出警告，跳过缺失区块，继续处理其他区块 |
| SHA256 计算失败 | 报告具体错误，终止同步 |
| 缓存状态文件损坏 | 删除并重新初始化（等同于首次运行） |
| README.d 大规模重构 (diff > 50 行) | 提示用户变更较大，建议人工审查后在继续 |
