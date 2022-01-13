---
title: c++ tips
categories: 
	- [coding, c++]
tags:
	- c++
date: 2021/12/21 00:00:00
---

# namespace 别名

```c++
// 设置 namespase 别名
namespace tcxx = ::apache::thrift::stdcxx;
// 使用
tcxx::function<void()> 
```

# 引用别名

```c++
using S = ::space::Server;
auto server = S(80)
```

# 函数参数

```c++
setRouters(std::function<void(seastar::httpd::routes & )> routes) 
{
  // ...
}
```

