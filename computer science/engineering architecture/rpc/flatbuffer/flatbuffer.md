---
title: flatbuffer
categories: 
  - [架构, rpc, dsl]
tags:
  - flatbuffer
date: "2022-04-22T00:00:00+08:00"
update: "2022-04-22T00:00:00+08:00"
---

# 定义

```flatbuffer
table Weapon {
  name:string;
  damage:short;
}
```

# 转换

```c++
flatbuffers::FlatBufferBuilder fbb;
...

const Weapon * weapon = GetWeapon(fbb.GetBufferPointer());
```

# 打印

```c++
// 打印结构
#include "flatbuffers/minireflect.h"

RequestT req;
flatbuffers::FlatBufferBuilder fbb;
fbb.Finish(Request::Pack(fbb, &req));
std::string debug_info =  flatbuffers::FlatBufferToString(fbb.GetBufferPointer(), RequestTypeTable());
```

