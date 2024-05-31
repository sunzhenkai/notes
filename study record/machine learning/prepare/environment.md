---
title: [ML] 准备 - 环境
categories:
    - 研习录
    - 机器学习
tags:
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

配置 Shell

```shell
# for bash
~/miniconda3/bin/conda init bash
# for zsh
~/miniconda3/bin/conda init zsh
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

### 修改默认环境

```shell
$ conda config --set auto_activate_base false  # 关闭默认使用 base
$ conda activate {env-name}
```

# Kaggle

## 安装

详见[文档](https://www.kaggle.com/docs/api#getting-started-installation-&-authentication)，[Github 仓库](https://github.com/Kaggle/kaggle-api)。

```shell
$ pip install kaggle
```

在 [User Profile](https://www.kaggle.com/settings/account) 页面 `Create New Token`，并将下载的文件放到 `~/.kaggle/kaggle.json`。
