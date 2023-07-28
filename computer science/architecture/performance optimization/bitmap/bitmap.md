---
title: bitmap
categories: 
    - [架构, 性能优化, bitmap]
tags:
    - bitmap
date: 2021/10/09 00:00:00
update: 2021/10/09 00:00:00
---

# bitmap

bitmap（位图），是一个位数组，物理层面是内存中的一块连续区域，形式上可以表示为 `01010001011`。

## 用途

- 布隆过滤器

# roaring bitmap

对位图进行空间优化，思想是高位用于分桶，只存储低位。比如，如果存储一个 32 位整数，使用高 16 位获取分桶，每个分桶是一个 bitmap，低 16 位用来确定 bitmap 中的一个 bit，用 bit 值的 0/1 来标识数据是否存在。这样实际存储过程中，可以省略每个整数的高 16 位，理想情况下占用空间减少 50%。

## 用途

- lucene 存储倒排索引（其倒排索引 id 递增）

# 参考

- https://www.jianshu.com/p/818ac4e90daf
- https://www.cnblogs.com/mzhaox/p/11210108.html