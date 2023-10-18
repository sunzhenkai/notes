---
title: c++ 手册
categories: 
  - [coding, c++]
tags:
  - c++
date: 2020/11/10 21:00:00
---

# 数据结构

**可变容量数组 vector**

```c++
#include <vector>
// 初始化
std::vector<T> vec;
std::vector<T> vec(5, 0); // 长度 5, 元素值
std::vector<T> vec = {1, 2, 3, 4, 5};
std::vector<T> vec(arr, arr + sizeof(arr) / sizeof(arr[0]));
std::vector<T> vec(container.begin(), container.end());
// 插入
vec.push_back(element);
vec.emplace_back(element);
vec.insert(iterator, element);
// 访问元素
vec.at(index);
vec[index];
vec.front();
vec.back();
// 删除元素
vec.pop_back();
vec.erase(iterator);
vec.erase(start_iterator, end_iterator);
// 大小和容量
vec.resize();
```

**双向链表 list**

```shell
```

