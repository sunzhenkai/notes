---
title: flatbuffer
categories: 
	- [架构, rpc, dsl]
tags:
	- flatbuffer
date: 2022/04/22 00:00:00
update: 2022/04/22 00:00:00
---

# 打印

```c++
// 打印结构
Request req;
flatbuffers::FlatBufferBuilder fbb;
fbb.Finish(Request::Pack(fbb, &req));
std::string debug_info =  flatbuffers::FlatBufferToString(fbb.GetBufferPointer(), RequestTypeTable());
```