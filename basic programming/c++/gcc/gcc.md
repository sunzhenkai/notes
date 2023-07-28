---
title: gcc
categories: 
	- [coding, c++, gcc]
tags:
	- gcc
date: 2022/03/10 00:00:00
---

# Install

```shell
# 下载 
从这里 https://mirrors.aliyun.com/gnu/gcc/ 选一个版本，或使用其他源。

# 解压
tar xzf gcc-<version>.tar.gz
cd gcc-<version>

# 下载依赖
./contrib/download_prerequisites 

# 配置
./configure --prefix=/path/to/install/dir --enable-languages=c,c++ --disable-multilib

# 编译
make -j <thread-number>
make install

# 如果不想污染源文件
mkdir gcc-build
cd gcc-build
$PWD/../gcc-<version>/configure --prefix=/path/to/install/dir --enable-languages=c,c++ --disable-multilib
```

# 编译

```shell
gcc sample.cpp # 默认生成 a.out

# 指定输出文件
gcc -o sample.exe sample.cpp

# 指定 c++ std 版本
gcc -std=c++17 -o sample.exe sample.cpp
```

## 参数

```shell
-c	仅编译
-Dname=value	定义 name 值
-o file-name	输出
```

## Flags

```shell
# warning
-Wall			开启警告（all: 应该开启的最小警告集合）
-Wextra		开启扩展警告
-Werror 	所有警告视为错误
-Wno-error=...	关闭某项警告视为错误
-Wno-<...>			关闭某项警告视为错误
-Werror   所有警告视为错误
-Wextra

# 常用警告
-Werror=return-type    函数没有 return 视为错误
```

**示例**

```shell
export CFLAGS='-g -O3'
export CXXFLAGS='-ggdb3 -O0 -Wno-narrowing'
export CPPFLAGS='-DX=1 -DY=2 -Wno-narrowing'
export CCFLAGS='--asdf -Wno-narrowing'

make CXXFLAGS='-ggdb3 -O0 -Wno-narrowing' CPPFLAGS='-DX=1 -DY=2 -Wno-narrowing' CCFLAGS='--asdf -Wno-narrowing' all -j
```

# 编译库

```c++
// common.h

```

- [link 1](https://stackoverflow.com/questions/6562403/i-dont-understand-wl-rpath-wl)
- [link 2](https://stackoverflow.com/questions/54786262/c-what-would-happen-if-two-library-uses-same-source-code-for-build)

# 查看查找链接库路径

```shell
gcc -Xlinker -v
g++ -Xlinker -v
```

# 链接

- libraries 允许未定义的符号（undefined symbols）
- executable 不允许有未定义的符号
- 在代码中定义的符号（如函数名）还未使用到之前，链接器并不会把它加入到连接表中
