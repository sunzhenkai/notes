---
title: cuda setup
categories: 
  - [architecture, gpu, cuda]
tags:
  - cuda
date: "2023-04-16T00:00:00+08:00"
update: "2023-04-16T00:00:00+08:00"
---

# 安装

在 [这里](https://developer.nvidia.com/cuda-downloads) 选择规格，并下载。以 amd64 的 ubuntu 为例，下面是在线安装命令。

```shell
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda
```

文档参考[这里](https://docs.nvidia.com/cuda/index.html)，代码示例参考[这里](https://developer.nvidia.com/cuda-code-samples)。 

# 文档

## 官方

- [编码手册](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html)
- [最佳实践](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)

## 博客

- [ref 1](https://face2ai.com/program-blog/#GPU%E7%BC%96%E7%A8%8B%EF%BC%88CUDA%EF%BC%89)
- [ref 2](https://zhuanlan.zhihu.com/p/34587739)
- [ref 3](https://zhuanlan.zhihu.com/p/53773183)
- [ref 4](https://zhuanlan.zhihu.com/p/97044592)
