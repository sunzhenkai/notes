---
title: herdr - usage
categories:
  - 工具
  - herdr
tags:
  - herdr
  - tmux
  - terminal-multiplexer
  - ai-coding-agent
date: "2026-08-28T16:30:00+08:00"
update: "2026-08-28T16:30:00+08:00"
---

# Herdr

> Herdr 是一个面向 AI coding agent 的终端复用器（agent multiplexer）。如果你熟 tmux，Herdr 的基础快捷键几乎是故意做成 tmux-like 的；真正新增的是 **Workspace、Worktree、Sidebar、Agent、鼠标操作和 Agent 编排**。
>
> 来源：
> - [Keyboard | herdr](https://herdr.dev/docs/keyboard/)
> - [Config reference | herdr](https://herdr.dev/docs/config-reference/)
> - [GitHub - Mihailorama/herdr-terminal](https://github.com/Mihailorama/herdr-terminal)

Herdr 与 tmux 的关系：

- **基础 terminal multiplexing：Herdr ≈ tmux**
- **Agent + Workspace + Worktree + 可视化状态：Herdr >> tmux**

尤其在同时跑多个 AI coding agent（Claude Code / Codex / Pi / Hermes 等）时，Herdr 解决的核心问题是「我到底有多少 Agent 在跑、哪个卡住了、哪个完成了」，而不只是 tmux 的 pane 管理。

---

## 1. 与 tmux 对应的基础快捷键

Herdr 默认 prefix 也是 `Ctrl-b`：

| 操作        | tmux                    | Herdr               |
| --------- | ----------------------- | ------------------- |
| 新建窗口/Tab  | `prefix+c`              | `prefix+c`          |
| 下一个 Tab   | `prefix+n` / `prefix+l` | `prefix+n`          |
| 上一个 Tab   | `prefix+p` / `prefix+h` | `prefix+p`          |
| Tab 1~9   | `prefix+1..9`           | `prefix+1..9`       |
| Pane 左右上下 | `prefix+方向键` / `hjkl`   | `prefix+h/j/k/l`    |
| 水平分割      | `prefix+"`              | `prefix+minus`      |
| 垂直分割      | `prefix+%`              | `prefix+v`          |
| Zoom Pane | `prefix+z`              | `prefix+z`          |
| 关闭 Pane   | `prefix+x`              | `prefix+x`          |
| Resize    | `prefix+方向键`            | `prefix+r` → `hjkl` |
| Detach    | `prefix+d`              | `prefix+q`          |
| Copy mode | `prefix+[`              | `prefix+[`          |

> 从 tmux 迁移基本没有学习成本。

---

## 2. Herdr 真正额外的快捷键

### Workspace

这是 Herdr 比 tmux 更明显的一级概念：

```text
prefix+w              Workspace 导航
prefix+Shift+n        新建 Workspace
prefix+Shift+w        重命名 Workspace
prefix+Shift+d        关闭 Workspace
```

Workspace 更像：

```text
Workspace
 ├── Tab
 │    ├── Pane
 │    └── Pane
 └── Tab
      └── Pane
```

而不是 tmux 单纯的 session/window/pane 层级。

### Git Worktree

对 AI coding agent 特别有用的能力：`prefix+Shift+g` 直接创建新的 Git worktree。

```text
Workspace
├── main
│   └── Claude Code
├── feature-a
│   └── Codex
└── bugfix-b
    └── Claude Code
```

也就是说它开始把 **Git Worktree + Terminal + Agent** 作为一个整体管理。

### Sidebar

`prefix+b` 切换 Sidebar，会显示：

```text
Workspace
  ├─ Tab
  │   ├─ Claude   🟡 working
  │   └─ shell
  └─ Tab
      └─ Codex    🔴 blocked
```

这就是 tmux 没有的 **Agent awareness**。Herdr 能识别 Agent 的 `working / blocked / done / idle` 状态。

### Session / Workspace 快速导航

`prefix+g` 打开导航/选择器，比 `tmux ls` / `tmux attach` 更偏 GUI/TUI 的 workspace 管理方式。

---

## 3. Herdr 最大的额外能力：Agent

这个没有对应快捷键，但比快捷键更重要。

Herdr 可以识别：

- Claude Code
- Codex
- Pi
- OpenCode
- Hermes
- GitHub Copilot CLI
- Qoder CLI
- 等

然后提供：

```text
Agent 状态
   ↓
working
blocked
done
idle
   ↓
Sidebar / Notification
```

并且 Agent 可以通过 Herdr 的 CLI / Socket API 操作 terminal、pane、session，实现一定程度的 **Agent orchestration**。

---

## 4. 鼠标支持

| tmux | Herdr              |
| ---- | ------------------ |
| 基本靠键盘 | 点击 Pane / Tab / Workspace |
|      | 拖动 Pane 边界调整大小         |
|      | 右键菜单                  |
|      | 鼠标选择复制               |

所以可以完全不记快捷键也能用。

---

## 5. 无 prefix 模式

Herdr 可以配置：

```text
Ctrl+Alt+h   ← 左
Ctrl+Alt+j   ← 下
Ctrl+Alt+k   ← 上
Ctrl+Alt+l   ← 右

Ctrl+Alt+c   ← 新 Tab
Ctrl+Alt+z   ← Zoom
Ctrl+Alt+d   ← Split
```

也就是说 `tmux: Ctrl-b → h` 对应到 `Herdr: Ctrl-Alt-h`，两套可以同时存在。

---

## 6. tmux 用户最值得关注的快捷键

```text
prefix+w              Workspace
prefix+Shift+n        新 Workspace
prefix+Shift+g        Git Worktree
prefix+b              Agent Sidebar
prefix+g              Workspace/Session Picker
prefix+?              查看全部快捷键
```
