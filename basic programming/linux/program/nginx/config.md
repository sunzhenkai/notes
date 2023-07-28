---
title: nginx配置
categories: 
	- [linux,software]
tags:
	- linux
	- nginx
date: 2020/11/13 22:00:00
update: 2020/11/13 22:00:00
---

# 命令

```shell
# 检查配置文件
$ sudo nginx -t

# 重新加载配置
$ sudo nginx -s reload
```

# 配置

## Centos

centos 下 nginx 配置默认是在 `/etc/nginx/nginx.conf` 及 `/etc/nginx/conf.d/`。

# 开启目录访问

```nginx
# 在配置文件的 server 配置的 location 配置中添加 autoindex on
location / {
    autoindex on;
    autoindex_exact_size off;
    autoindex_format html;
    autoindex_localtime on;
}
```


# 配置服务

## upstream

```
upstream [us-name] {
    server 127.0.0.1:[port];
}

server {
    listen       80;
    server_name  example.com;
    # auth_basic "Auth Message";
    # auth_basic_user_file /etc/apache2/.htpasswd;
    client_max_body_size 100m;

    # rewrite ^/(.*) https://example.com/$1 permanent;

    location / {
        proxy_pass         http://[us-name];
        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        
        # enable websocket
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

# 认证

## Basic

```shell
# 1. 安装 apache2-utils (Debian, Ubuntu) / httpd-tools (RHEL/CentOS/Oracle Linux)
# 2. 创建认证文件
$ sudo mkdir /etc/apache2
## 创建
$ sudo htpasswd -c /etc/apache2/.htpasswd user
## 添加，移除 -c 参数
$ sudo htpasswd /etc/apache2/.htpasswd another-user

# 3. 配置
## 按路径配置
server {
	...
  location /api {
      auth_basic           "Administrator’s Area";
      auth_basic_user_file /etc/apache2/.htpasswd; 
  }
}
## 全局配置
server {
	...
	auth_basic           "Administrator’s Area";
  auth_basic_user_file /etc/apache2/.htpasswd; 
  
  location /api {
  	...
  }
}
```

# 异常

## 修改 root 后 403

**可能原因**

- 没有目录访问权限
- 目录没有指定的默认文件（比如，index.html），同时又未开启 autoindex

**修改 root**

```nginx
# /etc/nginx/nginx.conf
http {
  ...
  server {
    ...
    root /home/wii/www;
  }
}
```

**查看权限**

```shell
$ namei -om /home/wii/www
f: /home/wii/www
 dr-xr-xr-x root root /
 drwxr-xr-x root root home
 drwx------ wii  wii  wii
 drwxrwxr-x wii  wii  www
```

**查看 nginx 启动时使用的用户**

```shell
$ ps aux | grep nginx
wii       9364  0.0  0.0 112692  2012 pts/1    R+   15:54   0:00 grep --color=auto nginx
root     11219  0.0  0.0  39308   956 ?        Ss   14:58   0:00 nginx: master process /usr/sbin/nginx
nginx    11220  0.0  0.0  41796  4364 ?        S    14:58   0:00 nginx: worker process
nginx    11221  0.0  0.0  41796  3824 ?        S    14:58   0:00 nginx: worker process
nginx    11222  0.0  0.0  41796  4168 ?        S    14:58   0:00 nginx: worker process
nginx    11223  0.0  0.0  41796  4092 ?        S    14:58   0:00 nginx: worker process
```

可以看到，nginx 使用 nginx 启动，且没有 `/home/wii` 的访问权限，可以通过 `chomd` 设置 `/home/wii` 的权限，或更换其他路径。

**root 更换为 /www**

```shell
$ sudo mkdir /www
$ sudo chmod -R 755 /www
```

# 基于 consul 动态发现

## 重新编译 nginx

使用 [ginx-upsync-module](https://github.com/weibocom/nginx-upsync-module) 模块，下载 nginx 源码，然后把模块代码放在 modules 下，用下面命令编译 nginx。

```shell
#!/bin/sh
./configure --prefix="`pwd`/build" \
	--with-pcre \
	--with-stream \
	--with-http_v2_module \
	--with-http_realip_module \
	--with-http_gzip_static_module \
	--with-http_addition_module \
	--with-http_ssl_module \
	--with-http_sub_module \
	--add-module="`pwd`/modules/nginx-upsync-module" \
	--http-log-path=/logs/nginx/access.log \
  --error-log-path=/logs/nginx/error.log
