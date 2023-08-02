---
title: redis
categories: 
  - [架构, 存储, redis]
tags:
  - 架构
  - 存储
date: 2021/03/12 00:00:00
update: 2020/03/12 00:00:00
---

[toc]

# 简述

## 架构

redis的部署模式分为集群模式和哨兵模式，哨兵模式下的角色有主 + 从 + sentinel。无论哪种模式，主从模式都是存在的，起到读写分离、数据备份的作用。

### 哨兵模式

哨兵是一个独立与数据节点的进程，具备集群监控、消息通知、故障自动转移、配置中心的功能，用于解决高可用的问题。

这里了解两个概念，主观下线和客观下线。单个哨兵判断一个主节点下线，为主观下线；该哨兵向其他哨兵确认主节点是否下线，当一半以上哨兵确定主节点下线，则判定该主节点为客观下线。主节点被判定为客观下线后，哨兵会启动Raft选主程序，最终被投为领导者的哨兵节点完成主从自动切换的过程。

### 集群模式

官方提供的分布式方案，包含槽指派、重新分片、故障转移。

### 哨兵模式和集群模式的区别

- 监控：哨兵模式下，监控权交给了哨兵系统；集群模式下，工作节点自己监控
- 故障转移：哨兵模式下，哨兵发起选举，得到一个leader来处理故障转移；集群模式下，是在从节点中选举一个新的主节点，来处理故障的转移

# 数据安全

## 数据丢失

- 主从复制
  - 由于复制是异步的，如果在未复制前主节点宕机，数据丢失
- 脑裂
  - 网络分区间不可访问导致某个master节点和集群失联，但是客户端依然在写入数据，这部分数据会丢失

# 数据类型

## string

string 类型是二进制安全的，一个键最大能存储512MB数据。存储结构分位整数、EmbeddingString、SDS，整数存储字符串长度小于21且能转化为整数的字符串；EmbeddingString 存储字符串长度小于 39 的字符串；SDS 存储不满足上述条件的字符串。

- 只对长度小于或等于 21 字节，并且可以被解释为整数的字符串进行编码，**使用整数存储**

- 尝试将 RAW 编码的字符串编码为 EMBSTR 编码，**使用EMBSTR 编码**

- 这个对象没办法进行编码，尝试从 SDS 中移除所有空余空间，**使用SDS编码**

**SDS**

```c++
/*
 * 保存字符串对象的结构
 */
struct sdshdr {
    
    // buf 中已占用空间的长度
    int len;

    // buf 中剩余可用空间的长度
    int free;

    // 数据空间
    char buf[];
};

/*
 * 返回 sds 实际保存的字符串的长度
 *
 * T = O(1)
 */
static inline size_t sdslen(const sds s) {
    struct sdshdr *sh = (void*)(s-(sizeof(struct sdshdr)));
    return sh->len;
}

/*
 * 返回 sds 可用空间的长度
 *
 * T = O(1)
 */
static inline size_t sdsavail(const sds s) {
    struct sdshdr *sh = (void*)(s-(sizeof(struct sdshdr)));
    return sh->free;
}
```

**SDS扩容**

当字符串长度小于SDS_MAX_PREALLOC (1024*1024)，那么就以2倍的速度扩容，当字符串长度大于SDS_MAX_PREALLOC，那么就以+SDS_MAX_PREALLOC的速度扩容。

**SDS缩容**

释放内存的过程中修改len和free字段，并不释放实际占用内存。

## hash / 字典

底层使用哈希表实现，结构为数组+链表。redis 字典包含两个哈希表，用于在 redis 扩缩容时的渐进式rehash。

# 线程

redis 4.0 之后，新增了后台线程处理重操作，比如清理脏数据、无用连接的释放、大 key 的删除，但是工作线程仍然是单线程。基于内存的redis，性能瓶颈不在处理器，主要受限于内存和网络。redis 6.0 新增 I/O 线程，用于处理处理 I/O 的读写，使多个socket的读写可以并行，为工作线程减压。

# 其他

## rehash

在集群模式下，一个 redis 实例对应一个 RedisDB，一个RedisDB对应一个Dict，一个Dict对应两个Dictht（dict hash table），正常情况下只用到 ht[0]；ht[1] 在 rehash 时使用。

rehash 是redis在字典扩缩容时进行的操作，rehash 过程中，字典同时持有两个哈希表，删除、查找、更新等操作都会在两个哈希表上进行，新增操作只在新的哈希表进行，原有的数据的搬迁通过后续的客户端指令（hset、hdel）及定时任务完成。

**触发条件**

扩容条件：数据量大于哈希表数组长度时触发，如果数据量大于数组长度5倍，则进行强制扩容；缩容条件：数据量小于数组长度的10%。

**问题**

- 满容驱逐，由于 rehash 过程中会为新的哈希表申请空间，导致满容状态下大范围淘汰key

## lpush

## epoll

redis中使用IO多路复用（多路是指多个socket连接，复用指的是复用一个线程）的epoll方式。

# 问题

## 为什么吞吐量高？

- IO多路复用
- 基于内存的数据操作

## 过期机制？

可从过期策略和淘汰策略来分析。过期策略分位被动删除和主动删除两类，被动删除主要是读取过期key，惰性删除；主动删除，包括定期清理和内存超过阈值触发主动清理。

淘汰策略有多种。

| 淘汰策略        | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| volatile-lru    | 仅对设置了过期时间的key采取lru淘汰                           |
| volatile-lfu    | 对设置了过期时间的key执行最近最少使用淘汰，redis 4.0开始支持 |
| volatile-ttl    | 仅对设置了过期时间的key生效，淘汰最早写入的key               |
| volatile-random | 随机回收设置过期时间的key                                    |
| allkeys-lru     | 对所有key都采用lru淘汰                                       |
| allkeys-random  | 随机回收所有key                                              |
| allkeys-lfu     | 对所有key执行最近最少使用淘汰，redis 4.0开始支持             |
| no-enviction    | 默认策略，向客户端返回错误响应                               |

**注：**

- LRU：Least Recently Used，即最近最久未使用。如果一个数据在最近一段时间没有被访问到，那么在将来它被访问的可能性也很小。通常使用map+链表的方式实现，map判断key是否存在，链表保存顺序。
- LFU：Least Frequently Used，最近最少使用算法。与LRU算法的不同之处，LRU的淘汰规则是基于访问时间，而LFU是基于访问次数的。
- FIFO：First in First out，先进先出。

# 参考

- https://www.cnblogs.com/madashu/p/12832766.html
- https://www.cnblogs.com/aspirant/p/9166944.html
- https://i6448038.github.io/2019/12/01/redis-data-struct/