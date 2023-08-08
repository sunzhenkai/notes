---
title: centos user manager
categories: 
  - [linux,distro,centos]
tags:
  - distro
date: 2021/10/17 00:00:00
update: 2021/10/17 00:00:00
---

# 用户管理

```shell
# 创建 group
$ groupadd wii
# 添加用户
$ useradd -d /home/wii -m -s /bin/bash -g wii wii
# 添加至 sudoers
$ sudo usermod -aG wheel wii

# sudo 无需密码
$ sudo visudo
```

