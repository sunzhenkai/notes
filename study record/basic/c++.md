---
title: 研习录 - C++ 基础
categories: 
    - 研习录
tags:
    - 研习录
date: 2023/12/24 00:00:00
---

# 容器

## vector

```c++
v.at(index);
v[index];
v.front();
v.back();
v.push_back();
v.emplace_back();
v.pop_back();
```

## queue

```c++
q.front();
q.back();
q.push();
q.pop();
```

## stack

```shell
s.top();
s.push();
s.pop();
```

# 关键词

## virtual

- **作用** 
    - 定义**虚函数**
    - 仅定义未实现的函数为**纯虚函数**
    - 有纯虚函数的类，叫**抽象类**，无法直接实例化
    
- **原理** 
    - 虚函数是通过在类的**虚函数表（vtable）**中存储**函数指针**来实现的
        - 编译器会为包含虚函数的类创建一个**虚函数表**和指向虚函数表的**虚函数指针（vptr）**，虚函数表是一个指向虚函数的**指针数组**
        - 每个定义虚函数的类都有自己的虚函数表，包含该类所定义的虚函数地址
        - 当派生类重写（Override）基类的虚函数时，会在其自己的虚函数表中存储该虚函数的新地址，覆盖了基类虚函数表中相应位置的函数指针
        - 每个派生类都有自己独立的虚函数表，其中存储着派生类覆盖（Override）或新增的虚函数的地址
        - 当通过指向基类的**指针或引用**调用虚函数时，会通过虚函数指针查找对应的虚函数表完成调用，这个过程是在运行时动态决定的，被称为**动态绑定**


- 注意
    - 基类不可以是虚函数，析构函数在有资源释放时必须是虚函数
        - 虚函数通过查找虚函数表调用的，而虚函数是内存中的一片区域，需要先构造对象并创建内存空间，才能完成虚函数的调用，所以构造函数不能为虚函数
        - 析构函数，在存在释放内存空间的代码时，必须设置为虚函数，负责会存在因虚构函数无法调用导致的内存泄露问题

## volatile

提醒编译器使用 volatile 声明的变量随时可能改变，在编译期间不进行指令重排优化。C++ 标准保证 volatile 变量之间不会重排，不保证 volatile 和非 volatile 变量的重排优化。

此外，还有硬件级别的指令重排，volatile 无法保证。

# 内存

## 内存模型

