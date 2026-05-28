# Superpowers × Claude Code 使用教程

> 在 Claude Code 中安装和使用 Superpowers 的完整指南。

---

## 一、安装

### 方式一：官方 Marketplace（推荐）

```
/plugin install superpowers@claude-plugins-official
```

### 方式二：Superpowers Marketplace

先注册市场，再安装：

```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

---

## 二、验证安装

打开 Claude Code 会话，发送：

```
Tell me about your superpowers
```

Agent 应该会列出所有可用的 Superpowers 技能。如果回复中包含 brainstorming、writing-plans、TDD 等，说明安装成功。

### 检查 Hook 是否生效

Superpowers 通过 `SessionStart` hook 在每次会话启动时注入 bootstrap 上下文。如果 Skill 不自动触发，检查 hooks 配置：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start",
            "async": false
          }
        ]
      }
    ]
  }
}
```

---

## 三、工作原理

Superpowers 在 Claude Code 中通过两个机制工作：

### 1. Bootstrap 注入

`SessionStart` hook 在每次会话启动时运行，注入 `using-superpowers` Skill 的内容到系统提示中。这告诉 Agent：

- 在做任何事情之前，先检查是否有相关 Skill
- Skill 是强制性的工作流，不是建议
- 如果有 1% 的可能性某个 Skill 适用，就必须调用它

### 2. Skill 注册

插件注册所有 Skill 目录，Claude Code 自动发现。每个 Skill 是一个 `SKILL.md` 文件，包含：

- YAML frontmatter（名称、描述、触发条件）
- 详细的工作流指令
- 检查清单和验证步骤

---

## 四、核心工作流

### 自动触发——你不需要做任何特别的事

```
你：帮我做一个 React Todo List

Agent：[自动触发 brainstorming skill，不直接写代码]
      → "你想要什么样的 Todo List？"
      → "需要持久化吗？"
      → "有没有排序/过滤需求？"
      → 逐步提炼需求
      → 分段呈现设计，每段等你确认
      → 设计批准后保存设计文档

Agent：[自动触发 writing-plans skill]
      → 拆解成 2-5 分钟的小任务
      → 每个任务有文件路径、代码、验证步骤

Agent：[自动触发 using-git-worktrees]
      → 创建隔离的 git worktree
      → 在新分支上工作

Agent：[自动触发 subagent-driven-development]
      → 每个任务分派新子 Agent
      → 两阶段审查
      → 可以自主工作数小时
```

---

## 五、常用场景

### 场景 1：开发新功能

直接描述需求，其他全自动：

```
你：给用户资料页添加头像上传功能
（Agent 自动走 brainstorming → plan → implement → review 流程）
```

### 场景 2：调试问题

```
你：这个 API 返回 500 错误
（Agent 自动触发 systematic-debugging，4 阶段根因分析）
```

### 场景 3：代码审查

```
你：帮我审查这个 PR
（Agent 自动触发 requesting-code-review）
```

### 场景 4：接收代码审查反馈

```
你：审查者说这个方法太复杂了
（Agent 自动触发 receiving-code-review，技术严谨地评估反馈）
```

### 场景 5：并行开发

```
你：我要同时开发登录、注册、密码重置三个功能
（Agent 触发 dispatching-parallel-agents，多子 Agent 并行）
```

---

## 六、关键 Skill 速查

| 你说什么 | 触发的 Skill |
|---------|-------------|
| "帮我做个 XX" | brainstorming → writing-plans → subagent-driven-development |
| "这个 bug 怎么回事" | systematic-debugging |
| "帮我审查代码" | requesting-code-review |
| "审查者说 XXX" | receiving-code-review |
| "我要同时做 A、B、C" | dispatching-parallel-agents |
| "好了，发布吧" | finishing-a-development-branch |
| "写个新 Skill" | writing-skills |

---

## 七、自定义 Skill

### 项目级 Skill

在项目根目录创建 `.claude/skills/my-skill/SKILL.md`：

```markdown
---
name: my-skill
description: Use when [条件] - [做什么]
triggers:
  - 关键词1
  - 关键词2
---

# My Skill

[你的工作流指令]
```

### 个人级 Skill

在 `~/.claude/skills/my-skill/SKILL.md` 创建，格式同上。

**优先级**：项目级 > 个人级 > Superpowers

---

## 八、注意事项

1. **Claude Code 是一等公民**：Superpowers 最初为 Claude Code 设计，所有功能在此平台上完整可用
2. **子 Agent 支持**：Claude Code 的 `Task` tool 完整支持子 Agent 分派，`subagent-driven-development` 可以充分发挥
3. **Plan Mode**：Claude Code 的 Plan Mode 和 Superpowers 的 brainstorming 协同工作
4. **TDD 是硬性要求**：Skill 会删除先于测试写的代码，不要试图绕过
5. **更新**：插件会自动更新，也可通过 marketplace 手动更新

---

## 九、常见问题

### Skill 不自动触发

1. 确认 plugin 已正确安装（`/plugin list` 查看）
2. 重启 Claude Code 会话
3. 检查 SessionStart hook 是否正常

### Brainstorming 没有启动

有些情况下 Agent 可能直接开始写代码。此时：

1. 明确说："先不写代码，帮我设计一下"
2. 或说："use brainstorming skill"

### 子 Agent 失败

1. 确认使用的是 Claude Code（不是 Claude.ai 网页版）
2. 子 Agent 需要完整的工具访问权限

---

## 相关资源

- [Superpowers 概览](./README.md)
- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Superpowers GitHub](https://github.com/obra/superpowers)
- [Superpowers Discord](https://discord.gg/superpowers)
