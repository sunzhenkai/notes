---
title: microk8s usage
categories: 
	- [架构,container,microk8s]
tags:
	- microk8s
date: 2022/08/21 00:00:00
update: 2022/08/21 00:00:00
---

# 描述

参考 [官方文档](https://microk8s.io/docs)，搭建一个三节点 k8s 集群。

| 节点    | ip         |
| ------- | ---------- |
| k8s01-1 | 10.1.0.78  |
| k8s01-2 | 10.1.0.62  |
| k8s01-3 | 10.1.0.242 |

# alias

```shell
# ~/.bash_aliases
alias k='microk8s kubectl'
alias mk='microk8s'
```

**加入用户组**

```shell
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
# 重新进入 session
su - $USER
```

# Hosts

所有节点

```shell
10.1.0.78 k8s01-1
10.1.0.62 k8s01-2
10.1.0.242 k8s01-3
```

# 初始化集群

```shell
# k8s01-1 主节点
$ mk add-node
From the node you wish to join to this cluster, run the following:
microk8s join 192.168.9.103:25000/5b502d061dd31ec58d1f6ddf96e10c56/be841c6899a7

Use the '--worker' flag to join a node as a worker not running the control plane, eg:
microk8s join 10.1.0.78:25000/5b502d061dd31ec58d1f6ddf96e10c56/be841c6899a7 --worker

If the node you are adding is not reachable through the default interface you can use one of the following:
microk8s join 10.1.0.78:25000/5b502d061dd31ec58d1f6ddf96e10c56/be841c6899a7

# k8s01-2 worker 节点
microk8s join 10.1.0.78:25000/5b502d061dd31ec58d1f6ddf96e10c56/be841c6899a7 --worker

# 对 k8s01-3, 重复上述操作
```

**查看状态**

```shell
$ k get nodes
NAME      STATUS   ROLES    AGE     VERSION
k8s01-1   Ready    <none>   2d12h   v1.24.3-2+63243a96d1c393
k8s01-2   Ready    <none>   77s     v1.24.3-2+63243a96d1c393
k8s01-3   Ready    <none>   64s     v1.24.3-2+63243a96d1c393
```

**更详细的状态**

```shell
$ k get node -o wide
NAME      STATUS   ROLES    AGE     VERSION                    INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
k8s01-1   Ready    <none>   2d12h   v1.24.3-2+63243a96d1c393   10.1.0.78     <none>        Ubuntu 20.04.4 LTS   5.4.0-124-generic   containerd://1.5.13
k8s01-2   Ready    <none>   5m23s   v1.24.3-2+63243a96d1c393   10.1.0.62     <none>        Ubuntu 20.04.4 LTS   5.4.0-124-generic   containerd://1.5.13
k8s01-3   Ready    <none>   5m10s   v1.24.3-2+63243a96d1c393   10.1.0.242    <none>        Ubuntu 20.04.4 LTS   5.4.0-124-generic   containerd://1.5.13
```

# 安装插件

```shell
# 主节点
mk enable dns storage dashboard
```

# 获取 k8s 配置

```shell
mkdir ~/.kube
mk config > ~/.kube/config
```

# 问题排查

## 查看事件

```shell
k get events --sort-by=.metadata.creationTimestamp --namespace=kube-system
```

