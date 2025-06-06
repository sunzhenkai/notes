---
title: seastar usage
categories: 
  - [架构,java,框架,seastar]
tags:
  - seastar
date: "2021-12-15T00:00:00+08:00"
update: "2021-12-15T00:00:00+08:00"
---

# 启动

```shell
seastar::app_template app;
char *av[5] = {"--overprovisioned", "-c", "4", "--blocked-reactor-notify-ms", "25"};
app.run(sizeof av / sizeof *av, av, [] {
    return seastar::make_ready_future<>();
});
```

# `std::move`

```c++
seastar::future<int> slow_do_something(std::unique_ptr<T> obj) {
    using namespace std::chrono_literals;
    return seastar::sleep(10ms).then([obj = std::move(obj)] () mutable {
        return do_something(std::move(obj));
    });
}
```

- `mutable ` :  

  - > The `[obj = ...]` capture syntax we used here is new to C++14. This is the main reason why Seastar requires C++14, and does not support older C++11 compilers.
    >
    > The extra `() mutable` syntax was needed here because by default when C++ captures a value (in this case, the value of std::move(obj)) into a lambda, it makes this value read-only, so our lambda cannot, in this example, move it again. Adding `mutable` removes this artificial restriction.

## 异常和fail

```c++
#include "core/future.hh"
#include <iostream>
#include <exception>

class my_exception : public std::exception {
    virtual const char* what() const noexcept override { return "my exception"; }
};

seastar::future<> fail() {
    return seastar::make_exception_future<>(my_exception());
}

seastar::future<> f() {
    return fail().finally([] {
        std::cout << "cleaning up\n";
    });
}
```

抛出异常会导致整个 `f()` 执行失败，不建议抛出异常，应该返回fail future：

```c++
void inner() {
    throw my_exception();
}
seastar::future<> fail() {
    try {
        inner();
    } catch(...) {
        return seastar::make_exception_future(std::current_exception());
    }
    return seastar::make_ready_future<>();
}
```

或者使用`futurize_apply`：

```c++
seastar::future<> fail() {
    throw my_exception();
}
seastar::future<> f() {
    return seastar::futurize_apply(fail).finally([] {
        std::cout << "cleaning up\n";
    });
}
```

# 文档

- [tutorial](https://github.com/scylladb/seastar/blob/master/doc/tutorial.md)  OR [tutorial](http://docs.seastar.io/master/tutorial.html#disk-io-scheduler)
- [CLion 远程同步及远程调试](https://www.cnblogs.com/qiumingcheng/p/11185073.html)
