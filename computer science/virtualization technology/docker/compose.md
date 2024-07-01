---
title: docker compose
categories: 
  - [计算机科学,虚拟化,docker]
tags:
  - docker
date: 2023/08/02 00:00:00
---

# Docker Compose

Docker Compose是一个用于定义和运行多个容器化应用的工具。它允许你通过一个单独的配置文件（通常是YAML格式）来定义和管理多个Docker容器，以便这些容器能够协同工作。

Docker Compose的主要功能包括：

1. 定义服务：使用Compose文件可以指定多个相关联的服务，每个服务都在单独的容器中运行。例如，你可以定义一个Web服务、一个数据库服务和一个消息队列服务。
2. 配置网络和卷：Compose文件允许你定义容器之间的网络连接，以及将本地文件系统的目录与容器内的卷进行映射。
3. 管理环境变量：Compose文件支持设置和管理环境变量，这对于配置应用程序和容器之间的交互非常有用。
4. 批量启动和停止：使用Compose命令可以方便地一次启动或停止整个应用程序，而不需要分别管理每个容器。

# 对比 Dockerfile

相比之下，Dockerfile是用于构建Docker镜像的文本文件。它包含了描述如何构建镜像的指令和配置，例如基础镜像选择、安装软件包、配置环境等。通过执行Dockerfile中的指令，可以自动化地构建出一个可重复部署的镜像。

Dockerfile和Docker Compose的主要区别在于其关注点和使用场景：

- Dockerfile：适用于单个容器或一个独立的服务。它用于定义镜像的构建过程，使其可在任何支持Docker的环境中部署。
- Docker Compose：适用于多个相关容器组成的应用程序。它用于定义、配置和管理多个容器之间的交互，并提供了一种简化的方式来启动、停止和管理整个应用程序的多个服务。

通常情况下，你可以使用Dockerfile构建出应用程序所需的镜像，然后使用Docker Compose来定义和管理各个容器的协同工作，以搭建和运行复杂的多容器应用程序。

# 安装

```shell
$ sudo apt install docker-compose-plugin
```

# 命令

```shell
# 启动
$ docker compose up -d
# 停止
$ docker dompose stop

# 删除
# !!! 注意, 是删除
$ docker compose down
```

## 启动指定 service

```shell
$ docker compose up -d services...
```

# Nvidia GPU

## 安装驱动（ubuntu）

```shell
$ sudo ubuntu-drivers list                # 可安装驱动列表, 多版本
$ sudo ubuntu-drivers install nvidia:535  # 安装指定版本
```

## 安装工具（ubuntu）

安装文档参考这里[Installing the NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)。

```shell
$ curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
$ sudo apt-get update
$ sudo apt-get install -y nvidia-container-toolkit
```

## 配置 Docker

```shell
$ sudo nvidia-ctk runtime configure --runtime=docker
$ sudo systemctl restart docker # 重启 docker
```

## Docker Compose 添加配置

```shell
...
services:
  {service-name}:
    image: ...
    ...
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

