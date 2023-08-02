---
title: 树莓派配置
categories: 
  - [play,树莓派]
tags:
  - 树莓派
date: 2020/12/05 18:40:00
update: 2020/12/05 18:40:00
---

# Wifi认证及静态IP

```shell
#### Raspbian
$ cat /etc/network/interfaces
# ...
source-directory /etc/network/interfaces.d

auto wlan0
allow-hotplug wlan0
iface wlan0 inet static
	address 192.168.8.160
	netmask 255.255.255.0
	network 192.168.8.1
	gateway 192.168.8.1
	broadcast 192.168.8.255
	wpa-essid "..."
	wpa-psk "..."

# wpa-essid: wifi名称
# wpa-psk: wifi 密码，psk认证
```

