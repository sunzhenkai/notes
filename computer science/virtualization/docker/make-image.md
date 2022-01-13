---
title: 制作 docker 镜像
categories: 
    - [计算机科学,虚拟化,docker]
tags:
    - docker
date: 2021/12/27 00:00:00
update: 2021/12/27 00:00:00
---

# 编写 Dockerfile

```dockerfile
FROM	centos:7
LABEL	maintainer="zhenkai.sun@qq.com"
LABEL   version="v0.0.1-centos-7"
RUN     yum -y install gcc g++ automake autoconf make git libtool
```

# 构建镜像

```shell
$ docker build -t sunzhenkai/cmake-external-library .
```

# 发布

```shell
$ docker tag user/prop:latest user/prop:<version/tag>
$ docker login -u <用户名> -p <密码>
$ docker push user/prop:<version/tag>

# 实例
$ docker tag  sunzhenkai/cmake-external-library:latest sunzhenkai/cmake-external-library:centos7-v0.0.1
$ docker docker push sunzhenkai/cmake-external-library:centos7-v0.0.1
```

