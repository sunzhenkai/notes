---
title: Docker 容器
categories: 
    - [计算机科学,虚拟化,docker]
tags:
    - docker
date: 2020/12/21 19:00:00
update: 2020/12/21 19:00:00
---

# MySQL & mariadb

## MySQL

```shell
$ docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:latest --default-authentication-plugin=mysql_native_password
# 认证插件 mysql_native_password, passwd, sha256_password; 如果工具连接出错，可尝试添加
```

## mariadb

**下载镜像**

```shell
$ docker pull mariadb:latest
```

**运行镜像**

```shell
$ docker run -p 3306:3306 --name mariadb -e MYSQL_ROOT_PASSWORD=ipwd -d mariadb:latest
```

### 参考

- https://hub.docker.com/_/mysql/
- https://hub.docker.com/_/mariadb

# Redis

**下载镜像**

```shell
$ docker pull redis:latest
```

**运行容器**

```shell
$ docker run -itd --name redis -p 6379:6379 redis:latest
```

