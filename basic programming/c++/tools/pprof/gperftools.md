---
title: gperftools
categories: 
	- [coding, c++, tools, gperftools]
tags:
	- c++
    - gperftools
date: 2022/06/10 00:00:00
update: 2022/06/10 00:00:00
---

# 安装

```shell
$ yum install gperftools gperftools-devel -y
```

# Heap Profile

```shell
# dump
$ env LD_PRELOAD="/usr/lib64/libtcmalloc_and_profiler.so" HEAPPROFILE="heap-profile" <binary>
$ env LD_PRELOAD="/usr/lib64/libtcmalloc.so" HEAPPROFILE="heap-profile" <binary>
$ env LD_PRELOAD="/usr/lib64/libtcmalloc.so" HEAPPROFILE="/tmp/profile" HEAP_PROFILE_TIME_INTERVAL=60 <binary>

# analysis
$ pprof --text <binary> /tmp/profile....heap
$ pprof --svg <binary> /tmp/profile....heap > heap.svg
```
