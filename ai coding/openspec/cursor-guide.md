# Cursor IDE 专用指南

## 概述

Cursor IDE 使用 OpenSpec 的**默认快速路径（core profile）**，提供简洁的四步工作流。

## Cursor IDE 的四个命令

在 Cursor 中，OpenSpec 命令使用**连字符**格式（不同于其他 IDE 的冒号格式）：

```
/opsx-propose    # 创建变更提案
/opsx-explore    # 探索想法
/opsx-apply      # 实施任务
/opsx-archive     # 归档已完成的变更
```

## Cursor 的工作流程

### 快速路径（需求明确时）

```
/opsx-propose ──► /opsx-apply ──► /opsx-archive
```

### 探索路径（需求不明确时）

`/opsx-explore` 是纯对话模式，不创建任何文件，用于在正式提案前理清思路：

```
/opsx-explore ──► /opsx-propose ──► /opsx-apply ──► /opsx-archive
     ▲
     │
  理清问题、调查代码库、讨论方案
  想清楚后再 propose
```

**完整示例：**

```text
You: /opsx-propose add-dark-mode

AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md — 为什么要这样做，正在改变什么
     ✓ specs/       — 需求和场景
     ✓ design.md    — 技术方法
     ✓ tasks.md     — 实现清单
     准备好实施！

You: /opsx-apply

AI:  正在实施 add-dark-mode...
     ✓ 1.1 创建带有明暗状态的 ThemeContext
     ✓ 1.2 将 CSS 自定义属性添加到 globals.css
     ✓ 1.3 实现 localStorage 持久化
     ✓ 2.1 创建 ThemeToggle 组件
     ...
     所有任务完成！

You: /opsx-archive

AI:  正在归档 add-dark-mode...
     ✓ 已将规范合并到 openspec/specs/ui/spec.md
     ✓ 移动到 openspec/changes/archive/2025-01-24-add-dark-mode/
     完成！准备下一个功能。
```

## Proposal 完成后想改进怎么办？

**直接对话即可，不需要输入任何命令。** `/opsx-propose` 运行后，AI 已经有上下文，直接用自然语言告诉它你想怎么改就行。

```text
You: /opsx-propose add-dark-mode

AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md
     ✓ specs/
     ✓ design.md
     ✓ tasks.md

You: 方案改成用 Tailwind 的 dark: 前缀，不要用 CSS 变量

AI:  好的，我来更新相关工件...
     ✓ 已更新 proposal.md（技术方案）
     ✓ 已更新 design.md
     ✓ 已更新 specs/
     ✓ 已更新 tasks.md（调整了相关任务）

You: 另外先不做系统首选项检测了，只保留手动切换

AI:  好的，缩小范围...
     ✓ 已更新 specs/（移除系统首选项需求）
     ✓ 已更新 tasks.md（删除相关任务）

You: /opsx-apply

AI:  正在实施...
```

### 什么时候该直接对话 vs 开新变更？

| 情况 | 操作 | 示例 |
|------|------|------|
| 相同意图，细化执行 | 对话修改 | "改用 Tailwind 实现" |
| 范围缩小 | 对话修改 | "先不做自定义颜色了" |
| 发现遗漏 | 对话修改 | "加上 iOS 兼容性" |
| 意图根本改变 | 新变更 | 从"暗模式"变成"完整主题系统" |
| 范围爆炸 | 新变更 | 从"切换按钮"变成"主题引擎" |

### 方案 2：启用扩展工作流（推荐用于复杂变更）

如果想要**更多控制**，可以启用扩展工作流：

```bash
# 1. 在终端运行（不需要在 Cursor 中）
openspec config profile

# 2. 在交互式菜单中选择：
#    - Change delivery + workflows（更改交付 + 工作流）
#    - 然后在 workflow 列表中勾选：
#      ☑ propose
#      ☑ explore
#      ☑ new
#      ☑ continue
#      ☑ ff
#      ☑ apply
#      ☑ verify
#      ☑ archive

# 3. 更新 Cursor 的技能和命令
openspec update
```

**扩展工作流额外命令：**

