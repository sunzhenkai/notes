---
title: java 线程
categories: 
  - [coding,java,notes]
tags:
  - java
date: "2021-03-10T00:00:00+08:00"
update: "2021-03-10T00:00:00+08:00"
---

# Executor

```java
// 创建 executor
private static final ExecutorService executor = Executors.newFixedThreadPool(8);

// 异步提交 
executor.submit(Callable<V> / Runnable);
executor.execute(Runnable);

// 同步等待
executor.invokeAll(Collection<Callable<V>>);
  
// shutdown 
executor.shutdown();
```

**Tips**

- **submit** VS **execute** 
  - 参数不同，submit 可接受 Callable 和 Runable 类型变量，execute 只接受 Runable
  - submit 提交任务后可在主线程同步等待，execute 由于没有返回值，则不行
  - submit 可以通过 `Future.get()` 在主线程捕获异常，execute 则不行 

