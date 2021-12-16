---
title: seastar tutorail
categories: 
	- [架构,java,框架,seastar]
tags:
	- seastar
date: 2021/12/15 00:00:00
update: 2021/12/15 00:00:00
---

seastar 入门， 基于这里 [这里](http://docs.seastar.io/master/tutorial.html#disk-io-scheduler).

# 描述

seastar 使用两个概念 futures 和 continuations，提供复杂的异步编程库，使用非共享编程模型。

# 异步编程

大多数程序处理并行的请求，通常是每个连接使用隔离的操作系统级别的进程。这种技术也一直在进化，从一开始的每个请求都会创建一个进程，到创建一个线程池，最终进化到使用线程。不过，进化的共同点是在一个时刻，每个进程/线程处理一个连接。

异步/时间驱动的服务，通常一个核心对应一个线程。

seastar 是一个事件驱动的框架，允许你使用相对直接的方式编写非阻塞、异步代码。他的 API 基于 future，利用下面的概念达到极致性能。

- 协同微任务调度器
- 非共享 SMP 架构
- 基于 future 的 APIs
- 非共享 TCP 堆栈
- 基于 DMA 的存储 APIs

# 开始

每个 seastar 应用必须定义和运行一个 app_template 对象，该对象启动主事件循环（seastar 引擎）在一个或多个 cpu 核心上，运行指定的函数。

方法返回一个 future，指示何时退出程序，如果是返回 `make_ready_future<>` 则会立刻退出程序。无论何时，C 的 `exit()` 方法都不应使用，这会阻止 seastar 或程序进行适当的清理工作。

# 线程和内存

## 线程

seastar 应用在每个核心上运行一个线程，每个线程运行自己的 event loop，可以使用 `seastar::smp::count` 打印运行的线程数。

## 内存

