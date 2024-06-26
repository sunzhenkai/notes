---
title: Conda
categories: 
  - [机器学习,工具,Conda]
tags:
  - 机器学习
  - 工具
  - Conda
date: 2024/06/27 22:00:00
---

## 安装

**linux**

```shell
mkdir -p ~/.miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/.miniconda3/miniconda.sh
bash ~/.miniconda3/miniconda.sh -b -u -p ~/.miniconda3
rm -rf ~/.miniconda3/miniconda.sh
```

配置 Shell

```shell
# for bash
~/.miniconda3/bin/conda init bash
# for zsh
~/.miniconda3/bin/conda init zsh
```

## 环境

### 列出环境

```shell
$ conda info --envs
```

### 创建环境

```shell
$ conda create -n ml
```

**指定 channel**

```shell
$ conda create -n ml --channel=conda-forge
```

**克隆环境**

```shell
$ conda create --name new_name --clone old_name
```

### 启用环境

```shell
$ conda activate {env-name}
```

### 环境重命名

```shell
conda rename -n old_name new_name 
```

### 使用 yml 文件更新环境

```shell
$ conda env update --file env.yml --prune
```

### 删除环境

```shell
$ conda remove --name {env-name} --all
```

### 默认不启用 conda base 环境

```shell
$ conda config --set auto_activate_base false  # 关闭默认使用 base
```

## 打印环境信息

```shell
$ conda info
```

# Channel

### 为环境添加 channel

```shell
$ conda config --append channels conda-forge 
```

## 添加 channel

```shell
$ conda config 
```

## 打印 channel

```shell
$ conda config --show channels
```

# 包管理

conda 的包管理有 channel 的概念，如果不指定则为默认的 `defaults`。如果我们想要安装其他 channel 的包，示例如下。

```shell
$ conda install anaconda::gcc_linux-64
```

### 查询可用包

```shell
$ conda search {package}
```

或在 [这里](https://anaconda.org/) 搜索，页面有安装命令，比如。

```shell 
$ conda install anaconda::gcc_linux-64
# 另外一个包
$ conda install conda-forge::gcc_linux-64
```

### 已安装包

```shell
$ conda list
```

### 移除包

```shell
$ conda uninstall {package}
```

### 安装包

```shell
# 默认包
$ conda install {package}

# 指定channel
$ conda install {channel}::{package}

# 指定版本
$ conda install {package}={version}
```

# Trouble Shotting

## GLIBCXX_3.4.30 not found

```shell
ImportError: /home/wii/.miniconda3/envs/ml/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.30' not found (required by /home/wii/.miniconda3/envs/ml/lib/python3.12/site-packages/paddle/base/libpaddle.so)
```

可以通过如下命令，查看当前 gcc 支持的 GLIBCXX 版本。

```shell
$ strings /path/to/libstdc++.so.6 | grep GLIBCXX
```

这个报错通常是运行的程序依赖的 gcc 版本和已经安装的 gcc 版本不匹配，要么太高，要么太低。安装兼容版本的 gcc 即可。

## libstdcxx-ng 11.2.0.*  is not installable

```shell
libstdcxx-ng 11.2.0.*  is not installable because it conflicts with any installable versions previously reported
```

这个报错是在 conda 环境，安装 gcc 13.3.0 时报的错。原因是已经安装 `libstdcxx-ng 11.2.0.*` ，和要安装的 gcc 13.3.0 出现依赖冲突。可以先卸载。

```shell
$ conda uninstall libstdcxx-ng # 当然，大概率会失败
```

可以重新创建环境，并添加 channel conda-forge。

```shell
$ conda create --name {env-name} --channel=conda-forge conda-forge::gcc=13.2.0
```

# 推荐

```shell
$ conda create --name ml --channel=conda-forge conda-forge::gcc=13.2.0 conda-forge::python=3.12.4
```

