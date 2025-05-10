---
title: protobuf - go
categories: 
  - [架构, rpc]
tags:
  - protobuf
date: "2022-05-10T00:00:00+08:00"
update: "2022-05-10T00:00:00+08:00"
---

# Tips

## optional 字段生成基本变量指针

对于 proto2 语法，如果基础字段添加了 optional 修饰，那么生成的 go 文件对应的字段是指针。

```shell
// proto 定义
syntax = "proto2";

message Foo {
    optional int32 id = 1;
    optional string bar = 2;
}

// go 文件
type Foo struct {
  ...
  
	Id  *int32  `protobuf:"varint,1,opt,name=id" json:"id,omitempty"`
	Bar *string `protobuf:"bytes,2,opt,name=bar" json:"bar,omitempty"`
}
```

go 语法不能对常量、右值取地址，无法直接赋值给对应变量。proto 提供了对应的 [wrapper](https://github.com/golang/protobuf/blob/ae97035608a719c7a1c1c41bed0ae0744bdb0c6f/proto/wrappers.go#L19) 工具，传入右值，返回指针。

```go
foo := pb.Foo{}
foo.Id = proto.Int32(23)
```

