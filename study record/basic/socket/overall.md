---
title: Socket 编程
categories: 
    - 研习录
    - Socket
tags:
    - 研习录
date: 2024/1/31 00:00:00
---

# Basic

![img](overall/StatediagramforserverandclientmodelofSocketdrawio2-448x660.png)

## Code

- [SocketServer & SocketClient](https://github.com/sunzhenkai/cook-cpp/tree/master/src/study/socket/basic)
- [[Example] Echo Service](https://github.com/sunzhenkai/cook-cpp/tree/master/src/study/socket/echo_service)

# epoll

## methods

```c++
epoll_create(...)  // 创建 epoll
epoll_ctl(...)     // 向 epoll 注册 socketfd
epoll_wait(...)    // 从 epoll 获取事件
```

## steps

- `socket()`
- `bind()`
- `listen()`
- **epoll**
  - `epoll_create()`
  - `epoll_ctl()` : Add server socket to epoll instance
  - `epoll_wait()`
- `accept()`
- `epoll_ctl()`  :  Add client socket to epoll instance
- `read()`
- `write()`

# Reference

- [socket-programming-in-c](https://www.geeksforgeeks.org/socket-programming-cc/)
- [epoll-server example](https://github.com/hnakamur/luajit-examples/blob/master/socket/c/epoll-server.c)