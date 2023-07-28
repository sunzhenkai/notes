---
title: centos network
categories: 
	- [linux,distro,centos]
tags:
	- distro
date: 2021/09/04 00:00:00
update: 2021/09/04 00:00:00
---

# DNS

```shell
# centos 8
$ vim /etc/resolve.conf
nameserver 192.168.6.1 # 或其他
```

## resolveconf

```shell

```

# 修改网络配置

```shell
# 文件
$ vi /etc/sysconfig/network-scripts/ifcfg-[network_device_name]

# 配置
ONBOOT=yes
BOOTPROTO=dhcp
GATEWAY=...
DNS1=...
DNS2=...

# 重启网络
$ systemctl restart network
$ systemctl restart NetworkManager # centos 8
```

# sudo 权限无需密码

```shell
$ sudo visudo
# 添加如下内容，替换掉下面的用户名
<username> ALL=(ALL) NOPASSWD:ALL
```

