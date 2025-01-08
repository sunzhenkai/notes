---
title: MetaSpore - Startup
categories: 
    - [研习录, MetaSpore]
tags:
    - MetaSpore
date: 2024/12/26 00:00:00
---

# 打包

1. 先编译 C++ 库，生成 `metaspore.so`
2. 再使用 setuptools 和 wheel 工具，打包 python 库

# MetaSpore C++

MetaSpore C++ 包含几个模块。

- common
- serving
- metaspore (shared)

## common

- globals

  - 定义 gflags 变量

- hashmap

  Hjk

- arrow

- features
