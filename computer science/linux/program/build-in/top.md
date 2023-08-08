---
title: top
categories: 
  - [linux,software]
tags:
  - linux
  - top
date: 2021/07/13 00:00:00
update: 2021/07/13 00:00:00
---

# 操作

```shell
c  展示详细 COMMAND
m  切换内存展示
e  切换进程内存展示单位
E  切换顶部内存信息的单位
P  按 CPU 排序
W  保存当前配置到用户目录 (~/.toprc OR ~/.config/prop/toprc OR ...)
```

# 排序

## 指定队列排序

- 输入命令 top
- 输入 o
  - 再输入列名（大小写不敏感）
- 输入 O
  - 再输入列名（大小写不敏感），设置第二排序键

# 指定 pid

**指定单个**

```shell
$ top -p <pid>      # macos 使用 -pid 参数
```

**指定多个**

```shell
$ top -p `pgrep -d ',' python3`  # 非 macos
```

# 指定用户

```shell
$ top -u wii       # 只显示指定用户进程, macos 使用 -U 参数
```

