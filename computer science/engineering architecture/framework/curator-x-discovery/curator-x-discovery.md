---
title: curator x discovery
categories: 
  - [架构,java,框架,curator x discovery]
tags:
  - curator x discovery
date: "2021-06-03T00:00:00+08:00"
update: "2021-06-03T00:00:00+08:00"
---

## 概念

- `ServiceDiscovery`  ，创建 `ServiceProvider` 对象，首先需要有 `ServiceDiscovery` ；所有请求直接访问 zk
- `ServiceProvider`， 特定服务发现的封装，并集成了负载均衡策略；集成了 `ServiceCache` ，有节点监听和缓存
- `ServiceCache` ，会在本地内存缓存，并使用 watcher 来保持数据最新

# 说明

`ServiceDiscovery` 、`ServiceProvider` 需要调用 `start` 方法后可用。

## 注册

- 使用 `ServiceDiscovery` 的 `registerService` 注册服务后，只要 `ServiceDiscovery` 不 `stop` ，会一直保持节点注册
- 服务被强制 `stop` ，没有及时调用 `unregisterService` 接口来取消注册，zk 节点会保存一段时间（几秒），然后由 zk 摘除

## 查询

- `ServiceProvider` 的接口，会实时调用 zk 查询数据，

## 监听

`ServiceCacheListener` 有两个方法。

- `cacheChanged` 当服务节点变化时，会调用该方法
- `stateChanged` 当 zk 连接状态变化时，会调用该方法