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

## 集群模式

```shell
$ docker pull redis

docker create --name redis-node1 -p 6379:6379 redis --cluster-enabled yes
docker create --name redis-node2 -p 6378:6378 redis --cluster-enabled yes --port 6378
docker create --name redis-node3 -p 6377:6377 redis --cluster-enabled yes --port 6377
docker start redis-node1 redis-node2 redis-node3

docker exec -it redis-node1 /bin/sh

> redis-cli --cluster create 172.17.0.2:6379 172.17.0.3:6379 172.17.0.4:6379

> redis-cli --cluster create 192.168.4.13:6379 192.168.4.13:6378 192.168.4.13:6377

# 查看容器 ip
$ docker inspect <container-name>

# stop
docker stop redis-node1 redis-node2 redis-node3

# rm
docker rm redis-node1 redis-node2 redis-node3
```

# alpine

```shell
$ docker pull alpine:latest
$ docker run -itd --name alpine-ins alpine:latest
```

