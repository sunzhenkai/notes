---
title: vpn
categories: 
	- [工具,vpn]
tags:
	- vpn
date: 2022/10/29 00:00:00
update: 2022/10/29 00:00:00
---

# socks5

## server

```shell
# 安装
sudo apt install dante-server

# 配置
sudo vim /etc/danted.conf
# 修改配置
logoutput: /var/log/danted.log
internal: eth0 port = 1080
external: eth0
clientmethod: none
socksmethod: username
user.privileged: root
user.notprivileged: nobody

client pass {
	from: 0.0.0.0/0 to: 0.0.0.0/0
	log: error connect disconnect
}

socks pass {
	from: 0.0.0.0/0 to: 0.0.0.0/0
	command: connect
	log: error connect disconnect
	socksmethod: username
}

# 启动服务
sudo service danted start
```

**不启用认证配置**

```shell
logoutput: /var/log/danted.log
internal: enp2s0 port = 1080
external: enp2s0
clientmethod: none
method: none
user.privileged: root
user.notprivileged: nobody

client pass {
	from: 0.0.0.0/0 to: 0.0.0.0/0
	log: error connect disconnect
}

socks pass {
	from: 0.0.0.0/0 to: 0.0.0.0/0
	command: connect
	log: error connect disconnect
	method: none
}
```

