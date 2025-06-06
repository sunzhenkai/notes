---
title: 研习录 - 操作系统
categories: 
    - 研习录
tags:
    - 研习录
date: "2023-12-24T00:00:00+08:00"
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

## 内存屏障

**写屏障（Store Barrier）**、**读屏障（Load Barrier）**和**全屏障（Full Barrier）**。

- **防止指令之间的重排序**
- **保证数据的可见性**

[参考一](https://www.0xffffff.org/2017/02/21/40-atomic-variable-mutex-and-memory-barrier/)

[参考二](https://gaomf.cn/2020/09/11/Cpp_Volatile_Atomic_Memory_barrier/)

# 进程、线程、协程

## 操作系统由用户态切换至内核态的过程

- 触发事件
    - 系统调用（new/delete、wait/sleep、创建线程等）、异常（InterruptedException）、外围设备中断
    - 处理器将系统调用号和参数放到寄存器，触发执行**中断**指令（现代操作系统每个线程对应一个内核调度实体，不会阻塞整个应用程序）
- 异常/中断处理
    - CPU 暂停处理线程的正常处理，转而执行预定义的**异常或中断处理程序**
- 保存上下文
    - 把寄存器状态和指令指针保存到内存
- 切换到内核态
    - 在异常/中断处理程序中，处理器会将当前执行模式从用户态切换为内核态（修改处理器的特殊寄存器或标志位，使其处于内核特权级别）
- 执行内核代码
    - 从寄存器取出系统调用号及参数，执行操作系统函数
- 恢复上下文
    - 将应用程序的上下文从保存的位置恢复回处理器寄存器中
- 切换到用户态
    - 处理器将执行模式从内核态切换回用户态，并从中断/异常处理程序返回到应用程序的正常执行位置

# 并发控制

- 信号量
- 锁（读写锁、互斥锁、自旋锁）
    - 自旋锁，盲等锁的机制，不放弃 CPU 使用权
    - 可重入锁，同一进程可对同一资源重复上锁
    - 乐观锁，假定每次读取写入的过程中不会有其他线程修改资源，每次读时不上锁，在写时判断是否被更改
    - 悲观锁，假定每次读取后，在写入时资源都会被其他线程修改，每次读时都上锁

