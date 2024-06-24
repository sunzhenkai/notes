---
title: Kaggle - command line tool
categories: 
    - 研习录
tags:
    - 研习录
date: 2024/06/21 00:00:00
---

# 安装

详见[文档](https://www.kaggle.com/docs/api#getting-started-installation-&-authentication)，[Github 仓库](https://github.com/Kaggle/kaggle-api)。

```shell
$ pip install kaggle
```

在 [User Profile](https://www.kaggle.com/settings/account) 页面 `Create New Token`，并将下载的文件放到 `~/.kaggle/kaggle.json`。

# 使用

## 列出进行中的比赛

```shell
$ kaggle competitions list
```

## 列出比赛的文件

```shell
$ kaggle competitions files {competition}
```

## 下载数据

```shell
$ kaggle competitions download -f {filename} -c {competition} # 下载指定文件
$ kaggle competitions download -c {competition}   # 下载所有文件到当前工作路径
$ kaggle competitions download -p /path/to/save -c {competition} # 指定下载路径
```

