---
title: MetaSpore - Startup
categories: 
    - [研习录, 机器学习]
tags:
    - 机器学习
date: 2025/01/09 00:00:00
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

- arrow

- features

## metaspore

1. 提供离线训练、在线 serving 的共用代码
2. 离线使用
   1. 使用 pybind11 库定义并绑定 C++ 代码接口
   2. python 代码加载共享库，像调用 python 代码一样调用使用 pybind11 定义的 C++ 接口

# Getting Started

[文档链接](https://github.com/meta-soul/MetaSpore/blob/main/tutorials/metaspore-getting-started.ipynb)

## 定义模型

```python
embedding_size      : 每个特征组的 embedding size
# MetaSpore 相关
sparse              : ms.EmbeddingSumConcat
sparse.updater      : ms.FTRLTensorUpdater
sparse.initializer  : ms.NormalTensorInitializer
dense.normalization : ms.nn.Normalization
# Torch 相关
dense               : torch.nn.Sequential
```

初始化内容。

- EmbeddingSumConcat
  - SparseFeatureExtractor
    - 解析原始特征列配置文件
    - 向计算图中添加计算 Hash 特征的 Node
  - EmbeddingBagModule
- TensorUpdater，Sparse & Dense 数据更新类
  - FTRLTensorUpdater
- TensorInitializer，张量初始化器
  - NormalTensorInitializer，归一化张量初始化器
