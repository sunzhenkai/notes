---
title: c++ threads
categories: 
	- [coding, c++]
tags:
	- c++
    - threads
date: 2022/03/30 00:00:00
---

# Thread

## thread

```c++
#include <thread>

std::thread trd(function, args...);
```

## 线程私有数据

```shell
# 创建线程私有数据
int pthread_key_create(pthread_key_t *key, void (*destructor)(void*)); # 第二个函数为 destructor 函数，线程结束时调用
# 设置私有数据
int pthread_setspecific(pthread_key_t key,const void *pointer));  # 第一个参数由 pthread_key_create 产生
# 获取私有数据
void *pthread_getspecific(pthread_key_t key);
# 删除
int pthread_key_delete(pthread_key_t key);
```

# Mutex

```shell
#include <mutex>
#include <shared_mutex>
```

