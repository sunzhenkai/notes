---
title: HTTPS 证书
categories: 
  - [play,server]
tags:
  - server
date: "2022-08-21T00:00:00+08:00"
---

# CertBot

使用 CertBot 进行证书签发及自动更新。

```shell
# 安装 certbot
$ sudo snap install --classic certbot
$ sudo ln -s /snap/bin/certbot /usr/bin/certbot

# 证书签发
# 需要: 关闭监听 80 端口的 web server
$ sudo certbot certonly --standalone
# 依次输入 邮箱、域名等
# 证书会放在 /etc/letsencrypt/live/{domain}/ 下
# CertBot 会创建定时任务刷新证书
```

# Caddy

Caddy Server 可以自动识别证书，无需指定证书位置。

```shell
exploring.fun {
    reverse_proxy http://172.60.2.1:30800
}
```

