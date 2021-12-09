---
title: linux problems
categories: 
	- [linux,notes]
tags:
	- Linux
date: 2021/12/01 00:00:00
update: 2021/12/01 00:00:00
---

# 挂载磁盘导致无法进入系统

拔出新加的磁盘，修改 `/etc/fstab` ，使用 UUID 区分盘符，示例如下。

