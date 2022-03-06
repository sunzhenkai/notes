---
title: c++ sizeof
categories: 
	- [coding, c++]
tags:
	- c++
date: 2020/11/21 12:00:00
---

# 使用

```c++
sizeof(type/object)

查询对象/类型实际大小
```

# 示例

```c++
// 定义结构
struct Empty {};
struct Base { int a; };
struct Derived : Base { int b; };
struct Bit { unsigned bit: 1; };

// 实例化
Empty e;
Derived d;
Base& b = d;
[[maybe_unused]] Bit bit;
int a[10];
      
// 查询大小
sizeof e        // 1  Empty类大小
sizeof &e       // 8  类指针大小
sizeof(Bit)     // 4  Bit类大小
sizeof(int[10]) // 40 
sizeof(a)       // 40
((sizeof a) / (sizeof *a))    // 计算数组a的长度
((sizeof a) / (sizeof a[0]))  // 计算数组a的长度
sizeof d        // Derived对象大小
sizeof b        // Base对象大小
```

