---
title: centos 常见问题
categories: 
	- [linux,distro,centos]
tags:
	- distro
date: 2021/08/28 00:00:00
update: 2021/08/28 00:00:00
---

# 编码

```shell
# Failed to set locale, defaulting to C

# vim /etc/profile
# 输入
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_COLLATE=C
export LC_CTYPE=en_US.UTF-8
```

# yum 卡住

```shell
# 问题出在 Amazon Linux 2，所有 yum 命令卡住
ps aux | grep yum

kill -9 <pid>  # kill 所有 yum 进程
```

