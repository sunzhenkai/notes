---
title: ubuntu user manager
categories: 
	- [linux,distro,ubuntu]
tags:
	- distro
date: 2021/09/29 00:00:00
update: 2021/09/29 00:00:00
---

```shell
# 添加 group
$ groupadd wii

# 添加用户
$ useradd -d /home/wii -m -s /bin/bash -g wii wii

# 添加 sudo
$ sudo usermod -aG sudo <username>
```

