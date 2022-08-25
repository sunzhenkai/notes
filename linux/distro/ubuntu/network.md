---
title: ubuntu network
categories: 
	- [linux,distro,ubuntu]
tags:
	- distro
date: 2021/08/28 00:00:00
update: 2021/08/28 00:00:00
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

