---
title: C++ - 排障
categories: 
    - [研习录,C++]
tags:
    - 研习录
    - C++
date: 2024/03/18 00:00:00
---

# Core Dump

- gdb 调试 core dump 文件
- asan 调试内存问题

对于通过 core dump 不好排查原因的问题。

- 找到触发 core 的 case（i.e. 请求）
- 缩小问题范围