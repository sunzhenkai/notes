---
title: microk8s 安装
categories: 
	- [架构,container,microk8s]
tags:
	- microk8s
date: 2022/08/18 00:00:00
update: 2022/08/18 00:00:00
---

# 文档
- [microk8s](https://microk8s.io/docs)

# 安装
```shell
sudo snap install microk8s --classic 
```

# 加入用户组
```shell
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
# 重新进入 session
su - $USER
```

# 配置 k8s.gcr.io 镜像地址
```shell
# create a directory with the registry name
sudo mkdir -p /var/snap/microk8s/current/args/certs.d/k8s.gcr.io

# create the hosts.toml file pointing to the mirror
echo '
server = "https://k8s.gcr.io"

[host."https://registry.aliyuncs.com/v2/google_containers"]
  capabilities = ["pull", "resolve"]
  override_path = true
' | sudo tee -a /var/snap/microk8s/current/args/certs.d/k8s.gcr.io/hosts.toml


# 2
sudo mkdir -p /var/snap/microk8s/current/args/certs.d/registry.k8s.io
echo '
server = "registry.k8s.io"

[host."https://registry.aliyuncs.com/v2/google_containers"]
  capabilities = ["pull", "resolve"]
  override_path = true
' | sudo tee -a /var/snap/microk8s/current/args/certs.d/registry.k8s.io/hosts.toml
```

需要重启

```shell
sudo snap restart microk8s
```

# 检查状态

```shell
# 如果不翻墙/替换镜像, 会在这里卡住
microk8s status --wait-ready
```

# 配置

## 配置 kubectl 命令

```shell
mkdir -p ~/.local/bin/
vim ~/.local/bin/kubectl
# 输入如下内容
#!/bin/bash
exec /snap/bin/microk8s.kubectl $(echo "$*" | sed 's/-- sh.*/sh/')
```

## 配置别名

```shell
# vim ~/.bash_aliases
alias kubectl='microk8s kubectl'
alias k='microk8s kubectl'
alias mk='microk8s'
alias helm='microk8s helm3'
```

# 设置私有镜像仓库

```shell
$ docker login ... # 登录私有镜像仓库
$ kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=$HOME/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson \
    --namespace=default
```

# 组建集群

# 安装 dashboard

```shell
microk8s enable dns dashboard
# 生成 token
microk8s kubectl create token -n kube-system default --duration=8544h
```

# k8s.gcr.io 无法拉取镜像

配置 k8s.gcr.io 理论上可以解决问题。

```shell
# pause
## 从阿里云镜像拉取
docker pull registry.aliyuncs.com/google_containers/pause:3.7
## 重命名
docker tag registry.aliyuncs.com/google_containers/pause:3.7 k8s.gcr.io/pause:3.7
docker tag registry.aliyuncs.com/google_containers/pause:3.7 registry.k8s.io/pause:3.7

# metric server
docker pull registry.aliyuncs.com/google_containers/metrics-server:v0.5.2
docker tag registry.aliyuncs.com/google_containers/metrics-server:v0.5.2 k8s.gcr.io/metrics-server/metrics-server:v0.5.2
docker tag registry.aliyuncs.com/google_containers/metrics-server:v0.5.2 registry.k8s.io/metrics-server/metrics-server:v0.5.2
```

## Join 集群

```shell
# master 节点运行
$ microk8s add-node
From the node you wish to join to this cluster, run the following:
microk8s join 192.168.1.230:25000/92b2db237428470dc4fcfc4ebbd9dc81/2c0cb3284b05

Use the '--worker' flag to join a node as a worker not running the control plane, eg:
microk8s join 192.168.1.230:25000/92b2db237428470dc4fcfc4ebbd9dc81/2c0cb3284b05 --worker

If the node you are adding is not reachable through the default interface you can use one of the following:
microk8s join 192.168.1.230:25000/92b2db237428470dc4fcfc4ebbd9dc81/2c0cb3284b05
microk8s join 10.23.209.1:25000/92b2db237428470dc4fcfc4ebbd9dc81/2c0cb3284b05
microk8s join 172.17.0.1:25000/92b2db237428470dc4fcfc4ebbd9dc81/2c0cb3284b05

# slave 节点运行
$ microk8s join 172.17.0.1:25000/92b2db237428470dc4fcfc4ebbd9dc81/2c0cb3284b05
```

