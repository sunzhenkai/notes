---
title: k8s problems
categories: 
  - [架构,container,k8s]
tags:
  - k8s
date: 2022/08/27 00:00:00
---

# Pod 无法解析域名

Pod DNS 策略模式是 ClusterFirst，系统 `/etc/resolve.conf` 内容如下。

```shell
nameserver 127.0.0.53
options edns0 trust-ad
search .
```

导致 Pod 里面的 `/etc/resolv.conf` 配置也是如此，无法正常解析域名。先删除 `/etc/resolv.conf`（`/run/systemd/resolve/stub-resolv.conf` 的软链） ，再创建并写入如下内容。

```shell
nameserver 223.5.5.5
nameserver 8.8.8.8
```

```shell
sudo rm /etc/resolv.conf
sudo vim /etc/resolv.conf
```

重启 Pods。

```shell
kubectl delete pods --all -n=<namespace> # 删除所有 pods
```

