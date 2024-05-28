---
title: c++ - holes
categories: 
  - [coding, c++]
tags:
  - c++
date: 2022/02/09 00:00:00
---

# 容易 Core Dump 的情形

## 容器重新分配内存导致的非法内存访问

```c++
// 定义结构
struct Biz {...};
// 定义容器
std::vector<Biz> bizes;
bizes.emplace_back();  // 添加一个元素
auto p_biz = &bizes.back(); // 保存指针
bizes.emplace_back(); // 添加一个元素. 该操作可能会使指针 p_biz 失效, 因为内存重新分配
```

# 模板

- 模板类的定义和实现不能分隔
  - https://stackoverflow.com/questions/115703/storing-c-template-function-definitions-in-a-cpp-file
  - https://isocpp.org/wiki/faq/templates#templates-defn-vs-decl
  - https://isocpp.org/wiki/faq/templates#separate-template-class-defn-from-decl

> 类似需要在编译期展开的代码实现，不能放在 cpp 文件中，而应该放在 header 中

# 静态变量初始化

```c++
// s.h
#ifndef S_H
#define S_H
class S {
  static int v;
};
int S::v = 0;
#endif
```

上面的代码在链接时会报错。声明保护（gragma once 或使用 ifndef 判断）可以解决单个编译单元（单个源文件）的重复声明错误，但不能避免多个编译单元在链接时的重复定义错误。要解决这个问题，需要把静态变量的声明和初始化放在不同的文件里面。

```c++
// s.h
#ifndef S_H
#define S_H
class S {
  static int v;
};
#endif

// s.cpp
int S::v = 0;
```

# undefined reference to

- 未连接库
- 编译库的编译器版本不一致，ABI 不兼容
- `find_package` 的顺序，在某些情况下也有可能会导致这个问题
  - 被依赖先调用 find_package


## 编译 C 库使用 C++ 语法

```shell
gcc -lstdc++ code.c
```

