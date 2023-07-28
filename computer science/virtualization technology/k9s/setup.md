---
title: k9s setup
categories: 
	- [架构,container,k8s,k9s]
tags:
	- k9s
date: 2022/08/22 00:00:00
---

# Install

```shell
# brew
brew install derailed/k9s/k9s

# snap
sudo snap install k9s
```

# 连接集群

```shell
# microk8s
# 保存内容至 ~/.kube/config 
# k9s 会读取配置并连接集群
microk8s config > ~/.kube/config 
```

