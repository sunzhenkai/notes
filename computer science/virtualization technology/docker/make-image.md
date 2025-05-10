---
title: 制作 docker 镜像
categories: 
    - [计算机科学,虚拟化,docker]
tags:
    - docker
date: "2021-12-27T00:00:00+08:00"
update: "2021-12-27T00:00:00+08:00"
---

[toc]

# 编写 Dockerfile

## 示例

```dockerfile
FROM	centos:7
LABEL	maintainer="zhenkai.sun@qq.com"
LABEL version="v0.0.1-centos-7"
RUN   yum -y install gcc g++ automake autoconf make git libtool
```

## 命令

```shell
FROM  
LABEL 设置元数据(LABEL author=wii email=zhenkai.sun@qq.com)
ARG   设置参数, Dockerfile 内有效
RUN   构建时运行命令
EXPOSE 声明端口
ENV   设置环境变量, 多值空格分隔(ENV PAHT=/usr/bin GOROOT=/data/go/)
CMD   运行容器时运行, 指定默认运行的程序, 程序结束容器退出, 会被 docker run 命令行参数指定的命令覆盖, 仅最后一个生效
ENTRYPOINT 容器运行时运行，需要显式指定 --entrypoint 才会被覆盖, 只有最后一个生效, CMD 会作为 ENTRYPOINT 的参数
```

## RUN

```dockerfile
# update-alternatives 示例
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 30
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

# 示例
$ docker tag  sunzhenkai/cmake-external-library:latest hub.docker.com/sunzhenkai/cmake-external-library:centos7-v0.0.1
$ docker push hub.docker.com/sunzhenkai/cmake-external-library:centos7-v0.0.1
```

# 参考

- https://www.cnblogs.com/hnusthuyanhua/p/16409801.html
