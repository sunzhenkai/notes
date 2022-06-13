---
title: nginx creat self-signed SSL certificate 
categories: 
	- [linux,software]
tags:
	- linux
	- nginx
date: 2022/06/11 00:00:00
update: 2022/06/11 00:00:00
---

# 创建证书

```shell
# 自认证证书
# 生成 nginx-selfsigned.pass.key
$ openssl genrsa -des3 -passout pass:over4chars -out nginx-selfsigned.pass.key 2048
# 生成 nginx-selfsigned.key
$ openssl rsa -passin pass:over4chars -in nginx-selfsigned.pass.key -out nginx-selfsigned.key
$ rm nginx-selfsigned.pass.key # 可以删除了
# 生成 nginx-selfsigned.csr
$ openssl req -new -key nginx-selfsigned.key -out nginx-selfsigned.csr # 一直回车
# 生成 nginx-selfsigned.crt
$ openssl x509 -req -sha256 -days 365 -in nginx-selfsigned.csr -signkey nginx-selfsigned.key -out nginx-selfsigned.crt

# 需要的文件
- nginx-selfsigned.key
- nginx-selfsigned.crt
```

或者

```shell
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
```

# 设置 nginx 使用 ssl

把生成的整数文件放到 `/certs` 目录下。

```shell
$ sudo mkdir /certs
$ sudo mv nginx-selfsigned.key /certs
$ sudo mv nginx-selfsigned.crt /certs
```

生成 `dhparam.pem` 文件。

```shell
$ openssl dhparam -out /certs/dhparam.pem 4096
```

创建 `/etc/nginx/snippets/self-signed.conf` ，输入如下内容。

```shell
ssl_certificate /certs/nginx-selfsigned.crt;
ssl_certificate_key /certs/nginx-selfsigned.key;

ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
ssl_ecdh_curve secp384r1;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
add_header Strict-Transport-Security "max-age=63072000; includeSubdomains";
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;

ssl_dhparam /certs/dhparam.pem;
```

设置 nginx site 配置。

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;

    server_name server_domain_or_IP;
    include snippets/self-signed.conf;
    ...
}
```

# 配置 http 跳转 https 

按需配置。

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name server_domain_or_IP;
    return 302 https://$server_name$request_uri;
}
```

# 参考

- https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-16-04