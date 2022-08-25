---
title: network
categories: 
	- [play,network]
tags:
	- server
date: 2022/08/21 00:00:00
---

# 设置网关导致端口网关失效

参考[这里](https://unix.stackexchange.com/questions/664757/port-forwarding-does-not-work-using-different-gateway)。

```shell
ip route add 192.168.6.0/24 dev br0 table 16
ip route add default via 192.168.6.1 dev br0 table 16
ip rule iif to ipproto tcp sport 10014 lookup 16
```

另外一种[方式](https://superuser.com/questions/1091848/port-forwarding-not-working-for-certain-lan-ip)。

```shell
ip route add 192.168.6.0/24 dev br0 table 10
ip route add default via 192.168.6.1 table 10
ip route add 192.168.9.0/24 dev br1 table 12
ip route add default via 192.168.9.1 table 12
ip rule add from 192.168.6.0/24 table 10 priority 1
ip rule add from 192.168.9.0/24 table 12 priority 2

# 添加 docker 网络
ip route add 172.17.0.0/16 dev docker0 table 10
ip route add 172.17.0.0/16 dev docker0 table 12

# 刷新配置
ip route flush cache

# 校验
$ ip route show table 12
default via 192.168.9.1 dev br1
172.17.0.0/16 dev docker0 scope link
192.168.9.0/24 dev br1 scope link
```

## 示例

```shell
# out
ip route add default via 192.168.6.1 dev ens8 table 10
ip route add default via 192.168.9.1 dev ens9 table 12
# in
ip rule add from 192.168.6.0/24 table 10 priority 1
ip rule add from 192.168.9.0/24 table 12 priority 2 # 可以不设置 priority

# 如果有设置了默认的路由，可以忽略其中的一个，比如有如下默认路由
ip route add default via 192.168.6.1 dev ens8
# 那么只需要设置 192.168.9.0/24
ip route add default via 192.168.9.1 dev ens9 table 12
ip rule add from 192.168.9.0/24 table 12 
```

# 连接路由器的 VPN 之后无法访问内网服务

**原因**

路由器局域网网段和外网网段冲突，导致访问局域网 ip 不走 vpn 网络。

**设置**

```shell
# macos, route 命令
## 查看路由表
sudo netstat -rn
192.168.6.6        link#6             UHRLWIi           en0      8   
## en0 是 wifi 网络接口, vpn 的网络端口是 utun3
## 修改路由, 把 192.168.6.0/24 所有网段的路由走 vpn
sudo route change 192.168.6.0/24 -interface utun3
```

