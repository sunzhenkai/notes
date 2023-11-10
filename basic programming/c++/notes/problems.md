---
title: c++ - holes
categories: 
  - [coding, c++]
tags:
  - c++
date: 2022/02/09 00:00:00
---

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

## 编译 C 库使用 C++ 语法

```shell
gcc -lstdc++ code.c
```

