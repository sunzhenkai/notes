---
title: Kitty
categories: 
  - [tools, kitty]
tags:
  - kitty
date: 2025/3/28 00:00:00
---

# Troubleshotting

## unknown terminal type

报错信息

```shell
'xterm-kitty': unknown terminal type.
```

解决方案

```shell
# append this into shell config file
alias ssh="kitty +kitten ssh" # 但是这样在其他终端没法使用 ssh 甚至某些 ide 无法克隆东西
alias kssh="kitty +kitten ssh"
```

