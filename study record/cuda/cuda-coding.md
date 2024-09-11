---
title: CUDA - Coding
categories: 
    - 研习录
tags:
    - 研习录
date: 2024/08/15 00:00:00
---

# 错误处理

## 运行时 API 错误码

调用 CUDA 运行时 API 时，接口返回错误码。

```c++
__host__ __device__ cudaError_t cudaGetDeviceCount ( int* count ); // 获取设备数量, 返回错误码
```

## 错误检查

```c++
__host__ __device__ const char* cudaGetErrorName ( cudaError_t error );     // 获取错误码的枚举名称
__host__ __device__ const char*	cudaGetErrorString ( cudaError_t error );   // 获取错误码的解释描述
```

**定义错误检查函数**

```c++
__host__ void error_check_entry() {
  int device_id_in_use;
  error_check(cudaGetDevice(&device_id_in_use), __FILE__, __LINE__);
  error_check(cudaSetDevice(999), __FILE__, __LINE__);
  //  char *p_c;
  //  error_check(cudaMalloc(&p_c, 100), __FILE__, __LINE__);

  cudaDeviceSynchronize();
} /** output
error_check, ok
CUDA error:
        code=101, name=cudaErrorInvalidDevice, description=invalid device ordinal,
        file=/data/code/cook-cuda/src/sample/hello_world.cu, line=51
*/
```

## 核函数中的异常

核函数的返回值必须是 void。

```c++
__host__ __device__ cudaError_t cudaGetLastError ( void ); // 返回最后一次错误码
```

```c++
__global__ void kernel_error_entry() {
  dim3 block(2048);
  print_build_in_vars<<<2, block>>>();  // block size 最大 1024
  error_check(cudaGetLastError(), __FILE__, __LINE__);
} /** output
CUDA error:
        code=9, name=cudaErrorInvalidConfiguration, description=invalid configuration argument,
        file=/data/code/cook-cuda/src/sample/hello_world.cu, line=67
*/
```

# 性能评估

## 事件计时

```c++
__host__ cudaError_t cudaEventCreate ( cudaEvent_t* event );
__host__ __device__ cudaError_t 	cudaEventRecord ( cudaEvent_t event, cudaStream_t stream = 0 );
__host__ cudaError_t cudaEventSynchronize ( cudaEvent_t event );
__host__ cudaError_t cudaEventElapsedTime ( float* ms, cudaEvent_t start, cudaEvent_t end );
__host__ __device__ cudaError_t 	cudaEventDestroy ( cudaEvent_t event );
```

示例。

```c++
cudaEvent_t start, end;
error_check(cudaEventCreate(&start), __FILE__, __LINE__);
error_check(cudaEventCreate(&end), __FILE__, __LINE__);
error_check(cudaEventRecord(start), __FILE__, __LINE__);
cudaEventQuery(start);

// run GPU Task

error_check(cudaEventRecord(end), __FILE__, __LINE__);
error_check(cudaEventSynchronize(end), __FILE__, __LINE__);
float elapsed_time_ms;
ERROR_CHECK(cudaEventElapsedTime(&elapsed_time_ms, start, end));

printf("elapsed time: %f ms\n", elapsed_time_ms);
ERROR_CHECK(cudaEventDestroy(start));
ERROR_CHECK(cudaEventDestroy(end));
```

error_check。

```c++
__host__ __device__ cudaError_t error_check(cudaError_t err, const char *fn, int line) {
  if (err != cudaSuccess) {
    printf("CUDA error:\n\tcode=%d, name=%s, description=%s, \n\tfile=%s, line=%d\n", err, cudaGetErrorName(err),
           cudaGetErrorString(err), fn, line);
  }
  return err;
}
#define ERROR_CHECK(exp) error_check(exp, __FILE__, __LINE__)
```

## nvprof

nvprof 是评估 cuda 程序性能的工具。不过目前已经是过时的工具，不适用 compute capability >= 8.0 的设备。新设备适用 nsys 替代。 

```shell
$ nvprof {cuda-program}
```

## nsys

```shell
$ nsys profile {cuda-program} # 运行并记录程序的 profile 到 nsys-rep 文件
$ nsys analyze {nsys-rep}     # 分析 profile 文件
```

# 获取 GPU 信息

**运行时 API**

```c++
__host__ cudaError_t cudaGetDeviceProperties ( cudaDeviceProp* prop, int  device )
```

```c++
__host__ void PrintDeviceInfo() {
  int deviceCount;
  cudaGetDeviceCount(&deviceCount);
  std::cout << "GPU device count: " << deviceCount << std::endl;

  for (int i = 0; i < deviceCount; ++i) {
    // sm: 流式多处理器, Streaming Multiprocessor
    cudaDeviceProp dp{};
    cudaGetDeviceProperties(&dp, i);
    std::cout << "device.0  " << std::endl;
    std::cout << "  sm count: \t\t\t\t" << dp.multiProcessorCount << std::endl;
    std::cout << "  shared memory per block: \t\t" << dp.sharedMemPerBlock / 1024 << "KB" << std::endl;
    std::cout << "  max threads per block:\t\t" << dp.maxThreadsPerBlock << std::endl;
    std::cout << "  max threads per multi processor:\t" << dp.maxThreadsPerMultiProcessor << std::endl;
    std::cout << "  max threads per sm:\t\t\t" << dp.maxThreadsPerMultiProcessor / 32 << std::endl;
    std::cout << "  max blocks per multi processor:\t" << dp.maxBlocksPerMultiProcessor << std::endl;
  }
}
```

