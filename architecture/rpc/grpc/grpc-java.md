---
title: grpc java
categories: 
    - [架构, rpc, gRPC]
tags:
    - gRPC
date: 2021/06/03 00:00:00
update: 2021/06/03 00:00:00
---

# Channel

gRPC 代码实现中，Channel 是一个虚拟类，是物理连接的逻辑概念。ManagedChannelImpl 和 ManagedChannelImpl2 继承了该类，并实现了 newCall 和 authority 接口。

# SubChannel

SubChannel 是 LoadBalancer 的内部类，在了解 SubChannel 之前，需要先了解 SocketAddress 和 EquivalentAddressGroup。

## SocketAddress

SocketAddress 是一个虚拟类，代表一个不包含协议信息的 Socket 地址。

## EquivalentAddressGroup

EquivalentAddressGroup 是一组 SocketAddress，在 Channel 创建连接时，其包含的 SocketAddress 被视为无差异的。

## SubChannel

再回到 SubChannel，他表示和一个服务器或者 EquivalentAddressGroup 表示的一组等价服务器的 **一个物理连接**，这里需要注意的是，他至多有一个物理连接。在发起新的 RPCs 时，如果没有激活的 transport，在被安排 RPC 请求时，会创建 transport。调用 requestConnection ，会请求 Subchannel 在没有 transport 的情况下创建 transport。

SubChannel 有一个 `List<EquivalentAddressGroup> ` 属性，可以通过 `setAddresses(List<EquivalentAddressGroup> addrs)` 和 `setAddresses(EquivalentAddressGroup addrs)` 设置。

# InternalSubchannel

InternalSubchannel 表示一个 SocketAddress 的 Transports 。他实现了 TransportProvider 接口，定义了 `obtainActiveTransport` 方法，该方法如果没有激活的 transports，则会调用 `startNewTransport` 进行创建。

### 获取 SocketAddress

在创建 transports 时，需要先获取 SocketAddress。在创建 InternalSubChannel 时，会传入 `List<EquivalentAddressGroup>` 。**需要注意的是，InternalSubChannel 默认使用 第一个 EquivalentAddressGroup 的 第一个 SocketAddress ，只有在 transport 被关闭时，才会尝试下一个服务地址。**

尝试完所有的地址，全部失败后，此时 InternalSubChannel 处于 TRANSIENT_FAILURE 状态，等待一个 delay 时间后，重新尝试。

# NameResolver

NameResolver 是一个可插拔的组件（pluggable component），代码层面是一个接口，用来解析一个 target（URI），并返回给调用方一个地址列表，gRPC 内置了 DnsNameResolver。

地址的返回是基于 Listener 机制，NameResolver 的实现类，需要定义 start 方法，方法会传入一个 Listener，当服务列表发生变化时，调用 Listener 的 onResult 方法，通知 NameResolver 的持有方。

# LoadBalancer

LoadBalancer 是一个可插拔的组件，接受 NameResolver 拿到的服务方列表，提供可用的 SubChannel。

## RoundRobinLoadBalancer

从 RoundRobinLoadBalancer 的 handleResolvedAddresses 实现可以发现。

- 每次刷新时

  - 对新增服务方创建 SubChannel
  - 对于删掉的服务方进行剔除
  - 对于可用的服务方，不会重新创建 SubChannel

  

# ManagedChannelImpl

## +Channel

**Channel** 去执行一次远程调用，是通过 **newCall** 方法，传入 **MethodDescriptor ** 和 **CallOptions**。对于 **ManagedChannelImpl**，其实现 Channel 接口，newCall 方法转而调用 InterceptorChannel 的 newCall，先简单说下 InterceptorChannel。

> managedChannelImpl 字段是调用 `ClientInterceptors.intercept(channel, interceptors)` 构造，先说 InterceptorChannel 再说 ClientInterceptors。
>
> **InterceptorChannel** 将 Interceptor 和 Channel 的结合，由 channel + interceptor 构造，调用 channel 的 newCall 时，会执行 interceptor 的 interceptCall，该调用会传入 channel。对于一个原始 channel 和 多个 interceptor，先将 interceptor 倒序，然后依次创建 InterceptorChannel，进行包装。
>
> ```java
> for (ClientInterceptor interceptor : interceptors) {
>   channel = new InterceptorChannel(channel, interceptor);
> }
> ```
>
> 相比之下，**ClientInterceptors** 只是一个工具类。

接着，怎么用上 NameSolver 的。在构造 interceptorChannel 时，传入一个 channel。这个channel 是一个 RealChannel 对象。

> **RealChannel** 实现了 Channel 接口。

## +SubChannel

这里需要再提一下，Channel 是逻辑连接，SubChannel 是物理连接。ManagedChannelImpl 实现了 Channel 接口，同时，有一个内部类 SubchannelImpl 实现 SubChannel。

### 创建物理连接

首先调用 SubchannelImpl 的 `requestConnection` ，在方法内会调用 `InternalSubchannel` 的 `obtainActiveTransport` 创建和 SocketAddress 的连接。

## +NameResolver

在 ManagedChannelImpl 内，定义了 NameResolverListener，实现了NameResolver.Listener 接口，在 NameResolverListener 内做了 LoadBalancer 和 NameResolver 的结合。

### NameResolver + LoadBalancer

在 NameResolverListener 的 onResult 方法内，当服务器地址变更时会执行改方法。首先，会从参数中获取服务端列 表`List<EquivalentAddressGroup>`，接下来调用 AutoConfiguredLoadBalancer 的 `tryHandleResolvedAddresses` 方法，再调用 LoadBalancer 的 `handleResolvedAddresses`。整个调用实现比较绕，直接了解内置的 LB 即可。

