---
title: [ML] 准备 - 环境
categories: 
  - 研习录
tags:
  - 研习录
  - 机器学习 
date: 2024/05/28 00:00:00
---

# Conda

## 安装

**linux**

```shell
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

## 环境

### 创建环境

```shell
$ conda create -n ml
```

