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
