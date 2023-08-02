---
title: c++ - segmentation fault
categories: 
  - [coding, c++]
tags:
  - c++
date: 2022/1/13 00:00:00
update: 2022/1/13 00:00:00
---

# 原因

- 访问空指针
- 访问不可访问的内存
  - 访问不可访问的变量 / 已经不在可访问作用域的变量，即便 gdb 调试可以展示变量值

# 案例

```bash
# 1. 访问已经回收的临时变量
使用 seastar 时，调用返回 future 方法的方法，参数包含局部变量。在执行 then 回调时，局部变量已经不可访问（使用 gdb 调试仍可展示数值）。
解决方法是使用 seastar::do_with(std::move(v), [](V &v) { ... })

# 2. 未加 return 值导致 std::function 析构
定义的方法返回值类型不为 void，但是没有 return 语句，定义 std::function 对象，在析构时报 segmentation fault
```

# Lambda

## shared_ptr

### shared_ptr 引用导致的内存非法访问

```c++
class A {
public:
    int a;
};

std::function<void()> fun() {
    std::shared_ptr<A> sa = std::make_shared<A>();
    sa->a = 2;
    auto f = [&] {
        std::cout << "sa-> " << sa->a << std::endl;
        sa->a = 1;
    };
    return f;
}

void test() {
    std::cout << "----- in test -----" << std::endl;
    fun()();
    std::cout << "----- out test -----" << std::endl;
}
```

**调用**

```c++
int main() {
    test();
    return 0;
}
```

**输出**

```shell
----- in test -----
sa-> 281314120

Process finished with exit code 138 (interrupted by signal 10: SIGBUS)
```

**原因**

lambda 表达式使用引用访问局部变量，在 `fun()` 返回 lambda 表达式对象时，局部变量 `sa` 已被释放，在 `test` 中执行 lambda 表达式时会访问已被释放的内存。

**解决**

使用拷贝替换引用，增加引用计数。

```c++
std::function<void()> fun() {
    std::shared_ptr<A> sa = std::make_shared<A>();
    sa->a = 2;
    auto f = [&, sa] {
        std::cout << "sa-> " << sa->a << std::endl;
        sa->a = 1;
    };
    return f;
}
```

**输出**

```shell
----- in test -----
sa-> 2
----- out test -----

Process finished with exit code 0
```

