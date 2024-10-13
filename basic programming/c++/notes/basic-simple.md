---
title: c++ 手册
categories: 
  - [coding, c++]
tags:
  - c++
date: 2020/11/10 21:00:00
---

# 定义变量



# 基础操作

## 字符串

**c++**

```c++
// 查找
size_type idx = str.find(s); // 未查到: (idx == std::string::npos)
```

# 容器

**顺序容器**

- [x] 可变数组 vector
- [x] 双向链表 list
- [ ] 单向链表 forward_list
- [ ] 双端队列 deque
- [ ] 固定数组 array

**关联容器**

- [ ] 集合 set、multiset
- [ ] 映射 map、multimap

**容器适配器**

- [ ] 栈 stack
- [ ] 队列 queue
- [ ] 优先队列 priority_queue

## **可变容量数组 vector**

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

## **双向链表 list**

```c++
#include <list>
// 初始化
std::list<T> lst;
std::list<T> lst = {1, 2, 3, 4, 5};
std::list<T> lst(container.begin(), container.end());
// 插入
lst.push_back(element);
lst.push_front(element);
lst.insert(it, element);
lst.insert(it, n, element); // 在 it 插入 n 个 element
lst.insert(it, begin, end); // 在 it 插入迭代器 [begin, end) 内元素
// 赋值 (清空元素并重置为指定元素)
assign(begin, end);  
assign(n, element);
// 访问
l.begin(); // 返回迭代器
l.end(); // 返回迭代器
l.front(); // 返回元素
l.back(); // 返回元素
// 删除
erase(begin, end);
erase(it);
remove(element);
clear();
pop_back();
pop_front();
```

## [单向链表 forward_list](https://en.cppreference.com/w/cpp/container/forward_list)

```c++
#include <forward_list>
// 初始化
std::forward_list<int> fl;
std::forward_list<int> fl {1, 2, 3};
std::forward_list<int> fl(n, element);
std::forward_list<int> fl(begin, end);
// 插入
fl.push_front(element);
fl.insert_after(iter, element);
// 赋值 (清空元素并重置为指定元素)
// 访问
// 删除
```

## unordered_set

```c++
// 修改
insert(Key&&)
emplace(Args&&)
erase(const Key&)
merge()
// 查找
iterator find(Key)
size_type count(Key)
bool contains(Key)
```

# 基础知识

## 虚函数

- 运行时动态绑定
- 基类使用虚函数表（vtable）存储每个虚函数的地址
