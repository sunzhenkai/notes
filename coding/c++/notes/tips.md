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

## 对象成员函数作为参数

参考[这里](https://www.codeguru.com/cplusplus/c-tutorial-pointer-to-member-function/)。

# 字符串

## 分隔字符串

```c++
std::string server_address = "127.0.0.1:80";
std::vector<std::string> result;
boost::split(result, server_address, boost::is_any_of(":"));

result.at(0); // 127.0.0.1
result.at(1); // 80
```

## join 字符串

```c++
// 使用 fmt
#include <fmt/format.h>
// fmt::join(elems, delim)
auto s = fmt::format("{}",fmt::join(elems, delim)); 
```

# 类型转换

```c++
// string -> int
stoi("80")
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

# time

```c++
std::chrono::system_clock  // 系统时间
std::chrono::steady_clock  // 单调时间，并不能获取系统时间，多用来计算时间差
```
## 获取时间
```c++
#include <ctime>
#include <chrono>


long current_milliseconds() {
    auto now = std::chrono::system_clock::now();
    return std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
}

// 并不能获取系统时间
long current_milliseconds_v2() {
    auto now = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
}

long current_milliseconds_v3() {
    struct timeval now{};
    gettimeofday(&now, nullptr);
    return now.tv_sec * 1000 + now.tv_usec / 1000;
}

// 用 time 获取时间由性能问题
long current_seconds() {
    time_t t;
    time(&t);
    return (long) t;
}

long duration_milliseconds(std::chrono::time_point<std::chrono::system_clock,
        std::chrono::milliseconds> start) {
    auto now = std::chrono::system_clock::now();
    return std::chrono::duration_cast<std::chrono::milliseconds>(now - start).count();
}
```

> `time(..)` 获取时间性能有问题
>
> `gettimeofday(...)` 和 `std::chrono::system_clock::now()` 相近

## 格式化时间

```c++
#include <iomanip>  // std::put_time
#include <sstream>
#include <ctime>
#include <chrono>

std::string now_format(const std::string &f = "%F %T") {
    auto now = std::chrono::system_clock::now();
    auto now_t = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&now_t), f.c_str());
    return ss.str();
}

std::string now_format_v2(const std::string &f = "%F %T") {
    time_t now;
    time(&now);
    char s[30];
    struct tm *time_info = localtime(&now);
    strftime(s, 30, f.c_str(), time_info);
    return {s};
}

std::string now_format_v3(const std::string &f = "%F %T") {
    std::time_t t = std::time(nullptr);
    char buf[100];
    std::strftime(buf, sizeof(buf), "%F %T", std::localtime(&t));
    return {buf};
}

std::string now_format_v4(const std::string &f = "%F %T") {
    std::time_t t = std::time(nullptr);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&t), f.c_str());
    return ss.str();
}
```

## 计算时间差

```c++
template <
    class result_t   = std::chrono::milliseconds,
    class clock_t    = std::chrono::steady_clock,
    class duration_t = std::chrono::milliseconds
>
auto since(std::chrono::time_point<clock_t, duration_t> const& start)
{
    return std::chrono::duration_cast<result_t>(clock_t::now() - start);
}
```

## Timer

```c++
template <class DT = std::chrono::milliseconds,
          class ClockT = std::chrono::steady_clock>
class Timer
{
    using timep_t = typename ClockT::time_point;
    timep_t _start = ClockT::now(), _end = {};

public:
    void tick() { 
        _end = timep_t{}; 
        _start = ClockT::now(); 
    }
    
    void tock() { _end = ClockT::now(); }
    
    template <class T = DT> 
    auto duration() const { 
        gsl_Expects(_end != timep_t{} && "toc before reporting"); 
        return std::chrono::duration_cast<T>(_end - _start); 
    }
};
```

> [参考这里](https://stackoverflow.com/questions/2808398/easily-measure-elapsed-time)

**使用**

```c++
Timer clock; // Timer<milliseconds, steady_clock>

clock.tick();
/* code you want to measure */
clock.tock();

cout << "Run time = " << clock.duration().count() << " ms\n";
```

# thread & mutex

## thread

```c++
std::thread t(func, params...);
t.join();
```

## sleep

```c++
#include "thread"
std::this_thread::sleep_for(std::chrono::milliseconds(1000));

#include <unistd.h>
usleep(microseconds);
```

## mutex

### mutex

```c++
#include <mutex>

std::mutex mtx;
mtx.lock();
mtx.unlock();

std::lock_guard g(mtx);
```

> std::lock_guard 和 mtx.lock()、mtx.unlock() 作用等同，初始化时上锁，析构时解锁

### shared_mutex

```shell
#include <shared_mutex>

std::shared_mutex mtx;

## 独享锁
mtx.lock();
mtx.try_lock();
mtx.unlock();
# 或者
std::unique_lock lock(mtx);

## 共享锁
mtx.lock_shared();
mtx.try_lock_shared();
mtx.unlock_shared();
# 或者
std::shared_lock lock(mtx);
```

## condition

`condition` 通常和 `mutex` 一起使用。

```c++
#include <condition_variable>
std::condition_variable cv;

cv.wait(lock);
cv.notify_one();
```

下面是一个阻塞队列的示例。

```c++
namespace ctd {
    template<typename T>
    class BlockingQueue {
        int count;
        std::mutex mutex;
        std::condition_variable cv;
        std::deque<T> data;
    public:
        void Push(T const &value) {
            {
                std::unique_lock lock(mutex);
                data.push_front(value);
            }
            cv.notify_one();
        }

        T Pop() {
            std::unique_lock lock(mutex);
            cv.wait(lock, [=] { return !this->data.empty(); });
            T r(std::move(this->data.back()));
            this->data.pop_back();
            return r;
        }
    };
}
```

# 特殊函数

```c++
// 默认构造函数
classname ()
// 非默认函数
explicit classname(type param)
// 拷贝构造函数
classname(const classname &other)
// 赋值构造
classname& operator=(const classname &other)
// move 构造
classname(classname &&other)
// 赋值 move 构造
classname& operator=(classname &&other)

// 析构函数
~classname()
```

|         Function         |            syntax for class MyClass             |
| :----------------------: | :---------------------------------------------: |
|   Default constructor    |                  `MyClass();`                   |
|     Copy constructor     |        `MyClass(const MyClass& other);`         |
|     Move constructor     |      `MyClass(MyClass&& other) noexcept;`       |
| Copy assignment operator |   `MyClass& operator=(const MyClass& other);`   |
| Move assignment operator | `MyClass& operator=(MyClass&& other) noexcept;` |
|        Destructor        |                  `~MyClass();`                  |

# string_view

```c++
#include <string_view>
using namespace std::literals;

std::string_view v = "hello"sv;
```

# 类定义

## 静态变量

```c++
// a.h
class A {
  public:
  	static int v;
}

// a.cpp
int A::v;
```

# thread_local

## 静态成员变量定义

```c++
// a.h
class A {
  public:
  	static thread_local int v;
}

// a.cpp
thread_local int A::v;
```

# 全局成员定义

## 函数

### 仅在 header file

```c++
// global.h
namespace global {
  // static functions
  static void f() {
    // do something
  }
}
```

### header / source 分开定义

```c++
// global.h
namespace global {
  static void f();
}

// global.cpp
namespace global {
  void f() {
    // do something
  }
}
```

