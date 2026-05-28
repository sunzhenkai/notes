# Superpowers × OpenCode 使用教程

> 在 OpenCode 中安装和使用 Superpowers 的完整指南。

---

## 一、安装

### 方式一：Plugin 配置（推荐）

在 `opencode.json`（全局或项目级）中添加 plugin：

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"]
}
```

重启 OpenCode，插件自动安装并注册所有 Skill。

### 方式二：指定版本

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git#v5.0.3"]
}
```

### 从旧版符号链接安装迁移

如果你之前用 `git clone` + 符号链接方式安装：

```bash
# 删除旧链接
rm -f ~/.config/opencode/plugins/superpowers.js
rm -rf ~/.config/opencode/skills/superpowers
rm -rf ~/.config/opencode/superpowers

# 然后按方式一重新安装
```

---

## 二、验证安装

重启 OpenCode 后，发送：

```
Tell me about your superpowers
```

Agent 应该会列出所有可用的 Superpowers 技能。如果只回复了普通问候，说明插件未加载。

---

## 三、使用方式

### 列出所有 Skill

```
use skill tool to list skills
```

### 加载指定 Skill

```
use skill tool to load brainstorming
```

### Skill 优先级

```
项目级 Skill > 个人 Skill > Superpowers Skill
```

- **项目级**：`.opencode/skills/` 目录（在项目根目录）
- **个人级**：`~/.config/opencode/skills/` 目录
- **Superpowers**：通过 plugin 自动注册

---

## 四、创建自定义 Skill

### 个人 Skill

```bash
mkdir -p ~/.config/opencode/skills/my-skill
```

创建 `~/.config/opencode/skills/my-skill/SKILL.md`：

```markdown
---
name: my-skill
description: Use when [条件] - [做什么]
---

# My Skill

[你的 Skill 内容]
```

### 项目 Skill

在项目根目录创建 `.opencode/skills/my-skill/SKILL.md`，格式同上。

---

## 五、工作流实战

### 场景 1：从零开发新功能

直接描述你想做什么，Superpowers 自动触发：

```
你：我想做一个用户注册功能

Agent：[自动触发 brainstorming skill]
      → 逐步提问，澄清需求
      → 分段呈现设计，等你确认
      → 确认后保存设计文档
      → [自动触发 writing-plans]
      → 生成实现计划
      → [自动触发 subagent-driven-development]
      → 分派子 Agent 逐任务实现
```

**你不需要手动调用任何 Skill。** 只要说清楚想做什么，Agent 自动走完流程。

### 场景 2：调试 bug

```
你：这个测试失败了，帮我看看

Agent：[自动触发 systematic-debugging]
      → 4 阶段根因分析
      → 不猜测，先调查
      → 修复后 [自动触发 verification-before-completion]
      → 确保真正修好了
```

### 场景 3：并行开发多个功能

```
你：我计划做 A、B、C 三个功能

Agent：[触发 brainstorming → writing-plans]
      → 计划完成后 [触发 dispatching-parallel-agents]
      → 多个子 Agent 同时工作
      → 每个完成时审查
```

---

## 六、工具映射

Superpowers 的 Skill 最初为 Claude Code 编写，OpenCode 自动适配：

| Claude Code 工具 | OpenCode 等价 |
|------------------|--------------|
| `TodoWrite` | `todowrite` |
| `Task`（子 Agent） | `@mention` 系统 |
| `Skill` tool | OpenCode 原生 `skill` tool |
| `Read` / `Write` / `Edit` / `Bash` | OpenCode 原生工具 |

---

## 七、更新

OpenCode 通过 git 依赖安装 Superpowers。某些版本会缓存，重启可能不会拉取最新提交：

1. 清除 OpenCode 包缓存
2. 或重新安装 plugin
3. 或指定版本号强制更新

---

## 八、常见问题

### 插件不加载

```bash
# 检查日志
opencode run --print-logs "hello" 2>&1 | grep -i superpowers
```

1. 确认 `opencode.json` 中 plugin 配置正确
2. 确认 OpenCode 版本足够新
3. 重启 OpenCode

### Skill 找不到

1. 用 `skill` tool 列出可用 Skill
2. 确认 plugin 正在加载
3. 每个 Skill 需要有 `SKILL.md` 文件和有效的 YAML frontmatter

### Bootstrap 没出现

1. 确认 OpenCode 版本支持 `experimental.chat.system.transform` hook
2. 修改配置后重启 OpenCode

---

## 相关资源

- [Superpowers 概览](./README.md)
- [OpenCode 官方文档](https://opencode.ai/docs/)
- [Superpowers OpenCode 详细文档](https://github.com/obra/superpowers/blob/master/docs/README.opencode.md)
