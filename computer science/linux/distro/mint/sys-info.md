---
title: 系统信息
categories: 
  - [linux,distro,mint]
tags:
  - distro
date: 2021/08/24 00:00:00
update: 2021/08/24 00:00:00
---

# 获取发行版信息

```shell
# 当前发行版
$ cat /etc/issue
Linux Mint 20 Ulyana \n \l

# 当前发行版的 debian 版本
$ cat /etc/debian_version
bullseye/sid

# 当前发行版的上游版本信息
$ cat /etc/upstream-release/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=20.04
DISTRIB_CODENAME=focal
DISTRIB_DESCRIPTION="Ubuntu Focal Fossa"
```

