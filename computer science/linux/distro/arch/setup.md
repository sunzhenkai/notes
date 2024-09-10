---
title: Arch Linux 初始化
categories: 
  - [linux,distro,centos]
tags:
  - distro
date: 2021/09/04 00:00:00
update: 2021/09/04 00:00:00
---

# 网络设置

## 使用 systemd-networkd 管理网络

新增文件 `/etc/systemd/network/20-wired.network`，下面是静态 IP 配置示例。

```
[Match]
Name=enp1s0

[Network]
Address=192.168.6.2/24
Gateway=192.168.6.1
DNS=192.168.6.1
```

启动 systemd-networkd

```shell
$ systemctl enable systemd-networkd
$ systemctl start systemd-networkd
```

# 配置 SSH 远程登录

```shell
$ pacman -S openssh
$ vim /etc/ssh/sshd_config # 添加如下内容
PasswordAuthentication yes
PermitRootLogin yes  # 允许 Root 用户远程登录（密钥、密码均可）
```

启动 sshd

```shell
systemctl enable sshd.service
systemctl start sshd.service
```

# 创建用户及用户组

```shell
$ groupadd -g 100 wii
$ useradd -m -d /home/wii -s /bin/zsh -g wii wii
```

# 普通用户获取超级管理员权限

```shell
$ pacman -S sudo
$ chmod 0600 /etc/sudoers
$ vim /etc/sudoers # 添加如下内容, 最好在文件最后
wii ALL=(ALL:ALL) NOPASSWD: ALL   # wii 用户使用 sudo 获取所有权限，且不需要密码
```

# 必备

```shell
$ pacman -S sudo git curl wget zip unzip base-devel gdb
```

