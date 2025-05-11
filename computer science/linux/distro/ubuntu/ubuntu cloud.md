---
title: ubuntu cloud
categories: 
  - [linux,distro,ubuntu]
tags:
  - distro
date: "2021-09-04T00:00:00+08:00"
update: "2021-09-04T00:00:00+08:00"
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

# sudo 命令较慢
```shell
sudo vim /etc/hosts
# 在 127.0.0.1 后面追加 hostname
```

# 开启 ssh 密码登录

```shell
$ sudo vi /etc/ssh/sshd_config
PasswordAuthentication yes
$ sudo service ssh restart  # 重启 ssh server
```

# 设置时区

```shell
sudo dpkg-reconfigure tzdata
# 选择 Asia -> Shanghai
```

# 设置 DNS
```shell
sudo vim /etc/netplan/50_cloud_init.yaml

# 添加 nameserver
network:
    version: 2
    ethernets:
        ens3:
            dhcp4: true
            match:
                macaddress: fa:16:3e:6c:21:ff
            mtu: 1450
            set-name: ens3
            nameservers:
                    addresses: [223.5.5.5, 223.6.6.6]
```

# 配置更新源
`sudo vim /etc/apt/sources.list`
## 20.04
### aliyun
```shell
deb https://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

# deb https://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
# deb-src https://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
```