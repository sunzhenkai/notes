---
title: grpc java
categories: 
    - [架构, rpc, gRPC]
tags:
    - gRPC
date: 2021/06/03 00:00:00
update: 2021/06/03 00:00:00
---

# ManagedChannelImpl

**Channel** 去执行一次远程调用，是通过其 **newCall** 方法，传入 **MethodDescriptor ** 和 **CallOptions**。对于 **ManagedChannelImpl**，其实现 Channel 接口，newCall 方法转而调用 InterceptorChannel 的 newCall，先简单说下 InterceptorChannel。

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

