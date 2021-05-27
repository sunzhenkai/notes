---
title: 操作系统 - 进程、线程以及协程
categories: 
	- [计算机科学,操作系统]
tags:
	- 操作系统
date: 2021/03/11 00:00:00
update: 2021/03/11 00:00:00
---

# 简述

**进程**（Process）是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位，是[操作系统](https://link.zhihu.com/?target=https%3A//baike.baidu.com/item/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F)结构的基础。

**线程**（Thread）是[操作系统](https://link.zhihu.com/?target=https%3A//baike.baidu.com/item/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F)能够进行运算[调度](https://link.zhihu.com/?target=https%3A//baike.baidu.com/item/%E8%B0%83%E5%BA%A6)的最小单位。它被包含在[进程](https://link.zhihu.com/?target=https%3A//baike.baidu.com/item/%E8%BF%9B%E7%A8%8B)之中，是[进程](https://link.zhihu.com/?target=https%3A//baike.baidu.com/item/%E8%BF%9B%E7%A8%8B)中的实际运作单位。一条线程指的是[进程](https://link.zhihu.com/?target=https%3A//baike.baidu.com/item/%E8%BF%9B%E7%A8%8B)中一个单一顺序的控制流，一个进程中可以并发多个线程，每条线程并行执行不同的任务。

**协程** （coroutine）是可暂停和恢复执行的过程，是一种编程思想。

# 协程

子程序，或者称为函数，在所有语言中都是层级调用。子程序调用是通过栈实现的，一个线程同一时间就是执行一个子程序。**协程本质上也是子程序，协程作为子程序最大的特征是可中断可恢复**。

# 关联

## Java 中的线程

**green threads VS native threads**

> **green threads** 是一种由运行环境或虚拟机(VM)调度，而不是由本地底层操作系统调度的线程。绿色线程并不依赖底层的系统功能，模拟实现了多线程的运行，这种线程的管理调配发生在用户空间而不是内核空间，所以它们可以在没有原生线程支持的环境中工作。
> 在Java 1.1中，绿色线程（至少在 Solaris 上）是JVM 中使用的唯一一种线程模型。 由于绿色线程和原生线程比起来在使用时有一些限制，随后的 Java 版本中放弃了绿色线程，转而使用**native threads**。[[2\]](https://zhuanlan.zhihu.com/p/133275094#ref_2)

在 Java1.2 之后. Linux中的JVM是基于`pthread`实现的，即 **现在的Java中线程的本质，其实就是操作系统中的线程**。

# 参考

- https://zhuanlan.zhihu.com/p/133275094
- https://zhuanlan.zhihu.com/p/172471249
- https://www.zhihu.com/question/50185085
- https://www.zhihu.com/question/342261454/answer/800062080