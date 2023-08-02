---
title: network - use wifi adapter
categories: 
  - [play,network]
tags:
  - server
date: 2022/08/27 00:00:00
---

# 360 随身 wifi 1 代

## 驱动

[这里](https://github.com/jeremyb31/mt7601u-5.4.git) ，[这里](https://github.com/art567/mt7601usta.git)。

```shell
$ lsusb
...
Bus 001 Device 003: ID 148f:760b Ralink Technology, Corp. MT7601U Wireless Adapter
...
```

**安装驱动**

```shell
sudo apt install git dkms
git clone https://github.com/jeremyb31/mt7601u-5.4.git
sudo dkms add ./mt7601u-5.4
sudo dkms install mt7601u/1.0

# 重启
sudo reboot 
```

# 360 随身 wifi 2 代

## 驱动

[这里](https://github.com/openwrt/mt76.git)。