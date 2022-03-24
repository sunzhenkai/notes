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

# 分隔字符串

```c++
std::string server_address = "127.0.0.1:80";
std::vector<std::string> result;
boost::split(result, server_address, boost::is_any_of(":"));

result.at(0); // 127.0.0.1
result.at(1); // 80
```

# 类型转换

```c++
// string -> int
stoi("80")
```

