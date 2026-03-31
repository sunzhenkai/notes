# 工作流程

本指南涵盖 OpenSpec 的常见工作流程模式以及何时使用它们。有关基本设置，请参阅[入门指南](./getting-started.md)。有关命令参考，请参阅[命令](./commands.md)。

## 哲学：行动，而非阶段

传统的工作流强迫你经历阶段：先规划，然后实施，然后完成。但现实工作并不完全符合这些框框。

OPSX 采用了不同的方法：

```text
传统（阶段锁定）：

  PLANNING ────────► IMPLEMENTING ────────► DONE
      │                    │
      │   "不能回去"      │
      └────────────────────┘

OPSX（流式行动）：

  proposal ──► specs ──► design ──► tasks ──► implement
```

**关键原则：**

- **行动，而非阶段** - 命令是你可以做的事情，而不是你被困的阶段
- **依赖关系是赋能者** - 它们显示什么是可能的，而不是下一步必须做什么

> **自定义：** OPSX 工作流由定义工件序列的模式驱动。有关创建自定义模式的详细信息，请参阅[自定义](./customization.md)。

## 两种模式

### 默认快速路径（`core` 配置）

新安装默认为 `core`，它提供：
- `/opsx:propose`
- `/opsx:explore`
- `/opsx:apply`
- `/opsx:archive`

典型流程：

```text
/opsx:propose ──► /opsx:apply ──► /opsx:archive
```

### 扩展/完整工作流（自定义选择）

如果你想要明确的脚手架和构建命令（`/opsx:new`、`/opsx:continue`、`/opsx:ff`、`/opsx:verify`、`/opsx:sync`、`/opsx:bulk-archive`、`/opsx:onboard`），可以通过以下方式启用：

```bash
openspec config profile
openspec update
```

## 工作流程模式（扩展模式）

### 快速功能

当你知道要构建什么，只需要执行时：

```text
/opsx:new ──► /opsx:ff ──► /opsx:apply ──► /opsx:verify ──► /opsx:archive
```

**示例对话：**

```text
You: /opsx:new add-logout-button

AI:  Created openspec/changes/add-logout-button/
     准备创建：proposal

You: /opsx:ff

AI:  正在创建所有规划工件...
     ✓ proposal.md
     ✓ specs/
     ✓ design.md
     ✓ tasks.md
     准备实施！

You: /opsx:apply

AI:  正在完成任务...
     ✓ 将注销按钮添加到 header
     ✓ 实现了会话清除
     ✓ 添加了确认对话框
     所有任务完成！

You: /opsx:archive

AI:  ✓ 已合并规范
     ✓ 已归档变更
```

**最适合：** 中小型功能、错误修复、简单的变更。

### 探索式

当需求不明确或需要先调查时：

```text
/opsx:explore ──► /opsx:new ──► /opsx:continue ──► ... ──► /opsx:apply
```

**示例对话：**

```text
You: /opsx:explore

AI:  你想探索什么？

You: 我想提高页面加载性能，但不确定瓶颈在哪里。

AI:  让我帮你调查...
     [分析包大小，识别慢查询，审查组件渲染模式]

     我发现了三个主要瓶颈：
     1. 大的未优化图像
     2. ProductList 中的同步数据获取
     3. 来自上下文更改的重新渲染

     你想先解决哪个？

You: 让我们先解决数据获取问题。

You: /opsx:new optimize-product-list-fetching

AI:  Created change. 准备创建：proposal

You: /opsx:continue

AI:  根据我们的探索创建提案...
     [编写提案，整合调查见解]

     准备创建：specs, design
     你接下来想要哪个？

You: /opsx:continue

AI:  正在创建规范...
```

**最适合：** 性能优化、调试、架构决策、不明确的需求。

### 并行变更

同时处理多个变更：

```text
变更 A: /opsx:new ──► /opsx:ff ──► /opsx:apply (进行中)
                                         │
                                    上下文切换
                                         │
变更 B: /opsx:new ──► /opsx:ff ──────► /opsx:apply
```

**示例对话：**

