---
title: CUDA
categories: 
    - 研习录
tags:
    - 研习录
date: 2023/12/18 00:00:00
---

# 硬件

## CPU & GPU

![img](./cuda/image3-2.png)

## 内存

内存分级。

![img](cuda/memory-hierarchy-in-gpus-2.png)

# 核函数

## 定义

```c++
__global__ void function_name(...) {
  ...
}
```

- `__global__` 限定词
- 返回值必须是 `void`

## 特性

- 核函数在 GPU 上并行执行
- 核函数只能访问 GPU 内存
- 核函数不能使用变长参数
- 核函数不能使用静态变量
- 核函数不能使用函数指针
- 核函数具有**异步性**
  - 使用 `cudaDeviceSynchronize()` 来做同步
- 核函数不支持 iostream，打印需要使用 printf

## 核函数和线程等级

![img](cuda/kernel-as-function.png)

核（Kernel）是执行在 GPU 上的函数。应用程序的并行部分由K个不同的CUDA线程并行执行K次，而不是像常规的C/C++函数那样只执行一次。

每个CUDA内核都有一个`__global__`声明说明符。程序员通过使用内置变量为每个线程提供一个唯一的全局ID。

![Figure 2. CUDA kernels are subdivided into blocks.](cuda/gpus-in-blocks-625x203.png)

一组线程称为CUDA块（CUDA Block）。CUDA块被分组到一个网格（Grid）中。内核（Kernel）作为线程块网格（A Grid of Blocks of Threads）执行。

每个 CUDA 块被一个流式多处理器（Streaming Multiprocessor，SM）执行，不能被迁移到其他 SMs 处理（抢占、调试、CUDA动态并行期除外）。一个SM可以运行多个并发CUDA块，具体取决于CUDA块所需的资源。每个内核在一个设备上执行，CUDA支持一次在一个设备上运行多个内核。

![img](cuda/kernel-execution-on-gpu-1-625x438.png)

上图展示了内核执行和GPU中可用硬件资源的映射。

**限制。**

- CUDA架构限制每个块的线程数（每个块限制1024个线程）
- 线程块的维度可以通过内置的block Dim变量在内核中访问
- 块中的所有线程都可以使用内部函数`__syncthreads` 进行同步。使用 `__syncthreads` 块中的所有线程都必须等待
- `<<<…>>>` 语法中指定的每个块的线程数和每个网格的块数可以是int或dim3类型。这些三尖括号标记从主机代码到设备代码的调用。它也称为 Kernel Launch

**示例。**

```c++
// Kernel - Adding two matrices MatA and MatB
__global__ void MatAdd(float MatA[N][N], float MatB[N][N], float MatC[N][N])
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    int j = blockIdx.y * blockDim.y + threadIdx.y;
    if (i < N && j < N)
        MatC[i][j] = MatA[i][j] + MatB[i][j];
}
 
int main()
{
    ...
    // Matrix addition kernel launch from host code
    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks((N + threadsPerBlock.x -1) / threadsPerBlock.x, (N+threadsPerBlock.y -1) / threadsPerBlock.y);
    MatAdd<<<numBlocks, threadsPerBlock>>>(MatA, MatB, MatC);
    ...
}
```

CUDA为线程和块定义了内置的3D变量。线程使用内置的3D变量threadIdx进行索引。三维索引提供了一种自然的方式来索引向量、矩阵和体积中的元素，并使CUDA编程更容易。类似地，块也使用称为block Idx的内置3D变量进行索引。示例的 CUDA 程序用于两个矩阵相加，显示了多维 blockIdx 和 threadIdx 以及其他变量（如 blockDim）。选择 2D 块是为了便于索引，每个块有 256 个线程，其中 x 和 y 方向各有 16 个线程。使用数据大小除以每个块的大小来计算块的总数。

## 调用

核函数调用需要指定线程模型。

```c++
kernel_function<<<grid, block>>>();
```

# 线程模型

## 重要概念

- grid，网格
- block，线程块

# 参考

- [CUDA Refresher: The CUDA Programming Model](https://developer.nvidia.com/blog/cuda-refresher-cuda-programming-model/)

- [CUDA Refresher: Reviewing the Origins of GPU Computing](https://developer.nvidia.com/blog/cuda-refresher-reviewing-the-origins-of-gpu-computing/)