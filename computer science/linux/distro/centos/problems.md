---
title: centos 常见问题
categories: 
  - [linux,distro,centos]
tags:
  - distro
date: 2021/08/28 00:00:00
update: 2021/08/28 00:00:00
---

[toc]

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

# yum

## yum 命令卡住

```shell
# 问题出在 Amazon Linux 2，所有 yum 命令卡住
ps aux | grep yum

kill -9 <pid>  # kill 所有 yum 进程
```

## 其他问题

**Failed to download metadata for repo 'appstream'**

```shell
# 保存
CentOS Linux 8 - AppStream                                                                                          9.5  B/s |  38  B     00:03
Error: Failed to download metadata for repo 'appstream': Cannot prepare internal mirrorlist: No URLs in mirrorlist

# 解决
dnf --disablerepo '*' --enablerepo=extras swap centos-linux-repos centos-stream-repos -y
dnf distro-sync -y
```

# Openstack 初始化后无法联网

```shell
sudo vi /etc/sysconfig/network-scripts/ifcfg-eth0

# 添加 DNS1
DNS1=192.168.6.1

# 重启网络服务
sudo systemctl restart NetworkManager
```

# Centos 7 安装 gcc 7

```shell
sudo yum install gcc72-c++
```

# 软件包

```shell
# lcov
yum install lcov.noarch
```

