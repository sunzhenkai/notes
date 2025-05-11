---
title: ubuntu network
categories: 
  - [linux,distro,ubuntu]
tags:
  - distro
date: "2021-08-28T00:00:00+08:00"
update: "2021-08-28T00:00:00+08:00"
---

# 静态地址

```shell
# vim /etc/netplan/99_config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
        - 10.10.10.2/24  # 静态地址
      gateway4: 10.10.10.1
      nameservers:       # 可选
          search: [mydomain, otherdomain]
          addresses: [10.10.10.1, 1.1.1.1]

$ sudo netplan apply
```

# 重启

```shell
# method 1
$ sudo netplan apply

# method 2
$ sudo nmcli networking off
$ sudo nmcli networking on

# method 3
$ sudo systemctl start NetworkManager 
$ sudo systemctl stop NetworkManager 

# method 4
$ sudo service network-manager restart

# method 5
$ sudo ifdown -a
$ sudo ifup -a

# method 6
$ sudo systemctl restart sytemd-networking
```

# 接口

```shell
# up / down
ip link set dev ens7 up    # up
ip link set dev ens7 down  # down
```

# 路由

```shell
# 展示路由配置
ip route show

# 添加路由
ip route add <network_ip>/<cidr> via <gateway_ip> dev <network_card_name>
## 示例
ip route add 192.168.6.0/24 dev eth0
ip route add default 

# 删除路由
ip route del default # 删除默认路由
```



# 设置 DNS

```shell
## ubuntu 20.04+
# cat /etc/netplan/***.yaml
network:
    version: 2
    ethernets:
        ens4:
            dhcp4: true
            match:
                macaddress: fa:16:3e:65:2c:6b
            mtu: 1450
            set-name: ens4
            nameservers:
                addresses: [192.168.6.1,8.8.8.8]  # 设置 dns

# 生效
sudo netplan apply
```

# 防火墙

```shell
# 查看防火墙状态
$ sudo ufw status
# active: 激活, inactive: 非激活

# disable
$ sudo ufw disable
```

# Netplan

- gateway4 弃用，使用 route 代替

```shell
# 弃用版本
gateway4: 192.168.6.1
# 新版设置
routes:
  - to: default
		via: 192.168.6.1
```



## 设置路由

```yaml
network:
  version: 2
  ethernets:
    enp0s31f6:
      match:
        macaddress: 6c:4b:90:85:5d:59
      dhcp4: true
      wakeonlan: true
      set-name: enp0
      nameservers:
        addresses: [223.5.5.5, 8.8.8.8]
      addresses: [192.168.6.8/24]
      routes:
        - to: default
          via: 192.168.6.1
          table: 100
      routing-policy:
        - to: 192.168.6.0/24
          table: 100
          priority: 100
    enxf8e43b1a1229:
      match:
        macaddress: f8:e4:3b:1a:12:29
      addresses: [192.168.9.99/24]
      set-name: ext0
      nameservers:
        addresses: [223.5.5.5, 8.8.8.8]
```

# wireshark

## 安装

```shell
apt install tshark
```

文档参考[这里](https://www.wireshark.org/docs/wsug_html_chunked/AppToolstshark.html)。

## 使用

```shell
tshark -i <entwork-interface>

# 筛选端口
tshark -i enp0 -f "src port 30800"
```

# Wake On Lan

```shell
# 配置
$ cat /etc/netplan/*_config.yaml
# Let NetworkManager manage all devices on this system
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    enp4s0:
      match:
        macaddress: 2a:04:a0:46:08:38
      dhcp4: true
      wakeonlan: true
    enp5s0:
      match:
        macaddress: 2a:04:a0:46:08:39
      dhcp4: true
      wakeonlan: true
        
# 生效
$ sudo netplan apply
```

> **注意**
>
> 1. 如果不生效，尝试添加 macaddress match
