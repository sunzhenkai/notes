---
title: c++ 复杂对象
categories: 
  - [coding, c++]
tags:
  - c++
date: 2022/05/18 00:00:00
---

# 说明

这是一个小实验。

# 定义一个复杂类

```shell
struct Complex {
    int64_t a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z,
            a1, b1, c1, d1, e1, f1, g1, h1, i1, j1, k1, l1, m1, n1, o1, p1, q1, r1, s1, t1, u1, v1, w1, x1, y1, z1,
            a2, b2, c2, d2, e2, f2, g2, h2, i2, j2, k2, l2, m2, n2, o2, p2, q2, r2, s2, t2, u2, v2, w2, x2, y2, z2,
            a3, b3, c3, d3, e3, f3, g3, h3, i3, j3, k3, l3, m3, n3, o3, p3, q3, r3, s3, t3, u3, v3, w3, x3, y3, z3;
};
```

# 性能对比

作为实验，我们把负载类的对象插入一个 Map。在开始性能对比之前，定义计算时间的工具函数。

```c++
std::chrono::time_point<std::chrono::system_clock> now() {
    return std::chrono::system_clock::now();
}

long elapsed(std::chrono::time_point<std::chrono::system_clock> &start) {
    auto e = std::chrono::system_clock::now() - start;
    return std::chrono::duration_cast<std::chrono::milliseconds>(e).count();
}
```

## std::map

```shell
template<typename K, typename V>
using Map = std::map<K, V>;

int main() {
    typedef Complex MapV;
    int loop = 500 * 10000;
    MapV complex;
    Map<int, MapV> m;
    auto start = now();
    for (int i = 0; i < loop; ++i) {
        m[i] = complex;
    }
    std::cout << "elapsed: " << elapsed(start) << std::endl;
    return 0;
}
```

输出

```shell
elapsed: 7750
```

## std::unordered_map

```c++
template<typename K, typename V>
using Map = std::unordered_map<K, V>;

int main() {
    typedef Complex MapV;
    int loop = 500 * 10000;
    MapV complex;
    Map<int, MapV> m;
    auto start = now();
    for (int i = 0; i < loop; ++i) {
        m[i] = complex;
    }
    std::cout << "elapsed: " << elapsed(start) << std::endl;
    return 0;
}
```

输出

```shell
elapsed: 4474
```

## std::shared_ptr

如果我们改为使用共享指针。

```shell
template<typename K, typename V>
using Map = std::unordered_map<K, V>;

int main() {
    typedef std::shared_ptr<Complex> MapV;
    int loop = 1000 * 10000;
    MapV complex = std::make_shared<Complex>();
    Map<int, MapV> m;
    auto start = now();
    for (int i = 0; i < loop; ++i) {
        m[i] = complex;
    }
    std::cout << "elapsed: " << elapsed(start) << std::endl;
    return 0;
}
```

输出

```shell
elapsed: 2002
```

## 简单对象

再来对比下指针和简单对象。

### 智能指针

```c++
template<typename K, typename V>
using Map = std::unordered_map<K, V>;

int main() {
    typedef int64_t BaseType;
    typedef std::shared_ptr<BaseType> MapV;
    int loop = 500 * 10000;
    MapV complex = std::make_shared<BaseType>();
    Map<int, MapV> m;
    auto start = now();
    for (int i = 0; i < loop; ++i) {
        m[i] = complex;
    }
    std::cout << "elapsed: " << elapsed(start) << std::endl;
    return 0;
}
```

输出

```shell
elapsed: 2012
```

### 简单对象

```shell
template<typename K, typename V>
using Map = std::unordered_map<K, V>;

int main() {
    typedef int64_t BaseType;
    typedef BaseType MapV;
    int loop = 500 * 10000;
    MapV complex{};
    Map<int, MapV> m;
    auto start = now();
    for (int i = 0; i < loop; ++i) {
        m[i] = complex;
    }
    std::cout << "elapsed: " << elapsed(start) << std::endl;
    return 0;
}
```

输出

```shell
elapsed: 1763
```

# std::move

std::move 实际会调用 move constructor（A(A &&another)），所以，对于基础类型和没有实现 move constructor 的类不起效果。

定义 A。

```c++
class A {
public:
    A() {
        std::cout << "construct A" << std::endl;
    }

    A(const A& a) {
        std::cout << "copy construct A" << std::endl;
    }

    ~A() {
        std::cout << "destruct A" << std::endl;
    }
};
```

看下插入 map。

```c++
std::map<int, A> ma;
{
	A a;
	ma.emplace(1, std::move(a));
}

// 输出
construct A
copy construct A
destruct A
destruct A
```

用如下方式。

```c++
std::map<int, A> ma;
{
  ma[1];
}

// 输出
construct A
destruct A
```

实现移动构造。

```c++
class A {
public:
    A() {
        std::cout << "construct A" << std::endl;
    }

    A(const A& a) {
        std::cout << "copy construct A" << std::endl;
    }

    A(A &&a) {
        std::cout << "move construct A" << std::endl;
    }

    ~A() {
        std::cout << "destruct A" << std::endl;
    }
};
```



# 申请内存

先来看下空转。

```c++
int loop = 1000 * 10000;
auto start = now();
for (int i = 0; i < loop; ++i) {
}
std::cout << "elapsed: " << elapsed(start) << std::endl;

// output
elapsed: 24
```

再来看下申请内存。

```c++
int loop = 1000 * 10000;
auto start = now();
for (int i = 0; i < loop; ++i) {
    Complex complex{};
}
std::cout << "elapsed: " << elapsed(start) << std::endl;

// output
elapsed: 144
```

再来看下插入 vector。

```c++
int loop = 1000 * 10000;
std::vector<Complex> complexes;
auto start = now();
for (int i = 0; i < loop; ++i) {
    Complex complex{};
    complexes.emplace_back(complex);
}
std::cout << "elapsed: " << elapsed(start) << std::endl;

// output
elapsed: 9663
```

再看下 reserve size。

```c++
int loop = 1000 * 10000;
std::vector<Complex> complexes;
complexes.reserve(loop);
auto start = now();
for (int i = 0; i < loop; ++i) {
    Complex complex{};
    complexes.emplace_back(complex);
}
std::cout << "elapsed: " << elapsed(start) << std::endl;

// output
elapsed: 2525
```

再看下通过构造函数初始化列表。

```c++
int loop = 1000 * 10000;
auto start = now();
std::vector<Complex> complexes(loop, Complex{});
std::cout << "elapsed: " << elapsed(start) << std::endl;

// output
elapsed: 2069
```

再来看下 resize。

```c++
int loop = 1000 * 10000;
std::vector<Complex> complexes;
auto start = now();
complexes.resize(loop);
std::cout << "elapsed: " << elapsed(start) << std::endl;

// output
elapsed: 1996
```

# 小结

在深度理解程序的过程中，很多操作的实际成本和我们想象中的不太一样，用一句话直白的说明就是，"这个操作竟然这么耗时？"，或者，"这个操作这么快？"。

## 操作

- 计算
- 内存申请
- 容器
  - map，插入、查找