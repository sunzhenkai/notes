---
title: gdb
categories: 
  - [coding, tools]
tags:
  - c++
    - gdb
date: 2022/1/10 00:00:00
update: 2022/1/10 00:00:00
---

# 忽略 SIGNAL

```shell
Signal: SIG34 (Real-time event 34)
```

在使用 gdb 调试时，如果频繁被信号中断，可屏蔽对应信号，以 SIG34 为例。

```shell
# file: ~/.gdbinit
handle SIG34 nostop noprint pass noignore
```

```shell
handle SIG34 nostop noprint pass noignore
handle SIG35 nostop noprint pass noignore
```

# 调试程序

```shell
$ gdb <program>

# 为程序添加参数
$ gdb --args program <args>
```

# 调试 core 文件

```shell
$ gdb <program> <core-file>
$ gdb <program> -c <core-file>
$ gdb <program>
(gdb) core <core-file>
```

# 命令

[参考一](https://visualgdb.com/gdbreference/commands/)

## 常用命令

## b

```shell
# b, 断点相关
b main - Puts a breakpoint at the beginning of the program
b - Puts a breakpoint at the current line
b N - Puts a breakpoint at line N
b +N - Puts a breakpoint N lines down from the current line
b fn - Puts a breakpoint at the beginning of function "fn"
d N - Deletes breakpoint number N
info break - list breakpoints
```

```shell
r - Runs the program until a breakpoint or error
c - Continues running the program until the next breakpoint or error
f - Runs until the current function is finished
s - Runs the next line of the program
s N - Runs the next N lines of the program
n - Like s, but it does not step into functions
u N - Runs until you get N lines in front of the current line
p var - Prints the current value of the variable "var"
bt - Prints a stack trace
u - Goes up a level in the stack
d - Goes down a level in the stack
q - Quits gdb
```

## p

打印给定的表达式

```shell
print [Expression]
print $[Previous value number]
print {[Type]}[Address]
print [First element]@[Element count]
print /[Format] [Expression]
```

- Expression
  - 变量
  - 寄存器，$eax 等
  - 伪寄存器，$pc 等
- Format
  - 合法的格式符
    - o - octal
    - x - hexadecimal
    - u - unsigned decimal
    - t - binary
    - f - floating point
    - a - address
    - c - char
    - s - string

> **注意**
>
> - 打印本地变量时，需要确保选定了正确的帧（frame）

[参考一](https://visualgdb.com/gdbreference/commands/print)

## x

使用指定的格式，打印给定地址的内存内容。

```shell
x [Address expression]
x /[Format] [Address expression]
x /[Length][Format] [Address expression]
x
```

- Address expression
  - 寄存器，$eip
  - 伪寄存器地址，$pc
- Format
  - 格式
    - o - octal
    - x - hexadecimal
    - d - decimal
    - u - unsigned decimal
    - t - binary
    - f - floating point
    - a - address
    - c - char
    - s - string
    - i - instruction
  - 大小修饰符（size modifiers）
    - b - byte
    - h - halfword (16-bit value)
    - w - word (32-bit value)
    - g - giant word (64-bit value)
- Length
  - 指定打印的元素个数

[参考一](https://visualgdb.com/gdbreference/commands/x)

# 帧相关

```shell
(gdb) f n       # 选中第 n 个帧
(gdb) up       # 上一个帧
(gdb) down     # 下一个帧
```

# 打印变量

```shell
# 查看所有调用栈
bt
# 选中某个栈
select-frame <frame-no>

# 打印变量
display <variable-name>
```

## 列出变量

```shell
# 查看本地变量
info locals
# 查看全局变量
info variables
# 查看参数
info args
```

## 分类型打印

```shell
# 打印 char *
(gdb) p *(char**)0x21d4b4910

# map 相关
(gdb) p m._M_h           
(gdb) p (m._M_h._M_bbegin._M_node._M_nxt) 
(gdb) p m._M_h._M_buckets
(gdb) p m._M_h._M_buckets[0]

# vector 相关
(gdb) p *(v._M_impl._M_start+4) 
(gdb) p *(v._M_impl._M_start+4)._M_ptr.name # name: struct field

# 智能指针
(gdb) p sptr._M_ptr->name # name: struct field
```

### Vector

```shell
p *(*(m._M_impl._M_start+6)._M_impl._M_start) # vector<vector> 打印第 7 个元素 (vector)
```

## Pretty Printer

Pretty Printer 功能是否支持是在 gdb 编译时，根据编译选项决定的。在编译时需要添加编译参数 `--with-python` 来启用 Pretty Printer。下面的命令可以查看是否开启。

```shell
$ gdb -config
This GDB was configured as follows:
   configure --host=x86_64-pc-linux-gnu --target=x86_64-pc-linux-gnu
             ...
             --without-python
             --without-python-libdir
             ...
```

指定自定义的 python 路径，要指定到 python 二进制文件。

```shell
--without-python=/path/to/python/bin/python3
```

> 低版本的 python 在 configure 时会校验不通过，建议使用较新版本的 python3。

pretty printer 使用手册参考[这里](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Pretty-Printing.html#Pretty-Printing)。

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

# 常见问题

## value optimized out

```shell
# build type = debug
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -O0")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS_DEBUG} -O0")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS_DEBUG} -O0")
```

# 参考

- [打印变量](https://stackoverflow.com/questions/6261392/printing-all-global-variables-local-variables)

