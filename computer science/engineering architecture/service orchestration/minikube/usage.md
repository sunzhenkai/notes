---
title: minikube usage
categories: 
  - [架构,container,minikube]
tags:
  - minikube
date: "2023-07-12T00:00:00+08:00"
---

# 文档

- [minikube start](https://minikube.sigs.k8s.io/docs/start/)

# 安装

- [minikube install](https://minikube.sigs.k8s.io/docs/start/)
- [docker install](https://docs.docker.com/engine/install/)
  - 需要配置当前用户操作权限

- kubectl 安装
  - ubuntu `sudo snap install kubectl --classic`
  - arch `sudo pamac install kubectl`

## archilinux

### driver=virtualbox

```shell
$ sudo pamac install virtualbox
$ sudo modprobe vboxdrv
$ sudo modprobe vboxnetadp
$ sudo modprobe vboxnetflt

# 启动 minikube
$ minikube start --driver=virtualbox
```

# 配置

## 启用私有仓库

```shell
$ minikube addons configure registry-creds

Do you want to enable AWS Elastic Container Registry? [y/n]: n

Do you want to enable Google Container Registry? [y/n]: n

Do you want to enable Docker Registry? [y/n]: y
-- Enter docker registry server url: registry.cn-hangzhou.aliyuncs.com
-- Enter docker registry username: <username>
-- Enter docker registry password:

Do you want to enable Azure Container Registry? [y/n]: n
✅  registry-creds was successfully configured
$ minikube addons enable registry-creds
```

**注册**

```shell
$ kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=$HOME/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson \
    --namespace=default

# 在 deployment.yml 中添加如下内容
spec:
		...
    spec:
      imagePullSecrets:
        - name: regcred
```

# 问题

## driver=docker 时无法通过宿主机 ip 访问 service

- service type 设置为 NodePort
- 无法通过宿主机的 ip 或者 `127.0.0.1` + service node port 访问服务
