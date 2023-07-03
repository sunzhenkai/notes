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

# WireGuard

```shell
# 安装
apt install wireguard -y

# 添加网络接口
ip link add dev wg0 type wireguard
ip address add dev wg0 10.0.2.1/24

# 生成密钥
wg genkey | tee server-private.key | wg pubkey | tee server-public.key
```

**预设**

```shell
# vpn 网络
10.110.10.1/24
# 示例 client 地址
10.110.10.100/24
# 网络接口
ens18
# server 地址
192.168.6.192

# server 端密钥对
PUBLICKEY = HsNTZwNRji31XuNAhx+eMOD8y7CZEeoPEUzZWZXpqg0=
PRIVATEKEY = UHIqicenzBJQ6gnsSHqrvZbEEbjz6NJfl1qc4UgpMm8=

# client 端密钥对
PUBLICKey = KLL6tm7wiU/ouenCktUwThss5Jw9Xr79C+3u3QRnYCQ= 
PRIVATEKEY = oNLv6Ntj5iHulThhcCtZ0jYtRV0CTsC4d6rJkWo21FY=
```

**配置模板**

```shell
[Interface]
## Address : A private IP address for wg0 interface.
Address = 10.110.10.1/24
 
## Specify the listening port of WireGuard, I like port 33333, you can change it.
ListenPort = 51820
 
## A privatekey of the server ( cat /etc/wireguard/server-private.key)
PrivateKey = {private-key-of-server}

## The PostUp will run when the WireGuard Server starts the virtual VPN tunnel.
## The PostDown rules run when the WireGuard Server stops the virtual VPN tunnel.
## Specify the command that allows traffic to leave the server and give the VPN clients access to the Internet. 
## Replace enp1s0 = Your-Network-Interface-Name

PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o {Your-Network-Interface-Name} -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o {Your-Network-Interface-Name} -j MASQUERADE
```

```shell
[Interface]
Address = 10.110.10.1/24
ListenPort = 51820
PrivateKey = UHIqicenzBJQ6gnsSHqrvZbEEbjz6NJfl1qc4UgpMm8=

PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o ens18 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o ens18 -j MASQUERADE
```

**服务**

```shell
systemctl start wg-quick@wg0
systemctl enable wg-quick@wg0
systemctl status wg-quick@wg0.service

# 查看状态
wg show wg0
```

**客户端配置**

```shell
# 重新生成密钥和公钥
[Interface]
PrivateKey = PrivateKey_of_the_Client
Address = IP_UNDER_VPN

[Peer]
###Public of the WireGuard VPN Server
PublicKey = PublicKey_of_the_Server

### IP and Port of the WireGuard VPN Server
Endpoint = IP_of_the_Sever:Port_VPN_of_the_Server

### Allow all traffic
AllowedIPs = 0.0.0.0/0
```

```shell
# 重新生成密钥和公钥
[Interface]
PrivateKey = oNLv6Ntj5iHulThhcCtZ0jYtRV0CTsC4d6rJkWo21FY=
Address = 10.110.10.100/24

[Peer]
PublicKey = HsNTZwNRji31XuNAhx+eMOD8y7CZEeoPEUzZWZXpqg0=
Endpoint = 192.168.6.192:51820
AllowedIPs = 0.0.0.0/0
```

**服务端添加 Peer**

```shell
wg set wg0 peer {client-public-key} allowed-ips 10.110.10.100

# 示例
wg set wg0 peer KLL6tm7wiU/ouenCktUwThss5Jw9Xr79C+3u3QRnYCQ= allowed-ips 10.110.10.100
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

