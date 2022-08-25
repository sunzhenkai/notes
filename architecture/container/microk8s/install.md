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

# 配置镜像地址
```shell
# create a directory with the registry name
sudo mkdir -p /var/snap/microk8s/current/args/certs.d/k8s.gcr.io

# create the hosts.toml file pointing to the mirror
echo '
server = "https://k8s.gcr.io"

[host."https://registry.cn-hangzhou.aliyuncs.com/google_containers"]
capabilities = ["pull", "resolve"]

' | sudo tee -a /var/snap/microk8s/current/args/certs.d/k8s.gcr.io/hosts.toml
```

# 检查状态
```shell
# 如果不翻墙/替换镜像, 会在这里卡住
microk8s status --wait-ready
```

# 设置别名
```shell
# vim ~/.bash_aliases
alias k='microk8s kubectl'
```