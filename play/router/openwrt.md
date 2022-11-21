---
title: openwrt
categories: 
	- [play,soft router]
tags:
	- soft router
date: 2022/10/16 00:00:00
---

# 开启 Samba

```shell
# 安装依赖
open install shadow-common shadow-useradd

# 添加用户
useradd share
smbpasswd -a share
```

