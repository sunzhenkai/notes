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

# Proxy

## 全局代理

```shell
export http_proxy=socks5://<host>:<port>
export https_proxy=socks5://<host>:<port>
```

### 适用

- cURL

## Git 代理

```shell
# 设置代理
git config --global https.proxy socks5://<host>:<port>
git config --global https.proxy socks5://<host>:<port>

# 取消
git config --global --unset http.proxy
git config --global --unset https.proxy
```

