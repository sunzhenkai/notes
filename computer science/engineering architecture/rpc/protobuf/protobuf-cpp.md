---
title: protobuf - c++
categories: 
  - [架构, rpc, dsl]
tags:
  - protobuf
date: 2022/04/22 00:00:00
update: 2022/04/22 00:00:00
---

# Descriptor & Reflection

## message

```c++
syntax = "proto3";

message Sea {
  string name = 1;
}

message World {
  int64 age = 1;
  repeated string tag = 2;
}
```

## Descriptor & Reflection

```c++
World wd{};

// protobuf 3
auto age = World::GetDescriptor()->FindFieldByName("age"); 
// protobuf 2
auto age = wd.GetDescriptor()->FindFieldByName("age"); 

// 设置单值
World::GetReflection->SetInt64(&wd, age, 10);
// 设置 repeated 字段
World::GetReflection()->AddString(&wd, tag, "a");
World::GetReflection()->AddString(&wd, tag, "b");
World::GetReflection()->SetRepeatedString(&wd, tag, 1, "c");

// 设置 submessage
wd.mutable_sea()->set_name("pacific");
```

# Json

```c++
#include <google/protobuf/util/json_util.h>

// message -> json
std::string output;
google::protobuf::util::MessageToJsonString(message, &output);

// json -> message
SomeMessage msg;
std::string input;
google::protobuf::util::MessageToJsonString(input, &msg);
```

# cmake

- https://stackoverflow.com/questions/63309544/cmake-protobuf-external-to-application-code
