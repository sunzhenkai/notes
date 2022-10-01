---
title: protobuf
categories: 
	- [架构, rpc, dsl]
tags:
	- protobuf
date: 2022/04/22 00:00:00
update: 2022/04/22 00:00:00
---

# 定义

```protobuf
syntax = "proto2";
package a.b;
```

# 命令行

```shell
protoc --go_out=<gen-output-path> -I<deps-path> <src-protocols>
```

