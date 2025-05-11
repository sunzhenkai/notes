---
title: IO 模型
categories: 
  - 研习录
tags:
  - 研习录
  - RPC
date: "2024-01-26T00:00:00+08:00"
---

# IO 模型分类

常见的 IO 模型分为以下五类。

- 同步阻塞 IO（BIO）
- 同步非阻塞 IO（NIO）
- IO 多路复用
- 信号驱动IO
- 异步非阻塞 IO（AIO）

# 客户端连接模式

从客户端角度，可以分为短连接、连接池、单连接，后两者属于长连接。对于单连接实现起来相对复杂，Server 端通常要实现 IO 多路复用，通常提供异步非阻塞 API，同一链接可以被多个线程使用。连接池的方式实现起来相对简单，通常提供阻塞式 API。

# 同步、异步、阻塞、非阻塞

参见 [这里](../../basic/cs)。

# PORT 复用

以 seastar 框架为例。首先，监听端口，并设置端口复用。

## 服务端

### 监听

```c++
// int port = 80;
listen_options lo;
lo.reuse_address = true;
listener = engine().listen(make_ipv4_address({port}), lo);
```

### 等待

调用框架 accept 方法，等待连接。

```c++
keep_doing([this] {
  return listener->accept().then([this] (seastar::accept_result &&ar) mutable {
    handle_connection(std::move(ar));
});
```

当有新链接创建时，返回 accept_result。

```shell
/// The result of an server_socket::accept() call
struct accept_result {
    connected_socket connection;  ///< The newly-accepted connection
    socket_address remote_address;  ///< The address of the peer that connected to us
};
```

### 处理

```shell
handle_connection(seastar::accept_result &&ar) {
  do_until(
    [ar] { return !ar->connection->is_valid(); },
    [this, ar]() mutable { return handle_one_session(ar);
  })
}

handle_one_session(seastar::accept_result &ar) {
  ar->connection.input().read_exactly(/*size of header*/).read_exactly(/*size of body*/).then(/* processor */);
}
```

### 回写数据

```c++
send(seastar::accept_result &ar, seastar::net::packet &&pack) {
  ar->connection.output().write(std::move(pack));
  ar->connection.output().flush();
}
```

## 客户端

### 创建连接

```c++
engine().net().connect(make_ipv4_address(ipv4_addr{server_addr}))
  .then_wrapped([this, server_addr](auto &&f) mutable {
    seastar::connected_socket fd = std::move(f.get0());
    fd.set_nodelay(true);
    fd.set_keepalive(true);
  });
```

### 发送数据

和 server 端回写数据一致。

```c++
send(seastar::accept_result &ar, seastar::net::packet &&pack) {
  ar->connection.output().write(std::move(pack));
  ar->connection.output().flush();
}
```

### 读取响应

```c++
read(seastar::connected_socket &&fd) {
  do_until(
    [this]{ return !is_running; },
    [&]() mutable {
      fd->input().read_exactly(/*size of header*/).read_exactly(/*size of body*/).then([] {
        /*
        1. get request id from response
        2. dispatch by request id (notify blocked thread)
        */
      })
    }
	)
}
```

## QA

### 是否并发处理请求

是的，server 端监听端口，有连接创建时，保存连接，并按顺序读取 header 和 body，读取一个完整请求后，交由 background 线程处理。

### 如何保证 request 和 response 一一对应

server 端不保证按请求顺序返回相应，由客户端根据响应信息进行路由（比如 request_id 或自增的 request_number）。