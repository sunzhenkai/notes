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

# 内置变量

```cmake
PROJECT_SOURCE_DIR           项目目录
CMAKE_CURRENT_LIST_DIR 		   当前 cmake 文件所在目录
CMAKE_STATIC_LIBRARY_PREFIX  静态库前缀, 例如 lib
CMAKE_STATIC_LIBRARY_SUFFIX  静态库后缀, 例如 .a
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

## 遍历

```cmake
set(L 1 2 3)
foreach(ITEM IN LISTS L)
	messag(STATUS "item: ${ITEM}")
endforeach()
```

## 循环

```cmake
set (L A B C)
foreach (V IN LISTS L)
	... ${V}
endforeach()
```

# 变量

## 判断变量是否定义

```cmake
if (DEFINED VAR_NAME) # NOT DEFINED VAR_NAME
	...
endif()
```

## 转换字符串为大写

```cmake
string(TOUPPER ${ORIGIN_VAR} DEST_VAR)
```

## 判断变量为空

```cmake
if (${V} STREQUAL "")
	...
endif()
```

## 变量默认值

```cmake
# option, 只对 BOOL 类型, 默认 OFF
option(BUILD_THIRD_PARTY "build third party library" ON)

# cache, STRING 类型等
set(BUILD_THIRD_PARTY ON CACHE BOOL "build third party library")
set(DEPS_DIR "/tmp/cpp-external-lib" CACHE STRING "library install prefix" )
```

# 修改库搜索路径

```shell
export CMAKE_PREFIX_PATH="$CUSTOME_LIBRARY_PATH"
export CMAKE_LIBRARY_PATH="$CUSTOME_LD_LIBRARY_PATH"
```

# 查找&链接库

```cmake
# 将库路径写入 CMAKE_PREFIX_PATH
set(CMAKE_PREFIX_PATH ${PATH_TO_LIB} ${CMAKE_PREFIX_PATH})
find_package(<library-name> REQUIRED)
# 使用
target_link_libraries(<library-name> <target-name>)
```

**示例**

```cmake
find_package(Snappy REQUIRED)
target_link_libraries(brpc Snappy::snappy)
```

# 自定义 Find Cmake 文件

```cmake
find_path(THRIFT_INCLUDE_DIR
    NAMES
        thrift/Thrift.h
    HINTS
        /usr/local
    PATH_SUFFIXES
        include
)

find_library(THRIFT_LIBRARIES
    NAMES
        thrift libthrift
    HINTS
        /usr/local
    PATH_SUFFIXES
        lib lib64
)

find_program(THRIFT_COMPILER
    NAMES
        thrift
    HINTS
        /usr/local
    PATH_SUFFIXES
        bin bin64
)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(THRIFT DEFAULT_MSG THRIFT_LIBRARIES THRIFT_INCLUDE_DIR THRIFT_COMPILER)
# 设置变量为高级，在 GUI 模式下默认不展示
mark_as_advanced(THRIFT_LIBRARIES THRIFT_INCLUDE_DIR THRIFT_COMPILER)
```

# 引入库

## 引入第三方库

> 引入第三方库的几种方式。第一种，find_path 查找头文件，find_library 查找库文件，分别使用 include_directories(DEP_INCLUDE_DIR)、target_link_libraries(target library) 链接库，这种方式一般用于没有 Find*.cmake 的库。第二种，对于有 Find cmake 的库，可以使用 find_package(Library REQUIRED) 来 import 库，然后使用 target_link_libraries 来链接库。第三种，自定义 Find Cmake 文件，借助 find_package_handle_standard_args 实现。对于有 pkgconfig 的库来说，也可以用 pkg_check_modules 来导入，但是有个问题，pkgconfig 内可能有写死的 prefix，移动之后可能会出现找不到库的问题。
>
> ```cmake
> # snappy
> find_package(Snappy REQUIRED)
> target_link_libraries(brpc-static Snappy::snappy)
> 
> # thrift
> find_path(THRIFT_INCLUDE_DIR NAMES thrift/Thrift.h PATH_SUFFIXES include)
> find_library(thrift thrift REQUIRED CONFIG)
> include_directories(${THRIFT_INCLUDE_DIR})
> target_link_libraries(brpc-static thrift)
> 
> # pkg_check_modules
> include(FindPkgConfig)
> pkg_check_modules(Curl libcurl REQUIRED)
> # Curl_INCLUDE_DIR、Curl_LIBRARIES、Curl_FOUND 会被设置
> ```

**示例**

```cmake
include(FindPkgConfig)
pkg_check_modules(brpc REQUIRED IMPORTED_TARGET brpc)
target_link_libraries(target PkgConfig::brpc)
```

## 使用 PkgConfig 文件添加库

**简版**

[文档](https://cmake.org/cmake/help/latest/module/FindPkgConfig.html#command:pkg_check_modules)。

```shell
# search
find_package(PkgConfig REQUIRED)
pkg_check_modules(SDL2 REQUIRED sdl2)

