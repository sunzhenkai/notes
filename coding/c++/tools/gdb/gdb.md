---
title: gdb
categories: 
	- [coding, c++, tools, gdb]
tags:
	- c++
    - gdb
date: 2022/1/10 00:00:00
update: 2022/1/10 00:00:00
---

# 忽略 SIGNAL

在使用 gdb 调试时，如果频繁被信号中断，可屏蔽对应信号，以 SIG34 为例。

```shell
# file: ~/.gdbinit
handle SIG34 nostop noprint pass noignore
```

