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
$ env LD_PRELOAD="/usr/lib64/libtcmalloc.so" HEAPPROFILE="/tmp/heap.hprof" <binary>
```

