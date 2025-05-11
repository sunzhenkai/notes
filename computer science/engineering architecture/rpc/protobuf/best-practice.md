---
title: protobuf best practice
categories: 
  - [架构, rpc]
tags:
  - protobuf
date: "2023-08-14T00:00:00+08:00"
update: "2023-08-14T00:00:00+08:00"
---

# 枚举定义

## 取值跳过 0

0 是默认值，在 Protobuf 3 中[移除了 optional 和 required 关键词](https://stackoverflow.com/questions/31801257/why-required-and-optional-is-removed-in-protocol-buffers-3)，在序列化时没有标记字段是否设置，这会在某些场景带来一些问题。

- 序列化时跳过为默认值的字段
  - 转换为 Json 时会缺少字段
- 无法区分未设置和设置为默认值
  - 这两种情况在某些场景下表示完全不同的含义，比如我们用一个字段存储特征，那么这个特征值是默认值和特征不存在是两种情况，不能混为一谈
