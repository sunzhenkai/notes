---
title: ubuntu cloud
categories: 
	- [linux,distro,ubuntu]
tags:
	- distro
date: 2021/09/04 00:00:00
update: 2021/09/04 00:00:00
---

# 初始化

使用 cloud init 初始化时，在实例启动后，可能需要等一小会，才能生效。

```
#cloud-config
chpasswd:
  list: |
    ubuntu:ubuntu
    wii:wii
  expire: False
```

# 开启 ssh 密码登录

```shell
$ sudo vi /etc/ssh/sshd_config
PasswordAuthentication yes
$ sudo service ssh restart  # 重启 ssh server
```

