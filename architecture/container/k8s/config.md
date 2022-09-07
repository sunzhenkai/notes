---
title: k8s 配置
categories: 
	- [架构,container,k8s]
tags:
	- k8s
date: 2022/08/15 00:00:00
update: 2022/08/15 00:00:00
---

# k8s objects

[官方文档](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)。k8s objects 是 k8s 系统中的持久化实体，用来表示服务集群的状态。

## Spec 和 Status

每个 k8s object 包含两个字段，spec 和 status。spec 是事先设置的期望的状态，由使用者指定。status 用来描述当前的状态，由 k8s 系统维护。

## 描述 k8s objects

当在 k8s 系统中创建 object 时，需要指定 object spec，来描述期望的状态，以及基础信息。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  # 部署的名字
  name: nginx-deployment
spec:
	# 用来查找关联的 pod, 所有标签都匹配才行
  selector:
    matchLabels:
      app: nginx
  replicas: 2 # tells deployment to run 2 pods matching the template
  # 定义 pod 相关信息
  template:
    metadata:
      labels:
        app: nginx
    spec:
    	# 定义容器，可以多个
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
        env:
        	- name: ENV_NAME
        		value: ENV_VALUE
```

### 需要的字段

- `apiVersion` - 创建 k8s object 时使用的 API 版本
- `kind` - 创建的 object 的类型
- `metadata` - 用来唯一标识 object，包括 `name`、`UID`、`namespace`
- `spec` -  k8s object 期望的状态

# 服务

## 端口

- ClusterIP，集群内可以访问，也可以使用 port-forward （用于测试）的方式访问
- NodePort，直接通过节点访问（k8s 节点，master & work）
  - 需要定义 nodePort
  - 不同的流量会被转发到不同的 pod
- LoadBalancer，负载均衡方式访问（需要负载均衡器）