```text
You: 我正在处理 add-dark-mode 但被拉去修复错误

You: /opsx:new fix-login-redirect

AI:  Created openspec/changes/fix-login-redirect/

You: /opsx:ff

AI:  ✓ 已创建规划工件

You: /opsx:apply

AI:  正在处理 fix-login-redirect...
     [实施修复]
     所有任务完成！

You: /opsx:archive

AI:  ✓ 已归档 fix-login-redirect

You: 让我们回到暗模式

You: /opsx:apply add-dark-mode

AI:  正在恢复 add-dark-mode...
     从任务 2.3 继续：更新 Header...
```

**最适合：** 并行工作流、紧急中断、团队协作。

当有多个完成的变更时，使用 `/opsx:bulk-archive`：

```text
You: /opsx:bulk-archive

AI:  发现 3 个完成的变更：
     - add-dark-mode (所有任务完成)
     - fix-login-redirect (所有任务完成)
     - update-footer (所有任务完成)

     检查规范冲突...
     ⚠ add-dark-mode 和 update-footer 都触及 specs/ui/

     检查代码库以解决...
     两个变更都已实现。将按时间顺序应用。

     归档所有 3 个变更？

You: 是

AI:  ✓ 已归档 add-dark-mode
     ✓ 已归档 fix-login-redirect
     ✓ 已归档 update-footer
     规范合并顺序：add-dark-mode → update-footer
```

批量归档检测多个变更何时触及相同的规范，并通过检查实际实施的内容来解决冲突。

### 完成变更

推荐的完成流程：

```text
/opsx:apply ──► /opsx:verify ──► /opsx:archive
                    │                 │
              验证              提示同步
              实现              如需要
```

#### Verify: 检查你的工作

`/opsx:verify` 在三个维度上验证实现与工件的一致性：

```text
You: /opsx:verify

AI:  正在验证 add-auth...

     COMPLETENESS
     ✓ tasks.md 中的所有 12 个任务都已检查
     ✓ 规范中的所有需求都有相应的代码
     ⚠ 场景"不活动后会话超时"未测试

     CORRECTNESS
     ✓ 实现与规范意图匹配
     ✓ 场景中的边缘情况已处理
     ✓ 错误状态与规范定义匹配

     COHERENCE
     ✓ 设计决策反映在代码结构中
     ✓ 命名约定与 design.md 一致
     ⚠ 设计提到"事件驱动"但实现使用轮询

     SUMMARY
     ─────────────────────────────
     关键问题：0
     警告：2
     准备归档：是（有警告）

     建议：
     1. 为会话超时场景添加测试
     2. 考虑重构为事件驱动（如设计所述），或更新 design.md
```

**verify 检查的内容：**

| 维度 | 验证内容 |
|------|---------|
| Completeness | 所有任务完成，所有需求已实施，场景已覆盖 |
| Correctness | 实现与规范意图匹配，边缘情况已处理 |
| Coherence | 设计决策反映在代码中，模式一致 |

Verify 不会阻止归档，但会显示你可能想要先解决的问题。

#### Archive: 完成变更

`/opsx:archive` 完成变更并将其移动到归档：

```text
You: /opsx:archive

AI:  正在归档 add-auth...

     工件状态：
     ✓ proposal.md 存在
     ✓ specs/ 存在
     ✓ design.md 存在
     ✓ tasks.md 存在（12/12 任务完成）

     Delta 规范：尚未同步到主规范
     → 现在要同步吗？

You: 是

AI:  ✓ 已将规范同步到 openspec/specs/auth/spec.md
     ✓ 移动到 openspec/changes/archive/2025-01-24-add-auth/

     变更归档成功。
```

如果规范未同步，归档会提示。它不会因未完成的任务而阻止，但会警告。

## 何时使用什么

### `/opsx:ff` vs `/opsx:continue`

| 情况 | 使用 |
|------|------|
| 需求明确，准备构建 | `/opsx:ff` |
| 探索中，想要审查每一步 | `/opsx:continue` |
| 在规范之前想要迭代提案 | `/opsx:continue` |
| 时间压力，需要快速移动 | `/opsx:ff` |
| 复杂变更，想要控制 | `/opsx:continue` |

