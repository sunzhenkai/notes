---
title: 研习录 - 操作系统
categories: 
    - 研习录
tags:
    - 研习录
date: 2023/12/24 00:00:00
---

# 概念

- 字大小（word size）
    - 在计算中，字是特定处理器设计使用的自然数据单位，是由处理器的指令集或硬件作为一个单元处理的固定大小的数据
    - 通常是计算机处理器在一个时钟内处理二进制数据的位数，是处理器的寻址能力和数据操作单位的大小

# 内存

## 内存对齐

现代处理器的内存子系统仅限以字大小（word size）的粒度和对齐的方式访问内存，内存对齐是指数据在内存中存放时，起始位置是某个数值的倍数，这个倍数通常是计算机的字大小。

内存对齐的目的是提高计算机系统访问数据的效率，减少访问内存的次数。当访问未对齐的内存数据且数据横跨两个计算机可以读取的字时，需要访问两次内存并做额外的 shift 操作才能读取到完整的数据。

```c++
#include <iostream>
using namespace std;

#pragma pack(push)
struct A {
    char a;
    double b;
};
#pragma pack(1)
struct B {
    char a;
    double b;
};
#pragma pack(4)
struct C {
    char a;
    double b;
};
#pragma pack(8)
struct D {
    char a;
    double b;
};
#pragma pack(16)
struct E{
    char a;
    double b;
};
#pragma pack(pop)

int main() {
    cout << sizeof(char) << " " << sizeof(double) << std::endl;
    cout << sizeof(A) << " " << sizeof(B) << " " << sizeof(C) << " " << sizeof(D) << " " << sizeof(E) << endl;
    return 0;
}
```

输出如下。

```shell
1 8
16 9 12 16 16
```