```
/opsx-new         # 开始变更脚手架
/opsx-continue    # 创建下一个工件（一次一个）
/opsx-ff          # 快速前进：创建所有规划工件
/opsx-verify      # 验证实现
```

**使用扩展工作流的示例：**

```text
# 开始变更
You: /opsx-new add-auth

AI:  Created openspec/changes/add-auth/
     准备创建：proposal

# 渐进式创建工件
You: /opsx-continue

AI:  正在创建 proposal...

You: /opsx-continue

AI:  正在创建 specs...

You: /opsx-continue

AI:  正在创建 design...

You: /opsx-continue

AI:  正在创建 tasks...
     所有规划工件完成！

# 或一次性完成
You: /opsx-ff

AI:  正在创建所有规划工件...
     ✓ proposal.md
     ✓ specs/
     ✓ design.md
     ✓ tasks.md
     准备实施！
```

### 方案 3：开始新变更（当改进变成不同工作时）

根据 OpenSpec 的决策指南：

```text
                    ┌─────────────────────────────────────┐
                    │     这是相同的工作吗？          │
                    └──────────────┬──────────────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
                ▼                  ▼                  ▼
         相同意图？       >50% 重叠？      原始可以
         相同问题？      相同范围？        在没有这些
                │                  │          变更的情况下
                │                  │          "完成"？
      ┌────────┴────────┐  ┌──────┴──────┐   ┌───────┴───────┐
      │                 │  │             │   │               │
     是                否 是           否  否              是
      │                 │  │             │   │               │
      ▼                 ▼  ▼             ▼   ▼               ▼
    更新              新 更新         新 更新              新
```

**更新 vs 新变更的判断标准：**

| 情况 | 操作 | 原因 |
|--------|------|------|
| 相同意图，细化执行 | 更新 | 同一个目标的不同实现方式 |
| 范围缩小（先 MVP） | 更新 | 可以独立标记为完成 |
| 范围爆炸（变成不同工作） | 新变更 | 原始提案无法识别 |
| 意图根本改变 | 新变更 | 解决不同问题 |

**示例决策：**

```text
场景 1："添加暗模式" → "需要支持自定义主题"
→ 新变更（范围爆炸）
原因：从基本暗模式变成完整主题系统

场景 2："添加暗模式" → "系统首选项检测比预期难"
→ 更新（相同意图）
原因：相同目标，只是实现更复杂

场景 3："添加暗模式" → "先发布切换，稍后添加首选项"
→ 更新然后归档，然后新变更
原因：原始可以作为 MVP 完成
```

## 实际工作流程示例

### 场景 1：简单的功能实现（直接路径）

```text
1. /opsx-propose add-user-profile
   → 创建变更和所有工件

2. /opsx-apply
   → 实施任务

3. /opsx-archive
   → 归档变更
```

### 场景 2：探索性工作（需要先理解问题）

```text
1. /opsx-explore
   AI: 你想探索什么？

2. 我想提高页面加载性能但不确定瓶颈

3. AI: 让我调查...
    发现三个瓶颈：
    1. 大的未优化图像
    2. ProductList 中的同步数据获取
    3. 来自上下文更改的重新渲染

4. 让我们解决数据获取问题

5. /opsx-propose optimize-product-list-fetching
   → 创建变更

6. /opsx-apply
   → 实施优化

7. /opsx-archive
   → 归档
```

### 场景 3：实施中发现问题（对话调整）

```text
1. /opsx-propose add-dark-mode
   → 创建 proposal、specs、design、tasks

2. /opsx-apply
   AI: 正在实施...

3. 实施 1.2 时发现：
   CSS 变量与现有 Tailwind 配置冲突

4. 直接对话：
   You: CSS 变量和 Tailwind 冲突了，改用 dark: 前缀

   AI: 好的，我来调整...
       ✓ 已更新 proposal.md
       ✓ 已更新 design.md
       ✓ 已更新 tasks.md（替换了冲突的任务）

5. 继续应用：
   You: /opsx-apply

   AI: 从任务 1.2 继续（已更新）...

6. 完成：
   You: /opsx-archive
```

### 场景 4：并行工作（切换上下文）

