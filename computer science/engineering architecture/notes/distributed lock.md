---
title: 架构 - 分布式锁
categories: 
  - [架构, notes]
tags:
  - 分布式锁
date: "2021-05-13T00:00:00+08:00"
update: "2021-05-13T00:00:00+08:00"
---

# 方案

- zookeeper
- redis
  - 加锁、解锁过程
  - 过期时间
  - 结合Bootstrap
- ParallelStream Completablefuture

