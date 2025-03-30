---
title: ubuntu setup
categories: 
  - [linux,distro,ubuntu]
tags:
  - distro
date: 2022/08/28 00:00:00
---

# 创建用户

```shell
# 添加 group
$ groupadd {groupname}
# 添加用户
$ useradd -d /home/{username} -m -s /bin/bash -g {username} {groupname}
# 添加 sudo
$ sudo usermod -aG sudo {username}
# 设置密码
$ sudo passwd {username}
```

**示例**

```shell
groupadd wii
useradd -d /home/wii -m -s /bin/bash -g wii wii
sudo usermod -aG sudo wii
sudo passwd wii
```

**sudo 权限无需密码**

```shell
$ visudo
<username>    ALL=(ALL) NOPASSWD: ALL
```

# 设置时区

**timedatectl**

```shell
# 查看当前时区信息
$ timedatectl
               Local time: 一 2023-06-26 16:21:01 CST
           Universal time: 一 2023-06-26 08:21:01 UTC
                 RTC time: 一 2023-06-26 08:21:01
                Time zone: Asia/Shanghai (CST, +0800)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
# 查看所有可配置的时区名称
$ timedatectl list-timezones
Africa/Abidjan
Africa/Accra
Africa/Addis_Ababa
Africa/Algiers
Africa/Asmara
Africa/Asmera
Africa/Bamako
Africa/Bangui
Africa/Banjul
Africa/Bissau
...
# 设置时区
$ sudo timedatectl set-timezone Asia/Shanghai
```

**tzselect**

临时需改时区，重启后失效。

```shell
$ tzselect
```

# 安装依赖

```shell
$ git clone https://github.com/sunzhenkai/env-init.git
$ cd env-init && ./activate
$ source ~/.bashrc
$ ii ubuntu -c
```

# 生成 ssh key

```shell
$ ssh-keygen -t ed25519 -C "your_email@example.com"
```

```shell
ssh-keygen -t ed25519 -C "zhenkai.sun@qq.com"
```

