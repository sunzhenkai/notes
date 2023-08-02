---
title: gRPC 的一些实践
categories: 
  - [架构, rpc, gRPC]
tags:
  - gRPC
date: 2021/11/15 00:00:00
update: 2021/11/15 00:00:00
---

# gRPC 的一些想法

开源的 RPC 框架有很多，如果专注于 java，可以尝试 [finagle](https://twitter.github.io/finagle/)，打造基于 java 的微服务系统可以考虑  `dubbo`、`spring cloud`、`spring cloud alibaba`；如果是 c++ 可以尝试 thrift/pb + brpc；如果服务有跨语言调用的需求，可以考虑 thrift、gRPC。

相信，谷歌的背书 + 多语言 + pb & gRPC，会吸引很多人的注意，但是 gRPC 的一些坑还是要慢慢趟才行。

比如 ManagedChannel 默认的负载均衡是 pick_first。公司用了几年，虽然有了服务发现，但是创建 stub 时还是随机选择一个机器创建连接。如果服务端是 python，还要注意多个服务进程的负载均衡问题（python 服务一般会起多个进程，共用一个端口），因为 gRPC 的负载均衡是连接粒度的，如果客户端复用连接，那么就会出现请求全部集中在一个进程上面，这样至多使用机器的一个核心；这个问题简单一点可以通过创建多个连接，请求时随机选取来解决，比较好的解决方案是自定义 load balance，定义 subchannel 创建规则。

还有就是，gRPC 的文档并没有想象中那么多，就 java 来说，封装了大量的逻辑，有些甚至连代码注释说的都很模糊。

# ManagedChannel

ManagedChannel 有很多内置的实现，常用的是 `ManagedChannelImpl2`，涉及到几个比较重用的概念。