```text
变更 A（进行中）：
1. /opsx-propose add-dark-mode
2. /opsx:apply
   → 实施到一半...

被拉去修复错误：

3. /opsx-propose fix-login-bug
   → 创建新变更

4. /opsx-apply fix-login-bug
   → 完成修复

5. /opsx-archive fix-login-bug
   → 归档错误修复

回到原工作：

6. /opsx-apply add-dark-mode
   AI: 正在恢复 add-dark-mode...
       从任务 2.3 继续：更新 Header...
```

## 技能文件位置

Cursor 中的 OpenSpec 技能和命令位于：

```
.cursor/
├── skills/
│   └── openspec-*/
│       └── SKILL.md           # 技能定义
└── commands/
    └── opsx-*.md              # 命令文件
        ├── opsx-propose.md
        ├── opsx-explore.md
        ├── opsx-apply.md
        └── opsx-archive.md
```

## 常见问题

### Q: 为什么 Cursor 只有四个命令？

A: Cursor 使用默认的 `core` profile，这是 OpenSpec 为快速、高效的工作流设计的。如果你需要更多控制，可以通过 `openspec config profile` 启用扩展工作流。

### Q: `propose` 和 `explore` 有什么区别？

A: `explore` 是**思考模式** —— 不创建文件，只是对话和调查。当你准备好创建实际变更时，使用 `propose`。

### Q: 如何查看当前状态？

A: 使用 CLI 命令（在终端）：

```bash
# 列出所有变更
openspec list

# 查看特定变更的详情
openspec show add-dark-mode

# 查看工件状态
openspec status --change add-dark-mode
```

### Q: 我可以同时使用 CLI 和 Cursor 命令吗？

A: 完全可以！它们互补：
- **CLI 命令**：用于状态检查、验证、模式管理
- **Cursor 命令**：用于创建工件、实施、归档

### Q: proposal 完成后，发现需求变了怎么办？

A: 取决于变化程度：
- **小调整**：直接编辑 `proposal.md`，然后继续应用
- **重大变化**：开始新变更
- **范围爆炸**：归档当前变更（作为 MVP），开始新变更处理扩展

### Q: 如何回滚工件更改？

A: 工件文件（proposal.md、design.md、tasks.md）在 `openspec/changes/` 目录中，像其他源代码文件一样进行版本控制（git）。

```bash
# 查看更改
git diff openspec/changes/add-dark-mode/proposal.md

# 撤销更改
git checkout openspec/changes/add-dark-mode/proposal.md
```

## 最佳实践

### 1. 从 `explore` 开始处理复杂问题

当你不确定方向时：
```text
/opsx-explore
→ 讨论问题
→ 选项和权衡
→ 然后使用 /opsx-propose
```

### 2. 保持变更聚焦

每个更改一个逻辑工作单位。如果你正在做"添加功能 X 并且还重构 Y"，考虑两个单独的变更。

### 3. 命名变更清楚

```text
好的：                          避免：
add-dark-mode                  feature-1
fix-login-redirect             update
optimize-product-query         changes
```

### 4. 在归档前验证

如果启用了扩展工作流：
```text
/opsx:verify
→ 检查完整性
→ 检查正确性
→ 检查一致性
```

即使没有 `verify`，也可以手动检查：
- 所有 tasks.md 中的任务都勾选了？
- 所有需求都有相应的代码？
- 设计决策反映在实现中？

### 5. 清理上下文

OpenSpec 从干净的上下文窗口受益。在开始实施之前：
- 清除之前的聊天历史
- 保持良好的上下文卫生

## 下一步

- **启用扩展工作流**：如果想要更多控制，运行 `openspec config profile`
- **自定义配置**：创建 `openspec/config.yaml` 添加项目特定上下文
- **查看 CLI 参考**：了解更多终端命令
- **阅读工作流**：了解其他工作流模式

## 故障排除

### "命令未被识别"

确保：
1. OpenSpec 已初始化：`openspec init`
2. Cursor 已刷新技能：`openspec update`
3. 重启 Cursor IDE 以获取新技能

### "变更未找到"

- 检查变更文件夹是否存在：`openspec list`
- 确认你在正确的项目目录

### "没有准备就绪的工件"

- 运行 `openspec status --change <name>` 查看阻塞内容
- 创建缺失的依赖工件
