---
title: cmake/makefile flags
categories: 
  - [工具,cmake]
tags:
  - cmake
date: 2021/01/4 00:00:00
update: 2021/01/4 00:00:00
---

# 规约

**编译源文件**

```shell
$(CC) $(CPPFLAGS) $(CFLAGS) example.c -c -o example.o # -c: 编译，不执行链接操作
```

**链接**

```shell
$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) example.c -o example # -o: 指定输出文件名字
```

# 命令

| 命令 | 说明                                |
| ---- | ----------------------------------- |
| CC   | C 编译器                            |
| CXX  | C++ 编译器                          |
| CPP  | C / C++ 预编译器，通常是 "$(CC) -E" |

**示例**

```shell
export CC=/usr/local/bin/gcc-7
export CXX=/usr/local/bin/g++-7
```

# 变量

| 变量               | 含义                                                         | 示例     |
| ------------------ | ------------------------------------------------------------ | -------- |
| CFLAGS             | C 编译器选项                                                 |          |
| CXXFLAGS           | C++ 编译器选项                                               |          |
| CPPFLAGS           | C/C++ 预处理器的命令行参数                                   |          |
| LDFLAGS            | 链接参数                                                     |          |
| LD_LIBRARY_PATH    | 运行时动态链接库查找路径                                     |          |
| LIBRARY_PATH       | 编译时链接库查找路径                                         | /usr/lib |
| C_INCLUDE_PATH     | 头文件查找路径                                               |          |
| CPLUS_INCLUDE_PATH | C++ 头文件查找路径                                           |          |
| OBJC_INCLUDE_PATH  | ObjectiveC 头文件查找路径                                    |          |
| CPATH              | C/C++/ObjectiveC 头文件默认查找路径，多个路径使用 `:` 分隔，比如 `.:/root/include` |          |
| DYLD_LIBRARY_PATH  | Mac OS 动态链接库查找路径                                    |          |

# 参数

| 参数       | 说明                                                     | 示例                  |
| ---------- | -------------------------------------------------------- | --------------------- |
| c          | 编译                                                     | -c                    |
| o          | 输出文件名称                                             | -o                    |
| g          | 添加调试信息                                             | -g                    |
| l（小写L） | 链接标准库                                               | -lz                   |
| L          | 指定库搜索路径                                           | -L/user/local/lib     |
| I（大写i） | 指定头文件搜索路径                                       | -I/user/local/include |
| static     | 在支持动态链接的系统中，该参数覆盖-pie，并阻止链接共享库 | -static               |
| shared     | 生成可被链接的共享对象                                   | -shared               |
| PIC / pic  | 使用位置无关代码创建对象文件，创建共享库时需指定         | -fpic / -fPIC         |

# 说明

- ` -llibrary` / `-l library` 链接时，搜索指定库，优先使用共享库，除非指定 `-static` 参数
