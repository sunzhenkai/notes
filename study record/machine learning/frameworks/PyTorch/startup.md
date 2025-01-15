---
title: PyTorch - Startup
categories: 
    - [研习录, 机器学习]
tags:
    - 机器学习
date: 2025/01/09 00:00:00
---

# nn

## Module

所有神经网络模块的基类，自定义的模型也应把该类作为基类。

```python
forward(*input) : 定义每次调用时的计算逻辑，所有子类都应该重写
```

## Sequential

提供了一种简单的方式来按顺序堆叠神经网络的层，用于快速构建一个顺序的神经网络模型。在模型进行前向传播时，`nn.Sequential`会按照层的顺序依次调用每个层的`forward`方法，将前一层的输出作为下一层的输入，直到最后一层输出结果。

## Linear

## ReLU

# DDP

- rank，全局进程序号
- local_rank，本机进程序号，可以使用 `local_rank = torch.distributed.get_rank() % torch.cuda.device_count()` 计算（在每个机器进程数一致时）
- world size，全局并行数

# 附录

- https://www.alibabacloud.com/blog/alluxio-deep-learning-practices---1-running-pytorch-framework-on-hdfs_596532

- https://medium.com/@binfan_alluxio/deep-learning-at-alibaba-cloud-with-alluxio-running-pytorch-on-hdfs-3a99d7655fd4
- https://zhuanlan.zhihu.com/p/76638962
- https://www.paddlepaddle.org.cn/documentation/docs/zh/api_guides/low_level/layers/sparse_update.html
