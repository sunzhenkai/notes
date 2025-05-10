---
title: install seastar
categories: 
  - [架构,java,框架,seastar]
tags:
  - seastar
date: "2021-12-15T00:00:00+08:00"
update: "2021-12-15T00:00:00+08:00"
---

# 系统配置

## aio-max-nr

```shell
$ sudo vim /etc/sysctl.conf
# 添加
fs.aio-max-nr = 1048576
$ sudo sysctl -p /etc/sysctl.conf
```

## perf_event_open

```shell
$ sudo vim /etc/sysctl.conf
# 添加
kernel.perf_event_paranoid = -1
$ sudo sysctl -p /etc/sysctl.conf
```

# 命令行配置

```shell
# debug
--mode=debug
```

