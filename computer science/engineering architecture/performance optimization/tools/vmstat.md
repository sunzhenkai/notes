---
title: 性能分析 - vmstat
categories: 
    - [架构, 性能优化]
tags:
    - 性能分析
date: "2022-01-26T00:00:00+08:00"
update: "2022-01-26T00:00:00+08:00"
---

# 安装

```shell
# centos
```

# 命令

```shell
$ vmstat <period> <count>
```

# 输出

```shell
r 运行队列，分配到 CPU 的进程数
b 堵塞进程数
swpd 使用虚拟内存
free 空闲物理内存
buff 缓冲占用内存
cache 缓存占用内存
si 每秒从磁盘读取虚拟内存大小
so 每秒写入磁盘虚拟内存大小
bi 每秒从块设备接受块数量
bo 每秒发送的块数量
in 每秒 cpu 中断次数，包括时间中断
cs 每秒上下文切换次数
us 用户 cpu 时间
sy 系统 cpu 时间
id 空闲 cpu 时间
wa 等待 io cpu 时间
st 从虚拟机窃取时间
```

