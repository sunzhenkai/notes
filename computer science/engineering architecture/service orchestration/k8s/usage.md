---
title: k8s usage
categories: 
  - [架构,container,k8s]
tags:
  - k8s
date: 2022/06/09 00:00:00
update: 2022/06/09 00:00:00
---

[toc]

# 节点管理

## 删除节点

```shell
$ sudo kubeadm reset cleanup-node  # master 节点也可以清除
```

## 标签

```shell
# 查看 node 标签
$ kubectl get nodes --show-labels

# 打标签
$ kubectl label nodes <your-node-name> disktype=ssd
```

 设置 pod 的 node 标签选择（nodeSelector）

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disktype: ssd
```

设置 deployment node 标签选择

```yaml
spec:
	template:
    # 按标签选择机器
    nodeSelector:
      <label-name>: <label-value>
    # 设置机器亲和性
    affinity:
      # 设置 node 亲和性
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
            - matchExpressions:
                - key: <label-name>
                  operator: In
                  values:
                    - <label-value>
      # 设置 pod 亲和性
      podAntiAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
                - key: app.kubernetes.io/name
                  operator: In
                  values:
                    - <pod-name>
                    - <pod-name>
            topologyKey: kubernetes.io/hostname
```



# Deployment 管理

```shell
kubectl delete --all deployments d-n=<ns>
```

# Pod 管理

```shell
# 查看 pod  信息
$ kubectl get pods -A  # A = all-namespaces

# 删除 pod
$ kubectl delete pod <name> --namespace=<ns>
# 批量删除
kubectl delete pod --all -n=<ns>

# 查看 pod 详情; ip 等
$ kubectl describe pod <name> --namespace=<ns>
```

## Service

```shell
# 列出所有 service
k get services -o wide -A --sort-by=.metadata.name 

# 获取 service 详情; nodeport 等
k describe service kubernetes-dashboard -n kube-system
```

# Token

```shell
microk8s kubectl create token -n kube-system default --duration=8544h
```

# 私有仓库

```shell
# docker login
docker login hub.company.com

# 不指定 namespace, 设置 default
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=~/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson

# 每个 namespace 需要单独设置
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=~/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson \
    --namespace=ace

# 修改 deployment
apiVersion: v1
kind: Pod
metadata:
  name: private-reg
spec:
  containers:
  - name: private-reg-container
    image: <your-private-image>
  # 添加 imagePullSecrets
  imagePullSecrets:
  - name: regcred
```

# Secret

```shell
# 创建
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=$HOME/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson \
    --namespace=default

# 查看
kubectl get secrets
kubectl get secretss <secret> --output=yaml

# 删除
kubectl delete secret <secret>
```

# Namespace

```shell
# 创建命名空间
kubectl create namespace <space-name>
```

# 登录容器

```shell
kubectl exec --stdin --tty <pod-instance> -- /bin/bash
```

