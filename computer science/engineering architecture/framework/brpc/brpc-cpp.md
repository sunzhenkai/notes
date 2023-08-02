---
title: brpc c++
categories: 
  - [架构,框架,brpc]
tags:
  - brpc
date: 2020/12/31 00:00:00
update: 2020/12/31 00:00:00
---

# 描述

brpc c++ 是百度基于c++编写的RPC框架，文档参考[这里](https://github.com/apache/incubator-brpc/blob/master/README_cn.md)。

# 编译

编译文档参考[这里](https://github.com/apache/incubator-brpc/blob/master/docs/cn/getting_started.md)。编译brpc之前，首先需要准备依赖，brpc一下如下库。

- **gflags**：定义全局变量
- **protobuf**：序列化消息及服务接口
- **leveldb**：[rpcz](https://github.com/apache/incubator-brpc/blob/master/docs/cn/rpcz.md) 需要，记录RPC踪迹

