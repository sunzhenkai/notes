---
title: c++ tips
categories: 
	- [coding, c++]
tags:
	- c++
date: 2021/12/21 00:00:00
---

[toc]

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

# lambda

## lambda 参数

```shell
# 定义接受 lambda 作为参数的函数
## 方式 1
template<typename Func>
void lmb(Func &&f) {
    f();
}
## 方式 2
void lmb2(std::function<void()> &&f) {
    f();
}

# 调用
lmb([]() {
		std::cout << "run lambda" << std::endl;
});
lmb2([]() {
    std::cout << "run lambda 2" << std::endl;
});

# 定义变量
auto f = []() {
    std::cout << "lambda variable" << std::endl;
};
# 调用
lmb(f);
lmb2(f);
```

# 获取变量类型

```c++
int c = 0;
std::vector<decltype(c)> cs;   // 定义 vector，元素类型和 c 相同
cs.emplace_back(c);
```

