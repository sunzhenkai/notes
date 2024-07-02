---
title: Jupyter使用
categories: 
  - [机器学习,工具,Jupyter]
tags:
  - 机器学习
  - 工具
  - Jupyter
date: 2020/11/17 22:00:00
update: 2020/11/17 22:00:00
---

# 安装

```shell
$ pip3 install jupyter
```

# 运行

```shell
$ jupyter notebook
```

# 设置密码

```shell
# 生成配置文件
$ jupyter notebook --generate-config

# 设置密码, 把密码加密后写入文件, 不会启动服务
$ jupyter notebook password
```

# 设置监听和端口

```shell
$ jupyter notebook --ip 0.0.0.0 --port 18800 
```

# Trouble Shotting

## 'charset_normalizer' has no attribute 'md__mypyc'

```shell
AttributeError: partially initialized module 'charset_normalizer' has no attribute 'md__mypyc' (most likely due to a circular import)
```

**解决**

```shell
$ pip3 install --force-reinstall charset-normalizer
```

# 推荐

```shell
$ jupyter lab --notebook-dir=$PWD --ip 0.0.0.0 --port 18800 --NotebookApp.token=token
```

