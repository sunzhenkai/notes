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

# 调试程序

```shell
$ gdb <program>

# 添加程序参数
$ gdb --args program <args>
```

# 调试 core 文件

```shell
$ gdb <program> <core-file>
$ gdb <program> -c <core-file>
$ gdb <program>
(gdb) core <core-file>
```

# 打印变量

```shell
# 查看所有调用栈
bt
# 选中某个栈
select-frame <frame-no>

# 查看本地变量
info locals
# 查看全局变量
info variables
# 查看参数
info args

# 打印变量
display <variable-name>
```

# 常见问题

## gdb 卡住

```shell
Reading symbols from <bin>...done.
[New LWP 19134]
[New LWP 19669]
[New LWP 19672]
[New LWP 19670]
[New LWP 19200]
[New LWP 19668]
[New LWP 19667]
[New LWP 19673]
[New LWP 19676]
[New LWP 19680]
[New LWP 19197]
[New LWP 19671]
[New LWP 19674]
```

yum 同样卡住，使用 `ps aux | grep yum`，`kill -9` 之后，恢复正常。

# 断点

## Attach 方式

```shell
# 定义断点文件 bp.info
break main.cpp:15

# attach 进程
gdb attach 10232 -x bp.info
```

**命令**

```shell

```

# 参考

- [打印变量](https://stackoverflow.com/questions/6261392/printing-all-global-variables-local-variables)
