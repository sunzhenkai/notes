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

## 使用步骤

- 使用 `wg genkey` 和 `wg pubkey` 在每个节点创建公钥和私钥
- 配置
  - 主中继服务器（main relay server）
    - `[Interface]`
      - 确保在定义服务器可接收的路由地址时，指定整个 VPN 网络的 CIDR 范围
        - `Address = 192.0.2.1/24`
    - `[Peer]`
      - 为每个需要加入到 VPN 网络的客户端创建一个 `[Peer]`，使用对应的公钥（public key）
  - 客户端节点（client node）
    - `[Interface]`
      - 指定单个 IP，不中继流量
        - `Address = 192.0.2.3/32`
    - `[Peer]`
      - 为每个可以公开访问的 Peer 创建一个 `[Peer]` 
      - 在定义作为跳板服务器（Bounce Server）的远程对等体时，确保为整个VPN子网指定一个CIDR范围
        - `AllowedIPs = 192.0.2.1/24`
      - 确保为不中继流量且仅充当简单客户端的远程对等点指定单独的 IP
        - `AllowedIPs = 192.0.2.3/32`
  - 启动中继节点
    - `wg-quick up /full/path/to/wg0.conf`
  - 启动客户端节点
    - `wg-quick up /full/path/to/wg0.conf`

## 配置

```shell
# 安装
apt install wireguard -y

# 添加网络接口
ip link add dev wg0 type wireguard
ip address add dev wg0 10.0.2.1/24

# 生成密钥
wg genkey | tee server-private.key | wg pubkey | tee server-public.key
```

## 命令

**跳板服务器开启中继和转发**

```shell
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
echo "net.ipv4.conf.all.proxy_arp = 1" >> /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf
```

### 生成公钥、私钥

```shell
# generate private key
wg genkey > example.key

# generate public key
wg pubkey < example.key > example.key.pub
```

### 启停

```shell
wg-quick up /full/path/to/wg0.conf
wg-quick down /full/path/to/wg0.conf
# Note: you must specify the absolute path to wg0.conf, relative paths won't work

# start/stop VPN network interface
ip link set wg0 up
ip link set wg0 down

# register/unregister VPN network interface
ip link add dev wg0 type wireguard
ip link delete dev wg0

# register/unregister local VPN address
ip address add dev wg0 192.0.2.3/32
ip address delete dev wg0 192.0.2.3/32

# register/unregister VPN route
ip route add 192.0.2.3/32 dev wg0
ip route delete 192.0.2.3/32 dev wg0
```

## 注意

- 如果一个节点在 NAT 内，在配置远端 Peer 时需要配置 `PersistentKeepalive `，这样远端 Peer 才能访问当前 Node

```yaml
[Peer]
Endpoint = <ip:port>
PublicKey = <public-key>
AllowedIPs = 10.0.10.1/24
PersistentKeepalive = 25
```

## 其他

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

