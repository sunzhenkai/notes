---
title: linux xargs
categories: 
  - [linux,程序]
tags:
  - xargs
  - linux
date: "2020-10-31T00:00:00+08:00"
update: "2020-10-31T00:00:00+08:00"
---

# 描述

**功能**

- 配合管道使用，为命令传递参数

# 使用

```shell
$ find /sbin -perm +700 | ls -l         # NO; 这个命令是错误的
$ find /sbin -perm +700 | xargs ll      # NO; 无法配合alias使用
$ find /sbin -perm +700 | xargs ls -l   # OK; 这样才是正确的

# 杀死进程
$ ps aux | grep <program-name> | awk '{ print($2)}' | xargs kill
```

# 注意

- xargs 无法获取当前shell的alias，所有无法配合alias使用

# 参考

- https://www.runoob.com/linux/linux-comm-xargs.html