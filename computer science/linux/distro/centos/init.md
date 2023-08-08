---
title: centos 初始化
categories: 
  - [linux,distro,centos]
tags:
  - distro
date: 2021/09/04 00:00:00
update: 2021/09/04 00:00:00
---

# 配置

```shell
# 关闭 selinux
$ sudo vim /etc/selinux/config
SELINUX=enforcing -> SELINUX=disabled
$ sudo setenforce 0

# 关闭 swap
$ sudo vim /etc/fstab
注释掉行 /dev/mapper/centos-swap

# 关闭防火墙
$ systemctl stop firewalld
$ systemctl disable firewalld

# 设置 DNS
# centos 8
$ vim /etc/resolve.conf
nameserver 192.168.6.1 # 或其他
```

# 开启 EPEL repository

- [amz doc](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-enable-epel/)
