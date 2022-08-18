---
title: k8s 配置
categories: 
	- [架构,container,k8s]
tags:
	- k8s
date: 2022/08/15 00:00:00
update: 2022/08/15 00:00:00
---

# 服务

## 端口

- ClusterIP，集群内可以访问，也可以使用 port-forward （用于测试）的方式访问
- NodePort，直接通过节点访问（k8s 节点，master & work）
  - 需要定义 nodePort
  - 不同的流量会被转发到不同的 pod
- LoadBalancer，负载均衡方式访问（需要负载均衡器）