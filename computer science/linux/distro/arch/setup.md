---
title: Arch Linux 初始化
categories: 
  - [linux,distro,centos]
tags:
  - distro
date: "2021-09-04T00:00:00+08:00"
update: "2021-09-04T00:00:00+08:00"
---

# 中文

```shell
# 修改文件 /etc/locale.gen
en_US.UTF-8 UTF-8
zh_CN.UTF-8 UTF-8
zh_CN.GBK GBK
zh_CN GB2312

# locale-gen
$ sudo locale-gen
```

## zsh

```shell
 # 文件 ~/.zshrc
 export LC_ALL=en_US.UTF-8
 export LANG=en_US.UTF-8
```

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
$ systemctl enable systemd-resolved
$ systemctl start systemd-resolved
```

检查 DNS

```shell
$ resolvectl status
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
$ pacman -S zsh
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
$ pacman -S sudo git curl wget zip unzip base-devel
# C++ 开发
$ pacman -S gdb cmake ninja texinfo
```

# Wake On Lan

```shell
sudo pacman -S ethtool
sudo ethtool -s eth0 wol g

# 持久化配置
# /etc/systemd/network/50-wired.link
[Match]
MACAddress=aa:bb:cc:dd:ee:ff

[Link]
NamePolicy=kernel database onboard slot path
MACAddressPolicy=persistent
WakeOnLan=magic
```

或使用 wol service。

```shell
# 安装
yay -Sy wol-systemd
# enable
sudo systemctl enable wol@eno1.service  # eno1 为网络接口
```

