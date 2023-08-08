---
title: vpn
categories: 
  - [工具,vpn]
tags:
  - vpn
  - wireguard
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
internal: ens18 port = 1080
external: ens18
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

# ShadowSocks

```shell
# 安装
sudo apt install shadowsocks-libev

# 配置
sudo nano /etc/shadowsocks-libev/config.json
{
    "server":["::1", "127.0.0.1"],
    "mode":"tcp_and_udp",
    "server_port":8388,
    "local_port":1080,
    "password":"ACRrobo9ymXb",
    "timeout":60,
    "method":"chacha20-ietf-poly1305"
}

# 服务
sudo systemctl restart shadowsocks-libev.service
sudo systemctl enable shadowsocks-libev.service
systemctl status shadowsocks-libev.service

```

# Http

## squid

### ubuntu

- [ubuntu](https://ubuntu.com/server/docs/proxy-servers-squid)

```shell
# 安装
sudo apt install squid

# 配置
sudo vim /etc/squid/squid.conf
## 配置项
http_port <port>
dns_nameservers 8.8.8.8 8.8.4.4

# 认证
sudo apt install apache2-utils
# 生成账号 & 密码并写入文件
sudo touch /etc/squid/passwords
sudo htpasswd /etc/squid/passwords <user-name>  
# htpasswd -c 选项会重新生成文件

# 修改配置
sudo vim /etc/squid/squid.conf
## 添加如下内容
auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwords
auth_param basic realm proxy
acl authenticated proxy_auth REQUIRED
http_access allow authenticated
# 放在 http_access deney all 之前

# 其他配置
tcp_outgoing_address    198.18.192.194		# 设置出网端口(网络端口分配的ip)

# 启动服务
sudo systemctl start squid.service
# 或重启服务
sudo systemctl restart squid.service

# 开机启动
sudo systemctl enable squid.service

# 测试
curl -v -x http://<user-name>:<password>@<host>:3128 https://www.google.com/
```

