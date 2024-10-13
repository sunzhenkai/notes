---
title: docker 使用
categories: 
  - 算机科学
  - 虚拟化
  - docker
tags:
  - docker
date: 2020/12/21 19:00:00
update: 2020/12/21 19:00:00
---

# Docker

Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 [Linux](http://baike.baidu.com/item/Linux) 机器上，也可以实现[虚拟化](http://baike.baidu.com/item/%E8%99%9A%E6%8B%9F%E5%8C%96)。容器是完全使用[沙箱](http://baike.baidu.com/item/%E6%B2%99%E7%AE%B1/393318)机制，相互之间不会有任何接口。

# 安装
## ubuntu
参考[官网文档](https://docs.docker.com/engine/install/ubuntu/)。

## amazon linux 2

```shell
sudo amazon-linux-extras install epel -y
sudo amazon-linux-extras enable docker
sudo yum install -y docker
```

# 配置

## 修改 data 目录

```shell
# vim /etc/docker/daemon.json
{
   "data-root": "/data/docker"
}
```

# 容器

## 从镜像创建新容器

```shell
$ docker run -it -d --restart=always --name=ubuntu-18.04 ubuntu:18.04 

# 指定端口
$ docker run --restart=always -p 8080:8080 <image-name>
```

## 启动已创建容器

```shell
$ docker start container_id/container_name
```

## 查看运行的容器

使用`docker ps`命令可以查看所有正在运行中的容器列表，使用`docker inspect`命令我们可以查看更详细的关于某一个容器的信息。

```shell
docker ps
```

## 停止运行容器

```shell
docker stop container-name
```

**示例**

为了显示更直观, 删除部分内容并使用省略号代替.

```shell
root@VirtualBox:/home/conpot# docker ps
CONTAINER ID        IMAGE        ...
5a794455532d        nginx:alpine    ...  
8518250908b5        voxxit/rsyslog  ...
77613e26eb6f        elk_logstash    ...
7effd23c7005        elk_kibana      ...
root@VirtualBox:/home/conpot# docker stop 5a794455532d
5a794455532d
root@VirtualBox:/home/conpot# docker ps
CONTAINER ID        IMAGE      ...
8518250908b5        voxxit/rsyslog   ...
77613e26eb6f        elk_logstash     ...
7effd23c7005        elk_kibana       ...
root@VirtualBox:/home/conpot# docker stop 8518
8518
root@VirtualBox:/home/conpot# docker ps
CONTAINER ID        IMAGE             ...
77613e26eb6f        elk_logstash      ...
7effd23c7005        elk_kibana        ...
```

**停止所有运行的容器**

```shell
root@VirtualBox:/home/conpot# docker ps -q
77613e26eb6f
7effd23c7005
root@VirtualBox:/home/conpot# docker stop $(docker ps -q)
77613e26eb6f
7effd23c7005
root@VirtualBox:/home/conpot# docker ps -q
```

## 重命名容器

```shell
$ docker rename CONTAINER NEW_NAME
```
## 更新容器设置

```shell
$ docker update --restart=always container_name/container_id	# --restart=no
```

## 执行命令

```shell
$ docker exec -it [container] /bin/bash
```

## 列出所有容器

```shell
$ docker ps -a
```

## 删除容器

```shell
$ docker docker rm container-name
```

## 迁移容器

```shell
# 为 container 创建镜像
$ sudo docker commit <container-name> <image-name>
# 导出镜像
$ sudo docker save <image-name> > image-name.tar
# 或 sudo docker save <image-name> -o image-name.tar

#####

# 导入镜像
$ sudo docker load < image-name.tar
# 创建 container
$ sudo docker run -d --name <container-name> ... <image-name>
```

- [参考](https://www.linuxandubuntu.com/home/migrate-docker-containers-to-new-server)

# 镜像

## 导出镜像

```shell
$ docker save busybox > busybox.tar
$ docker save -o fedora-all.tar fedora
$ docker save -o fedora-latest.tar fedora:latest
# 压缩
$ docker save myimage:latest | gzip > myimage_latest.tar.gz
```

## 加载镜像

```shell
$ docker load -i docker-output.tar
$ docker load < docker-output.tar
```

## Search

```shell
$ docker search ubuntu
```

## 下载

```shell
$ docker pull
```

## 查看下载的容器

```shell
$ docker images
$ docker images ubuntu	# 查看单个镜像
```

## 分析镜像大小

参考工具 [dive](https://github.com/wagoodman/dive)。

```shell
dive hub.docker.com/<user>/<image>:<tag>
```

## 删除镜像 / 清理

```shell
$ docker image remove <id>
$ docker image prune    # 删除无用镜像
$ docker image prune -a # 删除所有镜像
```

## 导出/加载容器

```shell
docker export container-name > latest.tar
docker export --output="latest.tar" container-name
```


# 非 root 用户使用 docker
## ubuntu
https://www.jianshu.com/p/35cdb71a32d3

```shell
$ sudo groupadd docker
$ sudo usermod -aG docker $(whoami)

# 生效
$ sudo service docker restart
$ newgrp - docker # 切换到docker用户组
```

## macos

bash rc 添加如下内容。

```shell
unset DOCKER_TLS_VERIFY
unset DOCKER_CERT_PATH
unset DOCKER_MACHINE_NAME
unset DOCKER_HOST
```

# 拷贝文件

## 从容器拷贝至宿主机

```shell
docker cp <container-name>:/path/to/file /path/to/dest
```

## 从宿主机拷贝至容器

```shell
docker cp /path/to/file <container-name>:/path/to/dest
```

# docker hub

```shell
# 登录 docker hub
docker login

# 登录私有仓库
docker login hub.private.com
```

# 配置代理

```shell
sudo mkdir -p /etc/systemd/system/docker.service.d 
sudo touch /etc/systemd/system/docker.service.d/proxy.conf
sudo chmod 777 /etc/systemd/system/docker.service.d/proxy.conf
sudo echo '
[Service]
Environment="HTTP_PROXY=socks5://192.168.6.19:3213" 
Environment="HTTPS_PROXY=socks5://192.168.6.19:3213"
' >> /etc/systemd/system/docker.service.d/proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl restart kubelet
```

# 参考

- [[1] Docker容器的创建、启动、和停止](http://www.cnblogs.com/linjiqin/p/8608975.html)

# 配置网络

## centos

```shell
```

# 修改 `/var/lib/docker` 路径

```shell
sudo vim /lib/systemd/system/docker.service

```

**参考**

- [1](https://www.digitalocean.com/community/questions/how-to-move-the-default-var-lib-docker-to-another-directory-for-docker-on-linux)

# 异常

## `failed to start daemon: Devices cgroup isn't mounted`

```shell
yum install libcgroup libcgroup-tools libcgroup-pam
systemctl enable cgconfig
systemctl start cgconfig

# 重启
reboot
```

# 常用操作

## 查看磁盘占用

```shell
docker system df -v
# 会打印 image、container 的磁盘占用

# 查看容器磁盘占用
docker ps --size
```

## 清理无用镜像

```shell
docker image prune # 仅清理镜像

# !危险操作
docker system prune # 要同时清理未使用的镜像、停止的容器、未使用的网络和未挂载的卷
```

