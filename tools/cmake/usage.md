---
title: cmake 使用
categories: 
	- [工具,cmake]
tags:
	- cmake
date: 2020/12/31 00:00:00
update: 2020/12/31 00:00:00
---

[toc]

# Command Line

```shell
$ Generate a Project Buildsystem
# cmake [<options>] <path-to-source>
# cmake [<options>] <path-to-existing-build>
# cmake [<options>] -S <path-to-source> -B <path-to-build>

$ Build a Project
# cmake --build <dir> [<options>] [-- <build-tool-options>]

$ Install a Project
# cmake --install <dir> [<options>]

$ Open a Project
# cmake --open <dir>

$ Run a Script
# cmake [{-D <var>=<value>}...] -P <cmake-script-file>

$ Run a Command-Line Tool
# cmake -E <command> [<options>]

$ Run the Find-Package Tool
# cmake --find-package [<options>]

$ View Help
# cmake --help[-<topic>]
```

# CMakeLists

## 设置cmake最小版本

```cmake
cmake_minimum_required(VERSION 2.8)
```

## 设置项目名称

```cmake
project("...")
```

## 判断OS

```cmake
if (APPLE)
  # do something
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
elseif (UNIX)
  # do something
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
endif()
```

## 生成共享库

```cmake
add_library(name SHARED src)
```

## 使用静态库

```cmake
SET(CMAKE_FIND_LIBRARY_SUFFIXES ".a")    # 查找库文件后缀
SET(BUILD_SHARED_LIBS OFF)							 # 关闭使用共享库
SET(CMAKE_EXE_LINKER_FLAGS "-static")    # 连接时使用静态库
```

## 生成可执行文件

```cmake
add_executable(MAIN src/main.cpp)
```

## 包含cmake文件

```cmake
include(path/to/cmake)
```

## 打印消息

```cmake
MESSAGE("msg...")
```

## 指定compiler

```cmake
set(CMAKE_C_COMPILER "gcc-5")
set(CMAKE_CXX_COMPILER "g++-5")
```

## 编译类型

```shell
set(CMAKE_BUILD_TYPE=Release)	# or Debug
```

## 指定FLAGS

```shell
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
```