[C++ 内存模型](https://en.cppreference.com/w/cpp/language/memory_model)。

## 内存管理

- 代码段
- 数据段
- 堆
- 栈

[参考一](https://blog.csdn.net/qq_35018427/article/details/125975621)

# 语言

## 四种强制转换

- static_cast
  - 编译时期的静态类型检查
  - 相当于C语⾔中的强制转换
  - 不能实现普通指针数据（空指针除外）的强制转换
  - ⼀般⽤于⽗类和⼦类指针、引⽤间的相互转换
  - 没有运⾏时类型检查来保证转换的安全性
- dynamic_cast
  - 运⾏时的检查
  - 动态转换的类型和操作数必须是**完整类类型或空指针、空引⽤**
- const_cast
  - 强制去掉不能被修改的常数特性
- reinterpret_cast
  - 将指针或引⽤转换为⼀个⾜够⻓度的整型、将整型转换为指针或引⽤类型

## GLIBC 每次内存分配都会进行系统调用吗

glibc 维护一个内存池，分配内存时优先从内存池获取，分配失败再向操作系统分配内存。

**概念**

- Chunk，glibc 对内存进行分配和管理的基本单元，chunk 是 glibc 维护的一块连续内存
- Arena，一组相关的内存 Chunk 的集合，glibc 使用多个 Arena 来管理内存分配，其中至少有一个主 Arena（main arena），还可以包括线程特定的 Arena（thread arena）。每个 Arena 都有自己的 Chunk 空闲链表和其他数据结构，用于记录已分配和空闲的内存块。
- Heap，是指进程可用的虚拟地址空间中用于动态内存分配的部分，Heap 由一系列的内存区域（region）组成，每个内存区域都是通过调用 brk 或 mmap 系统调用来获取

Heap 是进程可用的虚拟地址空间中的动态内存区域，Arena 是 Heap 内部的内存池，Chunk 是 Arena 中的内存分配单元。

**获取内存的系统调用**

- brk，通过调整堆的结束地址来分配和释放内存，对于小型内存分配比较高效
- mmap，通过请求操作系统分配新的虚拟内存区域，适合大块内存的分配

**分配流程**

- 线程首先需要获取一个 Arena。查找环形链表获取未加锁的 Arena，如果都已加锁则创建 Arena（总数有限制）
- 搜索 Chunk。尝试 fastbin 等机制，查找合适的 Chunk
- 创建 Chunk。如果未找到，则会调用 brk（主 Arena） 或 mmap（非主 Arena）向操作系统申请内存，扩充 Heap
- 分割 Chunk。对获取的 Chunk 按照用户需要的大小进行内存切分，并返回起始内存指针
- 内存对齐。glibc 确保返回的内存块满足特定的对齐要求 

[参考一](https://zhuanlan.zhihu.com/p/560341532)

[参考二](https://zhuanlan.zhihu.com/p/662320270)

## 特殊函数

### 包含完整特殊函数的类

```c++
class SampleClass {
public:
    // 默认构造函数
    SampleClass() {
        std::cout << "Default constructor" << std::endl;
    }

    // 带参数的构造函数
    explicit SampleClass(int value) : data(value) {
        std::cout << "Parameterized constructor" << std::endl;
    }

    // 复制构造函数
    SampleClass(const SampleClass &other) : data(other.data) {
        std::cout << "Copy constructor" << std::endl;
    }

    // 移动构造函数
    SampleClass(SampleClass &&other) noexcept: data(std::move(other.data)) {
        std::cout << "Move constructor" << std::endl;
    }

    // 复制赋值操作符
    SampleClass &operator=(const SampleClass &other) {
        if (this != &other) {
            data = other.data;
        }
        std::cout << "Copy assignment operator" << std::endl;
        return *this;
    }

    // 移动赋值操作符
    SampleClass &operator=(SampleClass &&other) noexcept {
        if (this != &other) {
            data = std::move(other.data);
        }
        std::cout << "Move assignment operator" << std::endl;
        return *this;
    }

    // 析构函数
    ~SampleClass() {
        std::cout << "Destructor" << std::endl;
    }

private:
    int data{0};
};
```

### 初始化列表

- 不能使用初始化列表来初始化 vector 的情况
  - 当元素类型没有默认构造函数: 如果 `std::vector` 的元素类型没有默认构造函数或者是不可复制的类型
  - 当元素类型是有状态的: 如果 `std::vector` 的元素类型是具有状态的类（即具有非平凡的构造函数和析构函数）
  - 当元素类型是引用类型: `std::vector` 不能持有引用类型的元素

**示例**

```c++
void run {
    std::vector<SampleClass> scs{SampleClass(1)}; // 调用一次参数构造、一次拷贝构造
    std::cout << "> initialized <" << std::endl;
    std::vector<SampleClass> scs2;
    scs2.emplace_back(1); // 调用一次参数构造
    std::cout << "> initialized <" << std::endl;
    scs2.reserve(10); // 重新分配内存, 调用一次移动构造函数
    std::cout << "> done <" << std::endl;
}
/* Output
Parameterized constructor
Copy constructor
Destructor
> initialized <
Parameterized constructor
> initialized <
Move constructor
Destructor
> done <
Destructor
Destructor
*/
```

# STL

## 常见数据结构及底层实现

| 数据结构      | 底层实现 | 是否连续内存 | 备注                   |
| ------------- | -------- | ------------ | ---------------------- |
| vector        | 数组     | 是           |                        |
| list          | 双向链表 | 否           |                        |
| map / set     | 红黑树   | 否           | 平衡树，更新后进行平衡 |
| unordered_map | 哈希表   | 否           |                        |

# thread

```c++
#include <thread>
// 初始化 thread
auto th = std::thread(func, args...);
// thread 数组. thread 没有实现拷贝函数, vector 的部分初始化方法无法使用. 初始化列表也不能用
std::vector<std::thread> ths;
for (int i = 0; i < 5; ++i) ths.emplace_back(func, args...);

// 方法
th.join();
th.detach(); // 将线程从当前线程分离, 成为独立的后台线程, 主线程不再管理该线程
```

## detach

```c++
void payload() {
    while (true) {}
}

/**
 * terminate called without an active exception
 * Process finished with exit code 134 (interrupted by signal 6:SIGABRT)
 */
void run_thread() {
    std::thread th(payload);
}

/**
 * Process finished with exit code 0
 */
void run_thread_detach() {
    std::thread th(payload);
    th.detach();
}
```

## 注意 

- 当进程退出时，操作系统会停掉所有由该进程创建的线程（detach 后也会被 kill）

# 信号量

- [condition_variable](https://en.cppreference.com/w/cpp/thread/condition_variable)

## mutex & shared_mutex

```shell
#include "mutex"
#include "shared_mutex"
#include "iostream"

void test_shared_mutex() {
    std::shared_mutex shared_mtx;
    {
        std::shared_lock lock(shared_mtx);
    }
    {
        std::unique_lock lock(shared_mtx);
    }
}

void test_mutex() {
    std::mutex mtx;
    std::lock_guard lock(mtx);
}
```

## unique_lock & lock_guard

`std::lock_guard` 是一个轻量级的互斥锁封装，它提供了一种方便的方式来管理互斥锁的锁定和释放。`std::unique_lock` 是一个更加灵活和功能强大的互斥锁封装，提供了与 `std::lock_guard` 类似的锁定和释放互斥锁的功能，但还可以进行更多的操作。`std::unique_lock` 允许在构造函数中选择锁定模式，包括延迟锁定、递归锁定和尝试锁定等。

**Tips**

- 为什么 condition_variable 的 wait 方法使用 unique_lock 
  - lock_guard、scoped_lock 无法获取 mutex，unique_lock 可以

## condition_variable

```c++
// wait
cv.wait(std::unique_lock<std::mutex>) // 等待信号量
cv.wait(std::unique_lock<std::mutex>, Predicate) // 等待信号量, 并且 Predicate 返回 true
// wait_for
cv.wait_for(std::unique_lock<std::mutex>, const duration&) // 等待信号量
cv.wait_for(std::unique_lock<std::mutex>, const duration&, Predicate) // 等待信号量
// wait_until
cv.wait_until(std::unique_lock<std::mutex>, const time_point&)
cv.wait_until(std::unique_lock<std::mutex>, const time_point&, Predicate) 
// notify
cv.notify_one()
cv.notify_all()
```

**说明**

- Predicate > mutex，即便获取信号量，不满足 Predicate，仍不退出 wait
- duration/time_point > Predicate，即时不满足 Predicate，到达指定时间限制，仍会退出 wait

**示例**

```c++
using namespace std::literals;
std::mutex mtx;
std::condition_variable cv;
void run_wait() { // 等待 notify 后线程结束
    std::unique_lock lock(mtx);
    cv.wait(lock);
    std::cout << __FUNCTION__ << " done" << std::endl;
}
void run_wait_predicate() { // 等待 notify 后, 由于不满足 Predicate, 继续 wait, 线程无法退出
    std::unique_lock lock(mtx);
    cv.wait(lock, []() { return false; });
    std::cout << __FUNCTION__ << " done" << std::endl;
}
void run_wait_for() { // 一秒后超时, 未等待到 notify 及不满足 Predicate, 线程仍退出
    std::unique_lock lock(mtx);
    cv.wait_for(lock, 1s, []() { return false; });
    std::cout << __FUNCTION__ << " done" << std::endl;
}

void test_run() {
    std::vector<std::thread> ths;
    ths.emplace_back(run_wait);
    ths.emplace_back(run_wait_predicate);
    ths.emplace_back(run_wait_for);

    std::this_thread::sleep_for(2s);
    {
        std::lock_guard lock(mtx);
        cv.notify_all();
    }

    for (auto &th: ths) th.join();
}

/* RUN test_run
run_wait_for done
run_wait done
*/
```

# 并发控制

- 互斥锁
- 读写锁
- atomic
- thread local

## 有哪些锁机制

| 锁                           | 说明                 | 备注                         |
| ---------------------------- | -------------------- | ---------------------------- |
| std::mutex                   | 互斥锁               |                              |
| std::shared_mutex            | 读写锁（共享互斥锁） |                              |
| std::recursive_mutex         | 可重入锁（递归锁）   | 需要程序确保每次上锁都会释放 |
| std::timed_mutex             | 计时互斥锁           |                              |
| `std::recursive_timed_mutex` | 计时递归锁           | 需要程序确保每次上锁都会释放 |

## 如何实现自旋锁

可以通过原子操作和循环来实现自旋锁。

```shell
#include <atomic>
class SpinLock {
    std::atomic_flag flag;
public:
    SpinLock() : flag(ATOMIC_FLAG_INIT) {}
    void lock() {
        while (flag.test_and_set(std::memory_order_acquire)) {
            // 自旋等待直到获取到锁
        }
    }
    void unlock() {
        flag.clear(std::memory_order_release);
    }
};
```

## atomic

[atomic](https://en.cppreference.com/w/cpp/atomic/atomic)

