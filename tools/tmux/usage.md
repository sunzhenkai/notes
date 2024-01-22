---
wtitle: tmux
categories: 
  - [工具,tmux]
tags:
  - tmux
date: 2020/12/30 00:00:00
update: 2020/12/30 00:00:00
---

# 使用

```shell
# 启动
tmux 
# 启动并设置 session 名称
tmux new -s {session-name}
# attach
tmux a # or at, or attach
# attach by session name
tmux a -t {session-name}
# 列出 session 
tmux ls
# 清理 session
tmux kill-session -t {session-name}
```

# 快捷键

```shell
# active command mode
ctrl + b

# window
c		create
&   close
n   next 
p   previous 
w   list windows
f   find windows
,   name windows

# pane
" 	splite vertical
%		splite horizon
q   show pane numbers
o   change focued pane
ctrl+o  swap panes
[space] 切换布局

x		close panel (or exit)
arrow		change panel

# session
$  rename session
s  list session
d  detach (keep session alive)
```

# 拷贝模式

```shell
# active command mode
ctrl + b

# command
[  开启拷贝模式, 可以滚动屏幕
q  退出拷贝模式
[Esc]  退出拷贝模式
```

