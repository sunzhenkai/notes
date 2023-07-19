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

# 或者 ~/.local/bin/kubectl, 适配 k9s
#!/bin/bash
exec microk8s.kubectl $(echo "$*" | sed 's/-- sh.*/sh/')
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
mk enable dns storage dashboard helm3
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

## 异常

### Failed create pod sandbox

**错误信息**

```shell
Failed create pod sandbox: rpc error: code = Unknown desc = failed to set up sandbox container ... error getting ClusterInformation: Get ... https://10.152.183.1:443 ...
```

**原因**

```shell
NAMESPACE↑                 NAME                      TYPE                     CLUSTER-IP     
default                    kubernetes                ClusterIP                10.152.183.1
```

错误信息提示请求 ClusterIP 异常，检查节点 IP。

```shell
$ k get nodes -o wide
NAME STATUS   ROLES    AGE   VERSION   INTERNAL-IP   ... KERNEL-VERSION      CONTAINER-RUNTIME
a    Ready    <none>   16h   v1.27.2   172.21.0.3    ... 5.4.0-126-generic   containerd://1.6.15
b    Ready    <none>   16h   v1.27.2   192.168.6.201 ... 5.15.0-76-generic   containerd://1.6.15
```

**解决**
在 b 节点无法通过 a 的 INTERNAL-IP 访问 a（controller） 节点，修改两个节点的 `--node-ip` 为可以访问的 ip。

```shell
microk8s stop
# or for workers: sudo snap stop microk8s

sudo vim.tiny /var/snap/microk8s/current/args/kubelet
# Add this to bottom: --node-ip=<this-specific-node-lan-ip>

sudo vim.tiny /var/snap/microk8s/current/args/kube-apiserver
# Add this to bottom: --advertise-address=<this-specific-node-lan-ip>

microk8s start
# or for workers: sudo snap start microk8s
```

### certificate is valid for kubernetes ... not for mydomain.com

参考 [这里](https://microk8s.io/docs/services-and-ports)。

```shell
$ vim /var/snap/microk8s/current/certs/csr.conf.template
# 添加域名
[ alt_names ]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster
DNS.5 = kubernetes.default.svc.cluster.local
DNS.6 = mydomain.com  # 添加一行

# 生效
$ sudo microk8s refresh-certs --cert server.crt
```