```

## 配置

```shell
upstream main {
    server 127.0.0.1:8000;
    upsync 127.0.0.1:8500/v1/health/service/echo-service upsync_timeout=6m upsync_interval=500ms upsync_type=consul_health strong_dependency=off;
    upsync_dump_path /home/ubuntu/app/nginx/upsync_backend/echo-service.conf;
    include /home/ubuntu/app/nginx/upsync_backend/echo-service.conf;
}

server {
    listen 8080;

    location /api/v1/echo {
        proxy_pass http://main;
        mirror_request_body on;
        mirror /mirror;
    }
}
```

# 流量复制

mirror 有个坑，nginx 以 subrequest 的方式请求 mirror 地址，只有在所有 subrequest 完成之后才会处理下一个请求。如果用来复制流量给开发环境，那么开发环境的响应时间会作用在线上环境的请求上面。

[参考这里](https://stackoverflow.com/questions/51644141/how-to-make-nginx-mirror-module-not-wait-for-response) 和 [这里](https://forum.nginx.org/read.php?2,281042,281042)。

```shell
upstream main {
    server 192.168.0.10:8000;
}

upstream mirror {
    server 192.168.0.11:8000;
}

server {
    listen 8080;

    location /api/v1/echo {
        proxy_pass http://main;
        proxy_pass_request_body on;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        mirror_request_body on;
        mirror /mirror;
    }

    location /mirror {
        proxy_pass http://mirror$request_uri;
        proxy_pass_request_body on;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

# 附录

## 默认配置

```
##
# You should look at the following URL's in order to grasp a solid understanding
# of Nginx configuration files in order to fully unleash the power of Nginx.
# https://www.nginx.com/resources/wiki/start/
# https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/
# https://wiki.debian.org/Nginx/DirectoryStructure
#
# In most cases, administrators will remove this file from sites-enabled/ and
# leave it as reference inside of sites-available where it will continue to be
# updated by the nginx packaging team.
#
# This file will automatically load configuration files provided by other
# applications, such as Drupal or Wordpress. These applications will be made
# available underneath a path with that package name, such as /drupal8.
#
# Please see /usr/share/doc/nginx-doc/examples/ for more detailed examples.
##

# Default server configuration
#
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	# SSL configuration
	#
	# listen 443 ssl default_server;
	# listen [::]:443 ssl default_server;
	#
	# Note: You should disable gzip for SSL traffic.
	# See: https://bugs.debian.org/773332
	#
	# Read up on ssl_ciphers to ensure a secure configuration.
	# See: https://bugs.debian.org/765782
	#
	# Self signed certs generated by the ssl-cert package
	# Don't use them in a production server!
	#
	# include snippets/snakeoil.conf;

	root /var/www/html;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
	}

	# pass PHP scripts to FastCGI server
	#
	#location ~ \.php$ {
	#	include snippets/fastcgi-php.conf;
	#
	#	# With php-fpm (or other unix sockets):
	#	fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
	#	# With php-cgi (or other tcp sockets):
	#	fastcgi_pass 127.0.0.1:9000;
	#}

	# deny access to .htaccess files, if Apache's document root
	# concurs with nginx's one
	#
	#location ~ /\.ht {
	#	deny all;
	#}
}


# Virtual Host configuration for example.com
#
# You can move that to a different file under sites-available/ and symlink that
# to sites-enabled/ to enable it.
#
#server {
#	listen 80;
#	listen [::]:80;
#
#	server_name example.com;
#
#	root /var/www/example.com;
#	index index.html;
#
#	location / {
#		try_files $uri $uri/ =404;
#	}
#}
```