**经验法则：** 如果你能够预先描述完整范围，使用 `/opsx:ff`。如果你在过程中弄清楚，使用 `/opsx:continue`。

### 何时更新 vs 开始新变更

一个常见问题：何时更新现有变更是可以的，何时应该开始新的变更？

**更新现有变更时：**

- 相同意图，执行优化
- 范围缩小（MVP 优先，其余稍后）
- 学习驱动的更正（代码库不是你预期的）
- 基于实现发现的设计调整

**开始新变更时：**

- 意图根本改变
- 范围爆发到完全不同的工作
- 原始变更可以独立标记为"完成"
- 补丁会比阐明更混乱

```text
                     ┌─────────────────────────────────────┐
                     │     这是相同的工作吗？              │
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
      YES               NO YES           NO  NO              YES
       │                 │  │             │   │               │
       ▼                 ▼  ▼             ▼   ▼               ▼
    UPDATE            NEW  UPDATE       NEW  UPDATE          NEW
```

**示例："添加暗模式"**

- "还需要支持自定义主题" → 新变更（范围爆发）
- "系统首选项检测比预期更难" → 更新（相同意图）
- "让我们先发布切换，稍后添加首选项" → 更新然后归档，然后新变更

## 最佳实践

### 保持变更聚焦

每个更改一个逻辑工作单元。如果你正在"添加功能 X 并且还重构 Y"，考虑两个单独的变更。

**为什么重要：**
- 更容易审查和理解
- 更清晰的归档历史
- 可以独立发布
- 更简单的回滚（如果需要）

### 为不明确的需求使用 `/opsx:explore`

在承诺变更之前，探索问题空间：

```text
You: /opsx:explore

AI:  你想探索什么？

You: 我们应该如何处理 API 的速率限制？

AI:  让我调查你当前的设置和选项...
     [研究代码库，考虑模式]

     我看到我们可以采用三种方法：
     1. 基于中间件（简单，每端点）
     2. Redis 后端（可扩展，共享状态）
     3. 每用户令牌桶（公平，复杂）

     你当前的堆栈建议 #1 或 #2。你的规模如何？
```

探索在创建工件之前澄清思维。

### 在归档前验证

使用 `/opsx:verify` 检查实现是否与工件匹配：

```text
You: /opsx:verify

AI:  正在验证 add-dark-mode...

     ✓ tasks.md 中的所有任务都已检查
     ✓ 规范中的需求有相应的代码
     ✓ 设计决策反映在实现中

     准备归档！
```

在关闭变更之前捕获不匹配。

### 清楚地命名变更

好的名称让 `openspec list` 有用：

```text
好的：                          避免：
add-dark-mode                  feature-1
fix-login-redirect             update
optimize-product-query         changes
implement-2fa                  wip
```

## 命令快速参考

有关命令详细信息和选项，请参阅[命令](./commands.md)。

| 命令 | 目的 | 何时使用 |
|------|------|----------|
| `/opsx:propose` | 创建变更 + 规划工件 | 快速默认路径（`core` 配置） |
| `/opsx:explore` | 思考想法 | 不明确的需求、调查 |
| `/opsx:new` | 开始变更脚手架 | 扩展模式，明确的工件控制 |
| `/opsx:continue` | 创建下一个工件 | 扩展模式，逐步工件创建 |
| `/opsx:ff` | 创建所有规划工件 | 扩展模式，清晰范围 |
| `/opsx:apply` | 实现任务 | 准备编写代码 |
| `/opsx:verify` | 验证实现 | 扩展模式，归档前 |
| `/opsx:sync` | 合并 delta 规范 | 扩展模式，可选 |
| `/opsx:archive` | 完成变更 | 所有工作完成 |
| `/opsx:bulk-archive` | 归档多个变更 | 扩展模式，并行工作 |

## 下一步

- [命令](./commands.md) - 完整命令参考和选项
- [概念](./concepts.md) - 深入了解规范、工件和模式
- [自定义](./customization.md) - 创建自定义工作流
