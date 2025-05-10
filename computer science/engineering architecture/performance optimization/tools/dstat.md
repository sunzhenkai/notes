---
title: 性能分析 - dstat
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
sudo yum install -y dstat
```

# 命令

```shell
$ dstat
```

# 参数

默认参数为 `-cdngy`。

```shell
-c cpu 信息
-C cpu 信息，指定核心，如 -C 0,2,4
-d disk 信息
-n net 信息
-g page 信息
-y system 信息
```

# 输出

```shell
# cpu 相关
usr 用户消耗 cpu 时间占比
sys 系统消耗 cpu 时间占比
idl cpu 空闲时间占比
wai io 等待消耗的 cpu 占比
hiq 硬中断
siq 软中断

# system 相关
int 中断次数
csw 上下文切换次数

# disk
read 读取磁盘总数
write 写入磁盘总数

# net
recv 网络设备结束数据总数
send 网络设备发送数据总数

# page 相关（系统分页活动）
in 换入次数
out 换出次数
```

