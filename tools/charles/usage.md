---
title: charles usage
categories: 
	- [工具,charles]
tags:
	- charles
date: 2021/08/17 00:00:00
update: 2021/08/17 00:00:00
---

# 安装 & 配置

## 下载 & 安装 charles

[点击跳转](https://www.charlesproxy.com/download/)

## 配置

### chrome

下载插件 SwitchProxy，添加 charles 代理，并启用。

![image-20210817102317584](usage/image-20210817102317584.png)

# 转发 localhost

## 添加 host

在 `/etc/hosts` 中添加 `127.0.0.1 charles.prx`。

![image-20210817102356555](usage/image-20210817102356555.png)

## charles 中添加 `Map Remote`

![image-20210817103825440](usage/image-20210817103825440.png)

## 效果

![image-20210817103752293](usage/image-20210817103752293.png)