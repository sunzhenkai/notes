---
title: server
categories: 
	- [play,server]
tags:
	- server
date: 2021/08/24 00:00:00
update: 2021/08/24 00:00:00
---

# BIOS 配置

## 断电恢复后自启动

- 开机长按 `Delete` 进入 BIOS
- `InelRCSetup -> PCH Configuration -> PCH Devices -> Restore AC after Power Loss`
- 设置为 `Power On`

设置断电恢复后启动，目的是设置远程启动。

# 系统

Centos 7。

# 配置

```shell
# 关闭 selinux
$ sudo vim /etc/selinux/config
SELINUX=enforcing -> SELINUX=disabled

# 关闭 swap
$ sudo vim /etc/fstab
注释掉行 /dev/mapper/centos-swap

# 关闭防火墙
$ systemctl stop firewalld
$ systemctl disable firewalld
```

# 程序

## zsh

```shell
$ sudo yum install zsh
```

## docker

```shell
# 一键安装脚本
$ curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

## 参考

- [docker 安装](https://www.runoob.com/docker/ubuntu-docker-install.html)

## vnc

**服务端**

```shell
sudo apt install xfonts-base xfonts-75dpi xfonts-100dpi
sudo apt install tightvncserver
```

**客户端**

从[这里](https://www.tightvnc.com/download.php)下载。

## 配置远程启动

整机无负载功率在 100w 左右，并不常用。远程关闭、启动方案是通过设置 BIOS 的断电恢复后自动启动 + 小米智能插座实现。
