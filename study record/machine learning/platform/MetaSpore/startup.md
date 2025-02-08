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

# 编译

## 镜像

- 环境变量

  ```shell
  export REPOSITORY={hub-repo}
  export VERSION={version}
  ```

- 构建 Dev 镜像（基础环境）

```shell
DOCKER_BUILDKIT=1 docker build --network host --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} --build-arg RUNTIME=gpu -f docker/ubuntu20.04/Dockerfile_dev -t $REPOSITORY/metaspore-dev-gpu:${VERSION} .

DOCKER_BUILDKIT=1 docker build --network host --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} --build-arg RUNTIME=cpu -f docker/ubuntu20.04/Dockerfile_dev -t $REPOSITORY/metaspore-dev-cpu:${VERSION} .
```

- Serving

  - Build 镜像（基于 Dev 镜像进行编译）
  - Service 镜像

- Training

  - Build 镜像（基于 Dev 镜像进行编译）

    ```shell
    DOCKER_BUILDKIT=1 docker build --network host --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} -f docker/ubuntu20.04/Dockerfile_training_build --build-arg DEV_IMAGE=$REPOSITORY/metaspore-dev-cpu:${VERSION} -t $REPOSITORY/metaspore-training-build:${VERSION} .
    ```
    
  - Spark Training 镜像
  
    ```shell
    DOCKER_BUILDKIT=1 docker build --network host --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} -f docker/ubuntu20.04/Dockerfile_training_release --build-arg METASPORE_RELEASE=build --build-arg METASPORE_BUILD_IMAGE=$REPOSITORY/metaspore-training-build:${VERSION} -t $REPOSITORY/metaspore-training-release:${VERSION} --target release .
    ```
  
- Jupyter

  ```shell
  DOCKER_BUILDKIT=1 docker build --network host --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} -f docker/ubuntu20.04/Dockerfile_jupyter --build-arg RELEASE_IMAGE=$REPOSITORY/metaspore-training-release:${VERSION} -t $REPOSITORY/metaspore-training-jupyter:${VERSION} docker/ubuntu20.04
  ```

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

## 步骤

- 定义模型（PyTorch Module）
- 定义 Estimator
  - PyTorchEstimator，封装 PyTorch 模型，并在分布式环境下训练（调用 fit 方法并传入 DataFrame 进行训练）
  - 调用 launcher.launch() 在个节点启动 PS 进程（server、worker、coordinator）

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
- Normalization，归一化

## 训练模型

```python
PyTorchEstimator
```

- 定义 PyTorchEstimator
  - module
  - worker / server 数量
  - 模型输出路径
  - Label 列索引

```python
PyTorchAgent
PyTorchLauncher
PyTorchHelperMixin
PyTorchModel
PyTorchEstimator
```

## 核心概念

- JobRunner
- PyTorchEstimator
  - pyspark.ml.base.Estimator
- Launcher
  - PSLauncher
- Agent
- Module
  - EmbeddingOperator
  - TensorUpdater
  - TensorInitializer
  - Normalization
- PyTorchModel
  - pyspark.ml.base.Model
- Metric