# link
target_link_libraries(testapp ${SDL2_LIBRARIES})
target_include_directories(testapp PUBLIC ${SDL2_INCLUDE_DIRS})
target_compile_options(testapp PUBLIC ${SDL2_CFLAGS_OTHER})
```

**自己添加 target**

- https://github.com/scylladb/seastar/blob/master/cmake/Findhwloc.cmake

## find_package

```cmake
# 完整签名
find_package(<PackageName> [version] [EXACT] [QUIET]
             [REQUIRED] [[COMPONENTS] [components...]]
             [OPTIONAL_COMPONENTS components...]
             [CONFIG|NO_MODULE]
             [GLOBAL]
             [NO_POLICY_SCOPE]
             [BYPASS_PROVIDER]
             [NAMES name1 [name2 ...]]
             [CONFIGS config1 [config2 ...]]
             [HINTS path1 [path2 ... ]]
             [PATHS path1 [path2 ... ]]
             [REGISTRY_VIEW  (64|32|64_32|32_64|HOST|TARGET|BOTH)]
             [PATH_SUFFIXES suffix1 [suffix2 ...]]
             [NO_DEFAULT_PATH]
             [NO_PACKAGE_ROOT_PATH]
             [NO_CMAKE_PATH]
             [NO_CMAKE_ENVIRONMENT_PATH]
             [NO_SYSTEM_ENVIRONMENT_PATH]
             [NO_CMAKE_PACKAGE_REGISTRY]
             [NO_CMAKE_BUILDS_PATH] # Deprecated; does nothing.
             [NO_CMAKE_SYSTEM_PATH]
             [NO_CMAKE_INSTALL_PREFIX]
             [NO_CMAKE_SYSTEM_PACKAGE_REGISTRY]
             [CMAKE_FIND_ROOT_PATH_BOTH |
              ONLY_CMAKE_FIND_ROOT_PATH |
              NO_CMAKE_FIND_ROOT_PATH])
```

### CONFIG 命令

```cmake
find_package(PackageName CONFIG)
```

`CONFIG` 命令会尝试搜索包提供的 `<PackageName>Config.cmake` 或 `<lowercasePackageName>-config.cmake` 文件，并把包含该文件的文件夹路径赋值给 `<PackageName>_DIR` ，`<PackageName>_CONFIG` 保存配置文件的完整路径。

### 默认搜索路径



### 指定搜索路径

```shell
find_package (<package> PATHS paths... NO_DEFAULT_PATH)
# NO_DEFAULT_PATH: 不使用默认路径
```

### 设置变量

```shell
# 不管是否找到都会设置
{PackageName}_FOUND
```

# 库管理

## ExternalProject_Add

```shell
include(ExternalProject)

set(target spdlog)
set(CMAKE_ARGS
        -DCMAKE_BUILD_TYPE=Release
        -DCMAKE_INSTALL_PREFIX=${DEPS_PREFIX}
        -DCMAKE_INSTALL_LIBDIR=lib
        -DBUILD_STATIC_LIB=ON
        -DBUILD_SHARED_LIB=OFF)
ExternalProject_Add(
        ${target}_build
        GIT_REPOSITORY https://github.com/gabime/spdlog.git
        GIT_TAG v1.9.2
        CMAKE_ARGS ${CMAKE_ARGS}
)

# 指定 libary 安装文件夹，统一在 lib/lib64
-DCMAKE_INSTALL_LIBDIR=lib

# 参数
ExternalProject_Add(
        <target-name>
        GIT_REPOSITORY <git-repo-address>
        GIT_TAG <git-tag>
        PREFIX <prefix-path>        # 创建 build、src 等目录所在的位置, 不是安装的路径
        INSTALL_DIR <install_dir>		# 不是安装的位置，作为属性，可用 ExternalProject_Get_Property 获取，在 CONFIGURE_COMMAND 等中指定 prefix
        CMAKE_ARGS ${CMAKE_ARGS}
)
```

### 传入 CMAKE_C_FLAGS / CMAKE_CXX_FLAGS

```shell
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -lstdc++ -ldl")
ExternalProject_Add(... CMAKE_ARGS -DCMAKE_C_FLAGS=${CMAKE_C_FLAGS})

