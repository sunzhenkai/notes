---
title: memset & fill
categories: 
  - [coding, c++]
tags:
  - c++
date: "2020-11-21T12:00:00+08:00"
---

# memset

## 头文件

```c++
// c
#include <string.h>
// c++
#include <cstring>
```

## 使用

```c++
void *memset( void *dest, int ch, size_t count );
dest : 需要填充内存指针
ch   : 填充内容，被强转成unsigned char使用
count: 需要填充数量

dest指针开始前count个字节的每个字节赋值为ch
```

## 示例

```c++
char str[] = "hello world";
memset (str, '-', 5);
puts(str);

// output
"----- world"
```

# fill

## 头文件

```
#include <algorithm>
```

## 使用

```c++
template< class ForwardIt, class T >
constexpr void fill( ForwardIt first, ForwardIt last, const T& value );
first : 开始迭代器
last  : 中止迭代器
value : 需要填充的值
```

