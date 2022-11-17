---
title: rustscan
categories:
	- [tools, rustscan]
tags:
	- rustscan
comments: true
date: 2022/10/29 00:00:00
update: 2022/10/29 00:00:00
---

# 描述

端口扫描工具，[地址](https://github.com/RustScan/RustScan)。

# 安装

## brew

```shell
brew instsall rustscan
```

## docker

```shell
docker pull rustscan/rustscan:2.0.0
```

# 使用

```shell
rustscan -a 192.168.6.100 --ulimit 5000

# 指定端口
rustscan -a 192.168.6.100 --ulimit 5000 -p 21,22,80

# 指定范围
rustscan -a 192.168.6.100 --ulimit 5000 -p 1-65535
```

# 查看监听的端口

```shell
sudo netstat -tunlp
```

