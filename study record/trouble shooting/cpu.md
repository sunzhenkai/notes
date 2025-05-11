---
title: 问题排查 - CPU
categories: 
    - 研习录
tags:
    - 研习录
date: "2024-07-16T00:00:00+08:00"
---

# 原因分析

## 计算任务

- 计算量过大的任务占用过多 CPU
- 死循环

## 上下文切换

- 死锁
- 频繁加锁
- 过多的并发
- 内存不足
- 频繁 GC（Java、GO 等语言）

# 问题排查

## 借助 TOP 命令

```shell
top -Hp {pid}  # 查看指定进程内各线程占用 CPU 的情况
```

**查看线程数量**

```shell
ps -p {pid} -L | wc -l
```

## 排查进程的上下文切换情况

### pidstat

```shell
pidstat -w -p {pid}
```

其中，`<PID>` 是目标进程的进程 ID。上述命令将显示指定进程的 CPU 上下文切换统计信息，包括自愿切换（voluntary switches）和非自愿切换（non-voluntary switches）。

```shell
Linux 4.14.301-224.520.amzn2.x86_64 (...) 	2024年07月04日 	_x86_64_	(32 CPU)

10时23分19秒   UID       PID   cswch/s nvcswch/s  Command
10时23分19秒     0   3637168      0.17      0.00  ...
```

```shell
# 安装
yum install sysstat -y
```

### perf

```shell
perf stat -e cs,<event> -p <PID>
# event: cs (所有模式切换) , cs:u (用户模式切换), cs:k (内核模式切换)
$ perf stat -e cs,cs:u,cs:k -p 3637168  # Ctrl-C 结束收集

^C
 Performance counter stats for process id '3637168':

            44,981      cs
                 0      cs:u
            44,981      cs:k

      27.447834538 seconds time elapsed
```

**perf stat 和 perf record 区别**

- perf stat

- 快速查看程序基本性能指标
- 采集 CPU 指令、缓存命中率、上下文切换等

- perf record

- 可采集系统或特定进程的性能事件
- 采集指令、缓存、分支等事件
- 可导出文件，用于后续的分析

```shell
yum install perf -y
```

# 其他问题

- 如何区分是计算任务占用 CPU 还是过多上下文切换占用任务
- 区分 IO 线程和 Work 线程的必要性