---
title: Linux之网络配置
categories: 
	- [linux,notes]
tags:
	- Linux
date: 2020/12/05 18:40:00
update: 2020/12/05 18:40:00
---

# DNS

## Debian+

```shell
# interfaces; configured by dns-nameserver
$ cat /etc/network/interfaces
...
auto wlan0
allow-hotplug wlan0
iface wlan0 inet static
	address 192.168.8.160
	netmask 255.255.255.0
	network 192.168.8.1
	gateway 192.168.8.1
	broadcast 192.168.8.255
	wpa-essid "<wifi-id>"
	wpa-psk "<wifi-password>"
	dns-nameserver 8.8.8.8
	dns-nameserver 8.8.4.4
	dns-nameserver 192.168.8.1
```

