---
title: zellij - usage
categories: 
  - [工具,zellij]
tags:
  - zellij
date: "2025-03-30T00:00:00+08:00"
---

# Install

```shell
# cargo
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# zellij
cargo install --locked zellij
```

# Commands

**Open Session**

```shell
zellij -s {sessioin-name} # open new session with name
```

**Attach**

```shell
zellij a {session-name}
```

# Tips

## Copy Contest

```shell
# enter search mode -> edit
Ctrl+s -> e
# change editor
scrollback_editor "nvim"
```

# Troubleshotting

## Shortkey Conflict

```shell
# enter locked mode
Ctrl+g
```

