---
title: linux sre
categories: 
	- [linux,notes]
tags:
	- Linux
date: 2021/11/22 00:00:00
update: 2021/11/22 00:00:00
---

# 磁盘性能评估

## 写入空数据

```shell
$ dd if=/dev/zero of=test.data bs=2G count=10
```

