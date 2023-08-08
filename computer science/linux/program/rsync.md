---
title: rsync
categories:
  - [linux, software]
tags:
  - linux
    - rsync
date: 2022/10/21 00:00:00
---

# Command

```shell
# local
rsync [OPTION]... SRC [SRC]... DEST

# remote
rsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST
rsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST
rsync [OPTION]... SRC [SRC]... rsync://[USER@]HOST[:PORT]/DEST
rsync [OPTION]... [USER@]HOST:SRC [DEST]
rsync [OPTION]... [USER@]HOST::SRC [DEST]
rsync [OPTION]... rsync://[USER@]HOST[:PORT]/SRC [DEST]
```

# 参数

```shell
-r 递归同步
-R 使用相对路径名称
-c 文件比较使用校验和替代时间和大小
-P 显示进度并保留未传输完成的文件

--delete	  删除目标文件夹无关的文件
--progress  显示进度
```

