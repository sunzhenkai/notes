---
title: cmake 使用
categories: 
  - [工具,cmake]
tags:
  - cmake
date: "2020-12-31T00:00:00+08:00"
update: "2020-12-31T00:00:00+08:00"
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

# macro

```cmake
macro(AddLibrary MODULE)
    set(options NONE)
    set(oneValueArgs PREFIX DEP)
    set(multiValueArgs SUBMODULES)
    cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
    message(STATUS "AddLibrary MODULE=${MODULE} PREFIX=${ARG_PREFIX} DEP=${ARG_DEP} SUBMODULES=${ARG_SUBMODULES}")


    if ("${ARG_PREFIX}" STREQUAL "")
        message(FATAL_ERROR "PREFIX should not be empty")
    endif ()
    foreach (I IN LISTS ARG_SUBMODULES)
        set(TGT ${MODULE}::${I})
        add_library(${TGT} STATIC IMPORTED GLOBAL)
        set_target_properties(${TGT} PROPERTIES
                IMPORTED_LOCATION "${ARG_PREFIX}/lib/${CMAKE_STATIC_LIBRARY_PREFIX}${I}${CMAKE_STATIC_LIBRARY_SUFFIX}"
                INCLUDE_DIRECTORIES ${ARG_PREFIX}/include)
        add_dependencies(${TGT} ${ARG_DEP})
    endforeach ()
endmacro(AddLibrary)
```

```cmake
macro(AddLibraryV2 MODULE)
    set(options NONE)
    set(oneValueArgs PREFIX DEP)
    set(multiValueArgs SUBMODULES)
    cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
    message(STATUS "AddLibrary MODULE=${MODULE} PREFIX=${ARG_PREFIX} DEP=${ARG_DEP} SUBMODULES=${ARG_SUBMODULES}")


    if ("${ARG_PREFIX}" STREQUAL "")
        message(FATAL_ERROR "PREFIX should not be empty")
    endif ()
    foreach (I IN LISTS ARG_SUBMODULES)
        find_path(TGT_LIB_${I} NAMES "${I}" "lib${I}" HINTS ${ARG_PREFIX} PATH_SUFFIXES lib lib64)
        find_path(TGT_INCLUDE_${I} NAMES "${MODULE}" HINTS ${ARG_PREFIX} PATH_SUFFIXES include)
        set(TGT ${MODULE}::${I})
        message(STATUS "AddLibrary TARGET=${TGT} TARGET_LIB_DIR=${TGT_LIB_${I}} TARGET_INCLUDE_DIR=${TGT_INCLUDE_${I}}")
        add_library(${TGT} STATIC IMPORTED GLOBAL)
        set_target_properties(${TGT} PROPERTIES
                IMPORTED_LOCATION "${TGT_LIB_${I}}/${CMAKE_STATIC_LIBRARY_PREFIX}${I}${CMAKE_STATIC_LIBRARY_SUFFIX}"
                INCLUDE_DIRECTORIES ${TGT_INCLUDE_${I}})
        add_dependencies(${TGT} ${ARG_DEP})
        include_directories(${TGT_INCLUDE_${I}})
    endforeach ()
endmacro(AddLibraryV2)
```