# 注意: 下面方式均不可
ExternalProject_Add(... CMAKE_ARGS -DCMAKE_C_FLAGS=-lstdc++ -ldl)
ExternalProject_Add(... CMAKE_ARGS -DCMAKE_C_FLAGS="-lstdc++ -ldl")
ExternalProject_Add(... CMAKE_ARGS -DCMAKE_C_FLAGS='-lstdc++ -ldl')
```

## AddLibrary

```cmake
add_library(${TGT} STATIC IMPORTED GLOBAL)
set_target_properties(${TGT} PROPERTIES
	IMPORTED_LOCATION "${TGT_PREFIX}/lib/${CMAKE_STATIC_LIBRARY_PREFIX}${TGT}${CMAKE_STATIC_LIBRARY_SUFFIX}"
	INCLUDE_DIRECTORIES ${TGT_PREFIX}/include
	INTERFACE_INCLUDE_DIRECTORIES ${TGT_PREFIX}/include
)

# INTERFACE_INCLUDE_DIRECTORIES
set_target_propterties 添加 INTERFACE_INCLUDE_DIRECTORIES, 在 target_link_libraries 时，不需要再 include 库的头文件
```

## FetchContent_Declare

FetchContent_Declare 通常和 FetchContent_MakeAvailable 一块使用。

FetchContent_MakeAvailable 是 cmake 3.14 引入的。

FetchContent_Declare 的参数参考 ExternalProject_Add，和 ExternalProject_Add 相比，屏蔽了下面的命令。

- `CONFIGURE_COMMAND`
- `BUILD_COMMAND`
- `INSTALL_COMMAND`
- `TEST_COMMAND`

### URL 指定本地文件

```shell
FetchContent_Declare(
        boost
        URL file:///tmp/boost-submodule-boost-1.80.0-1.tar.gz
)
```

## 指定 CMakeLists.txt 路径

如果 `CMakeLists.txt` 文件不在仓库根目录下，可以用 `SOURCE_SUBDIR` 来指定子路径。

```cmake
include(FetchContent)
FetchContent_Declare(
  protobuf
  GIT_REPOSITORY https://github.com/protocolbuffers/protobuf.git
  GIT_TAG        ae50d9b9902526efd6c7a1907d09739f959c6297 # v3.15.0
  SOURCE_SUBDIR  cmake
)
```

## Configure 阶段让 Target 可用

- [ref 1](https://stackoverflow.com/questions/36084785/building-a-tool-immediately-so-it-can-be-used-later-in-same-cmake-run)
- [ref 2](https://stackoverflow.com/questions/17446981/cmake-externalproject-add-and-findpackage/23570741#23570741)

# 方法 (function)

```cmake
function(FNAME)
endfunction(FNAME)
```

## 作用域

方法有独立的作用域，可以访问父级作用域内的变量。在函数内定义的变量，对父级作用域不可访问。如果需要修改父级作用域变量，需要使用 PARENT_SCOPE。

```cmake
SET(VAR vALUEe PARENT_SCOPE)
```

## 参数

### 参数列表指定

```cmake
function(ARG version url flag)
    message(STATUS "version: ${version}, url: ${url}, flag: ${flag}")
endfunction(ARG)

ARG(1.0.0 www.so.com true)
```

### 非参数列表

首先了解在函数内定义的默认变量。

- ARGC，参数数量
- ARGN，参数，去掉声明的参数的参数列表
- ARGV，参数，全部参数
- ARG0，ARG1 ...

```cmake

function(ARG4)
    set(options OPTIONAL FAST)
    set(oneValueArgs NAME URL)
    set(multiValueArgs KEY)
    cmake_parse_arguments(PREFIX "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
    message(STATUS "FAST=${PREFIX_FAST} NAME=${PREFIX_NAME} URL=${PREFIX_URL} KET=${PREFIX_KEY}")
endfunction(ARG4)

ARG4(
        FAST
        NAME beijing
        URL www.so.com
        KEY weight price
)
# FAST=TRUE NAME=beijing URL=www.so.com KET=weight;price

ARG4(
        URL www.so.com
        KEY band price
)
# FAST=FALSE NAME= URL=www.so.com KET=band;price
```

# 宏 (macro)

```cmake
macro(MName)
endmacro(MName)
```

Macro 和 function 比较相似，区别如下。

- macro 和调用域共享变量的作用域，function 则有独立的作用域

# 参考

- https://github.com/snikulov/cmake-modules/blob/master/FindThrift.cmake

# 编译优化

## ccache

```shell
# 安装
sudo yum install ccache

# 配置
-DCMAKE_CXX_COMPILER_LAUNCHER=ccache
```

