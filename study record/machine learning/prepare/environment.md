---
title: 机器学习 - 环境
categories: 
    - 研习录
tags:
    - 研习录
date: "2024-05-28T00:00:00+08:00"
---

# Conda

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

### 为环境添加 channel

```shell
$ conda config --append channels conda-forge
```

## 包管理

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



# Kaggle

## 安装

详见[文档](https://www.kaggle.com/docs/api#getting-started-installation-&-authentication)，[Github 仓库](https://github.com/Kaggle/kaggle-api)。

```shell
$ pip install kaggle
```

在 [User Profile](https://www.kaggle.com/settings/account) 页面 `Create New Token`，并将下载的文件放到 `~/.kaggle/kaggle.json`。



