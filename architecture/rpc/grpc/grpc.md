---
title: gRPC
categories: 
	- [架构, rpc, gRPC]
tags:
	- gRPC
date: 2021/05/24 00:00:00
update: 2021/05/24 00:00:00
---

# Introduction

gRPC 是谷歌开源的一款 RPC 框架，protocal buffers 作为它的 IDL（Interface Definition Language，接口定义语言），也可以作为其底层数据交换格式。

# Overview

在 gRPC，一个客户端应用可以直接调用不同机器上服务端的方法。在一些 RPC 系统中，gRPC 是基于以下思路，定义一个服务接口，指定可以远程调用的方法，机器参数和返回类型；在服务端，实现这个接口，并且运行一个 gRPC 服务，来处理客户端的请求；在客户端，保存一个存根（stub，在一些语言中简称为客户端）提供和服务端相同的方法。

![Concept Diagram](grpc/landing-2.svg)

# Protocol Buffers

默认情况下，gRPC 使用 [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview) （Protobuffer，PB，谷歌开源的且成熟的序列化结构化数据的机制/工具）。使用 PB ，首先需要在 proto 文件中定义一个需要序列化的结构。

```protobuf
message Person {
  string name = 1;
  int32 id = 2;
  bool has_ponycopter = 3;
}
```

如果需要定义一个 Service。

```protobuf
// file: greeter.proto

syntax = "proto3";
// The greeter service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
```

如下命令。

```shell
$ protoc --java_out=jv greeter.proto
```

并不会生成用于 RPC 的 client 和 server，需要使用如下命令。

```shell
$ protoc --java_out=jv --grpc-java_out=jv greeter.proto
```

在使用之前，需要安装工具 `protoc-gen-grpc-java`，工具下载 / 本地编译步骤参考[这里](https://github.com/grpc/grpc-java/tree/master/compiler)。至于下载，可以移步 [这里](https://mvnrepository.com/artifact/io.grpc/protoc-gen-grpc-java)，选择一个版本并点击链接，在介绍表格部分有 Files 字段，点击 `View all` ，现在指定平台的可执行文件即可，然后运行如下命令。

```shell
$ protoc --plugin=protoc-gen-grpc-java=/Users/wii/Downloads/protoc-gen-grpc-java-1.38.0-osx-x86_64.exe --grpc-java_out=jv --java_out=jv greeter.proto 
```

**注意** 指定 plugin 时，使用决定路径。

查看生成结果。

```shell
$ ls jv
GreeterGrpc.java       GreeterOuterClass.java
```

# Core Concepts

## 服务定义

gRPC 默认使用 Protocol Buffers 作为服务定义语言，如果需要也可以使用其他可选项。

```protobuf
service HelloService {
  rpc SayHello (HelloRequest) returns (HelloResponse);
}

message HelloRequest {
  string greeting = 1;
}

message HelloResponse {
  string reply = 1;
}
```

gRPC 允许定义多种类型的服务方法。

- 一元 RPCs（Unary RPCs），客户端发送一次请求，得到一次响应，和通常的方法调用类似

  ```protobuf
  rpc SayHello(HelloRequest) returns (HelloResponse);
  ```

- 服务端流 RPCs（Server streaming RPCs），客户端向服务端发送一次请求，得到一个流来读取一系列的消息。客户端从返回的流中读取数据，直到没有更多信息。gRPC 保证一次独立调用中消息的顺序

  ```protobuf
  rpc LotsOfReplies(HelloRequest) returns (stream HelloResponse);
  ```

- 客户端流 RPCs（Client streaming RPCs ），客户端使用流，向服务端发送一系列的消息。客户端结束写入后，等待服务端读取并返回一个响应。同样，gRPC 保证一次独立调用中消息的顺序

  ```protobuf
  rpc LotsOfGreetings(stream HelloRequest) returns (HelloResponse);
  ```

- 双向流 RPCs（Bidirectional streaming RPCs），客户端和服务端通过读写流发送消息序列，两个流操作独立，所以客户端和服务端可以以任意顺序读写。比如，服务端可以等待接受到所有消息后返回响应消息序列；也可以每接受一个消息，返回一个响应消息。

  ```protobuf
  rpc BidiHello(stream HelloRequest) returns (stream HelloResponse);
  ```

## 使用 API

首先，在 `.proto` 文件中定义服务（service），gRPC 提供 PB（protocol buffer）编译插件，来生成客户端和服务端代码。gRPC 用户通常在客户端调用这些API，在服务端实现这些 API。

- 在服务端，实现服务接口定义的方法，并且运行一个 gRPC 服务来处理客户端的请求。gRPC 基础设施解码进来的请求，执行服务方法，并编码服务响应
- 在客户端，有一个本地对象，称作 stub（对于一些语言，术语为 client），其实现和服务端相同的方法。client 可以在本地对象上调用这些方法，使用合适的 pb 消息类型包装调用的参数，gRPC接着传送请求给服务端，并且返回服务端的 pb 格式消息响应。

## 同步 vs 异步

gRPC 在大部分语言中，具备异步和同步风格的接口。

## RPC 声明周期

### Unary RPC

- 当客户端调用 stub 的方法时，服务端会被告知这次调用的 [metadata](https://grpc.io/docs/what-is-grpc/core-concepts/#metadata)，包括方法的名称，请求的超时时间等
- 服务端可以马上返回自己的初始 metadata（在响应前必须传送），也可以等待客户端的请求消息，具体的行为由应用程序指定
- 一但服务器得到了完整的客户端请求消息，会做对应的工作并构造一个响应消息。接着返回响应，及详细的状态（status）和可选的尾部 metadata。
- 如果返回状态是 OK，客户端会得到这个响应，这就完成了客户端的调用。

### Server streaming RPC

server streaming RPC 和 unary RPC 类似，不同的是服务端在响应中返回一个消息流（a stream of message）。在所有的消息发送完后，详细的状态码和可选的尾部 metadata 会被传送给客户端。

### Client streaming RPC

服务端返回单个消息的实际，通常是接受到所有消息后，但并非必须如此。

### Bidirectional streaming RPC

双向流RPC，服务端接受到的客户端的 metadata、请求方法、deadline。

## Deadlines / Timeouts

gRPC 允许客户端指定超时时间。服务端可以知道一个指定 RPC 调用是否超时，或者剩余处理时间。

## 终止 RPC

可能存在服务端成功返回，但是客户端请求超时的情况。也有可能，服务端在客户端还在发送请求时来结束本次RPC。

## 取消 RPC

服务端和客户端都可以在任意时间取消一次 RPC 请求。

## Metadata

Metadata 包含一次特定 RPC 请求的信息，数据格式是 k-v 对的形式，key为string，value可以是string，也有可能是二进制数据。

## Channels

一个 gRPC 通道提供一个和指定host和port的 gRPC 服务器的连接，当创建一个客户端 stub 时会用到。客户端可以指定通道参数，来修改 gPRC 的默认行为，比如控制消息压缩开关。一个 channel 包含状态，包括 `connected` 和 `idle`。

gRPC 怎么处理关闭 channel 的流程，语言间有所不同。

# Appendix

## thrift VS protocol buffer

- pb 生成 service 的 client 和 server 代码，需要额外的插件