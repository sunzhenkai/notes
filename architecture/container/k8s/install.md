---
title: k8s 安装
categories: 
	- [架构,container,k8s]
tags:
	- k8s
date: 2021/08/25 00:00:00
update: 2021/08/25 00:00:00
---

# 拉取镜像

```shell
$ kubeadm config images pull --image-repository registry.aliyuncs.com/google_containers
```

# 初始化

```shell
# 10.244.0.0/16 是 chennel 扩展的配置
# 192.168.6.33 是 master 节点的 ip，如果是单机，即为该机器 ip 地址
$ kubeadm init --pod-network-cidr=10.244.0.0/16 \
  --apiserver-advertise-address=192.168.6.33
```

# 网络扩展

## flannel

### 安装

```shell
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

# 常用命令

## 查看节点信息

```shell
$ kubectl get nodes
NAME                    STATUS     ROLES                  AGE     VERSION
localhost.localdomain   NotReady   control-plane,master   2m13s   v1.22.1
```

## 查看 pod 信息

```shell
$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                            READY   STATUS    RESTARTS   AGE
kube-system   coredns-78fcd69978-9dk4n                        0/1     Pending   0          2m52s
kube-system   coredns-78fcd69978-w52zc                        0/1     Pending   0          2m52s
kube-system   etcd-localhost.localdomain                      1/1     Running   0          3m6s
kube-system   kube-apiserver-localhost.localdomain            1/1     Running   0          3m6s
kube-system   kube-controller-manager-localhost.localdomain   1/1     Running   0          3m8s
kube-system   kube-proxy-4w84n                                1/1     Running   0          2m52s
kube-system   kube-scheduler-localhost.localdomain            1/1     Running   0          3m6s
```

# 参考

- http://blog.hungtcs.top/2019/11/27/23-K8S%E5%AE%89%E8%A3%85%E8%BF%87%E7%A8%8B%E7%AC%94%E8%AE%B0/
- https://www.youtube.com/watch?v=ACypx1rwm6g