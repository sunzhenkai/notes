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
## 从这里 https://mirrors.aliyun.com/gnu/gcc/ 选一个版本，或使用其他源。
VERSION=7.3.0
wget https://mirrors.aliyun.com/gnu/gcc/gcc-${VERSION}/gcc-${VERSION}.tar.gz
# 解压
tar xzf gcc-${VERSION}.tar.gz
cd gcc-${VERSION}

# 下载依赖
./contrib/download_prerequisites 

# 配置
./configure --prefix=/opt/gcc/${VERSION} --enable-languages=c,c++ --disable-multilib
# 编译
make -j$(nproc)
make install

# 如果不想污染源文件
mkdir gcc-build
cd gcc-build
../configure --prefix=/opt/gcc/${VERSION} --enable-languages=c,c++ --disable-multilib
## 另一个配置
../configure --enable-bootstrap --enable-languages=c,c++,objc,obj-c++,fortran,go,lto --enable-shared --enable-threads=posix --enable-checking=release --enable-multilib --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only --with-linker-hash-style=gnu --enable-plugin --enable-initfini-array --with-isl --enable-libmpx --enable-libsanitizer --enable-gnu-indirect-function --enable-libcilkrts --enable-libatomic --enable-libquadmath --enable-libitm --with-tune=generic --with-arch_32=x86-64
```

## 错误处理

## 7.3.0

```shell
# 错误
../../.././libsanitizer/sanitizer_common/sanitizer_platform_limits_posix.cc:157:10: fatal error: sys/ustat.h: No such file or directory
 #include <sys/ustat.h>
 
# 解决方案
## 1. 不编译 sanitizer, configure 时添加参数 --disable-libsanitizer
vim libsanitizer/sanitizer_common/sanitizer_platform_limits_posix.cc
## 2. 注释第 157、250 行
// #include <sys/ustat.h>
// unsigned struct_ustat_sz = sizeof(struct ustat);
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
-Wno-error=...	    关闭某项警告视为错误
-Wno-<warning-name>	关闭某项警告
-Wextra
-w                  忽略所有警告

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

## 注意

- `-w` 和 `-Werror... ` 同时用会有冲突，`-w` 会短路 `-Werror`。`-w -Werror=...`  和 `-Werror=... -w` 都不行。

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

# 修改系统默认库查找路径

```shell
export LIBRARY_PATH={path}:{path}
```

# AUR 低版本 GCC

```shell
configure:4314: $? = 0
configure:4303: gcc -V >&5
gcc: error: unrecognized command-line option '-V'
gcc: fatal error: no input files
```

上面的报错可以忽略，只是尝试探测 gcc 版本，详见 [这里](https://superuser.com/questions/846768/gcc-unrecognized-command-line-options-v-and-qversion-with-autoconf)。
