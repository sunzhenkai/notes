---
title: cmake 使用
categories: 
	- [工具,cmake]
tags:
	- cmake
date: 2020/12/31 00:00:00
update: 2020/12/31 00:00:00
---

# 示例

**CMakeLists.txt**

```shell
$ mkdir cmake-project
$ cd cmake-project
$ touch CMakeLists.txt
```

**Code**

```shell
$ mkdir src && vim src/main.cpp
```

**Config**

```cmake
cmake_minimum_required(VERSION 3.10)

# set the project name
project(Tutorial)

# add the executable
add_executable(Tutorial src/main.cpp)
```

**Build**

```shell
$ mkdir build && cd build
$ cmake ..
$ make
```

**Run**

```shell
$ ./Tutorial
Hello, CMake.
```

# **语法示例**

```cmake
cmake_minimum_required(VERSION 2.8)
project("pybindcpp")
add_executable(HELLO src/pybindcpp.cpp)
```

# **完整示例**

```cmake
cmake_minimum_required(VERSION 2.8)
project("pybindcpp")

add_executable(HELLO src/pybindcpp.cpp)
```

# **编译**

```shell
$ mkdir build && cd build
$ cmake ..
$ make
```