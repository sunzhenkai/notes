# Superpowers × Cursor 使用教程

> 在 Cursor 中安装和使用 Superpowers 的完整指南。

---

## 一、安装

### 方式一：Plugin Marketplace（推荐）

1. 在 Cursor Agent Chat 中打开插件市场
2. 搜索 "superpowers"
3. 点击安装

### 方式二：手动安装

如果 Marketplace 不可用，可以手动配置：

```bash
# 克隆仓库
git clone https://github.com/obra/superpowers.git ~/superpowers
cd ~/superpowers
```

在项目根目录的 `.cursorrules` 或 `AGENTS.md` 中添加：

```markdown
@~/superpowers/skills/using-superpowers/SKILL.md
```

---

## 二、验证安装

打开 Cursor Agent Chat，发送：

```
Tell me about your superpowers
```

Agent 应该会列出所有可用的 Superpowers 技能。

---

## 三、Cursor 特有配置

### Hooks 配置

Cursor 使用 `hooks-cursor.json` 来注册会话启动钩子：

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "command": "./hooks/run-hook.cmd session-start"
      }
    ]
  }
}
```

这个钩子在每次会话启动时自动注入 Superpowers 的 bootstrap 上下文。

### 配置文件

Cursor 支持以下配置文件来触发 Superpowers：

| 文件 | 用途 |
|------|------|
| `.cursorrules` | 项目级指令，可引用 Superpowers Skill |
| `AGENTS.md` | Agent 行为定义 |
| `CLAUDE.md` | 兼容 Claude Code 格式的指令 |

---

## 四、使用方式

### 自动触发

Superpowers 在 Cursor 中同样自动触发。直接描述你想做什么：

```
你：帮我做一个暗色模式切换

Agent：[自动触发 brainstorming]
      → 提问澄清需求
      → 分段呈现设计
      → 等你确认后生成实现计划
      → 按 TDD 方式实现
```

### 手动触发 Skill

如果自动触发未生效，可以在消息中明确要求：

```
使用 brainstorming skill 来帮我设计这个功能
```

---

## 五、工作流实战

### 完整开发流程

```
1. [描述需求]              ← 你说话
2. brainstorming            ← 自动触发，澄清需求、提炼设计
3. writing-plans            ← 自动触发，拆解成小任务
4. subagent-driven-dev      ← 自动触发，子 Agent 逐任务实现
   ├── test-driven-dev      ← 每个 Agent 内部强制 TDD
   └── code-review          ← 每个任务完成后审查
5. finishing-dev-branch     ← 自动触发，验证、合并、清理
```

### 调试流程

```
你：这个组件渲染有问题

Agent：[自动触发 systematic-debugging]
      → 不猜测，先调查根因
      → 修复后验证
```

---

## 六、注意事项

### Cursor 特有

1. **Agent 模式**：确保使用 Agent 模式（不是普通 Chat），Superpowers 需要 Agent 的工具调用能力
2. **上下文窗口**：Cursor 的上下文窗口有大小限制，复杂项目可能需要分步操作
3. **Skill 可用性**：部分 Skill（如 `using-git-worktrees`）需要终端访问权限
4. **子 Agent**：Cursor 的子 Agent 支持可能和 Claude Code 不同，`subagent-driven-development` 可能需要适配

### 通用

1. **不要跳过 brainstorming**：即使你觉得需求很明确，让 Agent 走完流程
2. **审查设计文档**：Agent 会分段呈现设计，每段都要认真审阅
3. **TDD 是强制的**：Skill 会删除先于测试写的代码

---

## 七、常见问题

### Skill 不触发

1. 检查 `.cursorrules` 或 `AGENTS.md` 是否正确引用了 Superpowers
2. 确认在 Agent 模式下使用
3. 尝试手动要求使用特定 Skill

### 子 Agent 不可用

Cursor 的子 Agent 实现可能与 Claude Code 不同。如果 `subagent-driven-development` 无法分派子 Agent，改用 `executing-plans`（批量执行 + 人工检查点）。

---

## 相关资源

- [Superpowers 概览](./README.md)
- [Cursor 官方文档](https://docs.cursor.com)
- [Superpowers GitHub](https://github.com/obra/superpowers)
