---
title: c++ - perf
categories: 
  - [coding, c++]
tags:
  - c++
date: "2022-01-26T00:00:00+08:00"
update: "2022-01-26T00:00:00+08:00"
---

# 工具

gprof、perf、gperftools、valgrind。

# Perf

perf 工具默认生成记录文件 perf.data，读写路径是 pwd。

## 安装

```shell
# ubuntu
sudo apt install linux-tools-common linux-tools-generic linux-tools-`uname -r` -y

# centos
sudo yum install perf -y
```

```shell
# source code
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.134.tar.gz
tar -xf linux-5.10.134.tar.gz
cd linux-5.10.134/tools/perf

make  # 如果编译出错，可以尝试修改 Makefile.config 里面的 FLAGS, 移除 -Werror
cp perf /usr/bin/
```

## 工具

### bpftrace

```shell
bpftrace -e 'profile:hz:99 /pid == 1/ { @[ustack] = count(); }'
```

### google-perftools + brpc

```shell
apt install google-gperftools
```

```shell
pprof-symbolize --text 0.0.0.0:9500 --seconds=5
pprof-symbolize 0.0.0.0:9500 --seconds=5
```

### brpc/tools/pporf

`./brpc/tools/pprof` 是一个 prel 脚本文件，不需要编译

```shell
./brpc/tools/pprof --text localhost:9500/pprof/profile
```

### top

系统性能分析工具。

**参数**

```shell
-e 指定 event，多个 event 用 , 分隔
-s 指定分类聚合列， 默认是函数，还有 comm（命令）、pid 等
```

**使用**

```shell
# 所有进程
$ perf top 
# 指定进程
$ perf top -p <pid> 
```

### stat

运行命令 / 指定 pid，并收集性能统计数据。

### record

运行命令 / 指定 pid，并收集分析数据至 perf.data。

```shell
# 指定 pid
$ pid=$(pgrep <program-name>)

# 查看报告
$ perf report --show-total-period
```

### report

读取 perf.data，展示分析结果。

```shell
$ perf report 

# 参数
--show-total-period 展示总耗时列
-a 统计系统范围内数据
```

### diff

对比两个 `perf.data` 内容的区别，使用场景比如对比改动前后的变化。

### archive

用来打包 perf.data 中使用到的环境数据，用于离线分析。

```shell
# 打包
$ perf archieve

# 分析
$ tar xvf perf.data.tar.bz2 -C ~/.debug
```

## 使用

```shell
# 查看系统全部耗时
$ perf top

# pid
$ pid=$(pgrep <program-name>)

# 记录数据
$ perf record -e cpu-clock -F 99 -p $pid -g -- sleep 60 # 记录 60 秒数据

# 展示记录数据的分析结果
$ perf report --show-total-period
$ perf report --show-total-period$ -i <perf.data> # 指定记录文件
```

## 火焰图

使用 [这里](https://github.com/brendangregg/FlameGraph) 生成火焰图。

```shell
# 下载工具
$ git clone https://github.com/brendangregg/FlameGraph

# 生成火焰图
$ sudo perf script | FlameGraph/stackcollapse-perf.pl | FlameGraph/flamegraph.pl > flamegraph.svg
```

# 参考

- https://stackoverflow.com/questions/375913/how-can-i-profile-c-code-running-on-linux

# 问题

```shell
```

