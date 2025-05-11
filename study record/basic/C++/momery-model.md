---
title: C++ - 内存模型
categories: 
    - [研习录,C++]
tags:
    - 研习录
    - C++
date: "2024-03-15T00:00:00+08:00"
---

程序在执行前，先从磁盘加载程序到内存，这个过程会执行非静态全局变量的初始化。在程序启动过程中，会对内存做逻辑区域的划分，并将不同的代码、数据加载到不同的区域。

## 内存区域划分

- 全局/静态存储区
- 代码区
- 堆
- 栈

# 参考

[C++ 内存模型](https://en.cppreference.com/w/cpp/language/memory_model)

[C++内存分区模型](https://zhuanlan.zhihu.com/p/647137725)
