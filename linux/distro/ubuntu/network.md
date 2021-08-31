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

