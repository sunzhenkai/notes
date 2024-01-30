---
title: BRPC - 自定义
categories: 
  - 研习录
tags:
  - 研习录
  - RPC
date: 2024/1/25 00:00:00
---

# 自定义协议

对于绝大多数线上服务，服务间的 RPC 都是通过 TCP/IP 协议，brpc 同样是基于 TCP/IP 协议封装的 RPC 框架，支持自定义协议，来兼容多种服务端的调用。实现了部分常用的协议，也可以自定义适用于特定场景的协议。

这里是 BRPC 添加协议的[官方文档](https://brpc.incubator.apache.org/zh/docs/rpc-in-depth/new-protocol/)。

