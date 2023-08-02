---
title: gflags
categories: 
  - [coding, c++, library]
tags:
  - c++
  - gflags
date: 2021/01/06 21:00:00
---

# 编译

```shell
$ mkdir build && cd build
$ cmake -DCMAKE_INSTALL_PREFIX:PATH="/path/to/install" -DBUILD_SHARED_LIBS=1 .. # 编译共享库，如需打包静态库 添加 -DBUILD_STATIC_LIBS=1；默认打包静态库，指定打包共享库不打包静态库，可同时指定
# -DGFLAGS_NAMESPACE=google  指定 namespace 名称，默认gflags
$ make -j4 && make install
```

更多参考[这里](https://github.com/gflags/gflags/blob/master/INSTALL.md)。

# CMake

**提取Namespace**

```cmake
execute_process(
        COMMAND bash -c "grep \"namespace [_A-Za-z0-9]\\+ {\" ${DEPS_INCLUDE_DIR}/gflags/gflags_declare.h | head -1 | awk '{print $2}' | tr -d '\n'"
        OUTPUT_VARIABLE GFLAGS_NS
)

if (${GFLAGS_NS} STREQUAL "GFLAGS_NAMESPACE")
    execute_process(
            COMMAND bash -c "grep \"#define GFLAGS_NAMESPACE [_A-Za-z0-9]\\+\" ${DEPS_INCLUDE_DIR}/gflags/gflags_declare.h | head -1 | awk '{print $3}' | tr -d '\n'"
            OUTPUT_VARIABLE GFLAGS_NS
    )
endif ()
message("gflags namespace: " ${GFLAGS_NS})
```

# 使用

## 类型

基于gflags的设计哲学，不提供复杂的数据类型，可自行解析。

- DEFINE_bool
- DEFINE_int32
- DEFINE_int64
- DEFINE_uint64
- DEFINE_double
- DEFINE_string

## 定义

**示例**

```c++
#include <gflags/gflags.h>

   DEFINE_bool(big_menu, true, "Include 'advanced' options in the menu listing");
   DEFINE_string(languages, "english,french,german",
                 "comma-separated list of languages to offer in the 'lang' menu");
```

**说明**

可在任意文件中定义flag，但只能定义一次（只能 DEFINE 一次，但是可 DECLARE 多次）。如果需要访问位于多个源文件中的glfag，那么在其他文件中使用 DECLARE。最好，在`foo.cc` 中使用 DEFINE 定义，在`foo.h` 中使用 DECLARE 声明，那么只要在代码中添加 `#include <foo.h>` 就可以使用该flag。

## 访问

```c++
// 修改
FLAGS_languages += ",klingon";

// 方法调用
if (FLAGS_languages.find("finnish") != string::npos) {
  // do something
}
```

## 声明检查

```c++
static bool ValidatePort(const char* flagname, int32 value) {
   if (value > 0 && value < 32768)   // value is ok
     return true;
   printf("Invalid value for --%s: %d\n", flagname, (int)value);
   return false;
}
DEFINE_int32(port, 0, "What port to listen on");
DEFINE_validator(port, &ValidatePort);
```

在全局初始化时（紧接着DEFINE_int32定义flag）注册检查方法，可以保证在运行`main()`函数解析命令号之前执行校验。上面的代码，使用`DEFINE_validator` 宏指令调用 `RegisterFlagValidator` 方法，如果注册成功，返回true；如果第一个参数不是命令行标记或者该标记注册了其他校验，则返回false；返回值以`<flag>_validator_registered` 命名作为全局变量供访问。

## 解析标记

```c++
gflags::ParseCommandLineFlags(&argc, &argv, true);
```

通常，改代码唯有`main()`的开始。`argc` 和 `argv` 是传入`main()` 方法的准确参数，该例程可能会修改他们。最后的布尔参数用于指示是否从`argc`中删除标记（flags）以及其参数（arguments），并同步修改`argv`。如果为true，在该方法调用之后，argv只会保存命令行参数（commandline arguments），而不是命令行标记（glags）。如果为false，那么 ParseCommandLineFlags 不会修改 argc，但是会对argv中的参数重排序，使得所有的标记在最开始。比如，`"/bin/foo" "arg1" "-q" "arg2"`，方法会重排序 argv 为 `"/bin/foo" "-q" "arg1" "arg2"`，ParseCommandLineFlags 返回 argv 中第一个参数的索引，也即标记（flag）的后面的索引（在刚才的例子中，返回2，因为 argv[2] 指向第一个参数 arg1）。

**注**，命令行标记（commandline glags）形如 `-e -q`，命令行参数（commandline arguments）形如 `arg1 arg2` 。

## 在命令行设置标记

```shell
$ foo --nobig_menu -languages="chinese,japanese,korean" ...
```

当运行 ParseCommandLineFlags 时，会设置 `FLAGS_big_menu = false; FLAGS_languages = "chinese,japanese,korean"`。通过在标记前面添加`no`，为标记设置为 false 值。以下方式均可设置 languages 值。

```c++
app_containing_foo --languages="chinese,japanese,korean"
app_containing_foo -languages="chinese,japanese,korean"
app_containing_foo --languages "chinese,japanese,korean"
app_containing_foo -languages "chinese,japanese,korean"
```

布尔型值稍有不同。

```c++
app_containing_foo --big_menu
app_containing_foo --nobig_menu
app_containing_foo --big_menu=true
app_containing_foo --big_menu=false
```

尽管有很多方式灵活设置标记值，但是推荐使用统一的格式 `--variable=value`，对于布尔值使用 `--variable/--novariable`。

**注意**

- 如果在命令行中指定了标记，但是没有在程序中定义（使用DEFINE），将会导致致命错误。可以通过添加 `--undefok` 来屏蔽该异常
- 在 getopt 中，`--` 标记会终止标记解析，所以 `foo -f1 1 -- -f2 2`，中，`f1` 是标记，`f2` 不是
- 如果标记被指定多次，后面的值覆盖前面的，即最后一次定义有效
- 不像 getopt 库那样支持 单字母同义词，比如 `-h` （和 `--help` 同义），同样的也不支持组合标记，如 `ls -la `

## 修改默认值

有时候标记位于依赖库中，如果只想在一个程序中修改默认值，其他应用不变。可在 `main()` 方法中赋值新值，在调用 `ParseCommandLineFlags` 之前。

```c++
   DECLARE_bool(lib_verbose);   // mylib has a lib_verbose flag, default is false
   int main(int argc, char** argv) {
     FLAGS_lib_verbose = true;  // in my app, I want a verbose lib by default
     ParseCommandLineFlags(...);
   }
```

这种情况下，用户依然可以在命令行中指定标记值，但是如果不指定，则使用新的默认值。

## 特殊标记

- `--undefok=flagname,flagname,...` 

  - 对于指定的这些标记名称，用于阻止当命令行指定标记但在程序中未定义导致的异常退出

- `--fromenv`

  - `--fromenv=foo,bar`

  - 从环境变量中读取值，如果环境变量中未定义，则会导致致命异常

  ```shell
    export FLAGS_foo=xxx; export FLAGS_bar=yyy   # sh
    setenv FLAGS_foo xxx; setenv FLAGS_bar yyy   # tcsh
    
    # 等同于
    
    --foo=xxx, --bar=yyy
  ```

- `--tryfromenv`

  - 类似于 `--fromenv` ，区别是如果环境变量中未定义标记，不会导致异常

- `--flagfile`

  - `--flagfile=f`

  - 从文件读取参数定义，文件内容为标记定义列表，每行一个

  - 与命令行不同的是，需要等号将标记和参数值分开（命令行参数有多种设置方式，可不加等号）

  ```shell
    # 示例文件 /tmp/myflags:
    --nobig_menus
    --languages=english,french
    
    # 两种等价方式
    ./myapp --foo --nobig_menus --languages=english,french --bar   # --foo 和 --bar 泛指其他参数
  ./myapp --foo --flagfile=/tmp/myflags --bar
  ```
  
  - 注意：flagfiles方式，一些错误会默认禁止。特别的，未识别的标记名异常默认忽略（这在命令行设置方式下，需要显式使用`--undefok` 指定），以及未指定值的异常（比如在flagfile中只定义 `--languages` ，而不指定参数）
  
  - 通常的 flagfile 比示例要复杂：一系列文件名，每行一个，每个后面紧接着一系列标记，每行一个，根据需要重复多次。flagfile中的文件名可用通配符，比如 `*` 和 `?`，仅当当前程序的名称和flagfile文件中filenames中的一个匹配时，才会处理其挨着的标记
  
  - 以 `#` 开头的行会被忽略
  
  - 空白行及前置空白符会被忽略
  
  - 可在 flagfile 中使用 `--flagfile ` 指定其他 flagfile
  
  - 标记总是以期望的方式处理，首先从检查命令行参数开始，如果遇到 flagfile ，则处理其内容，然后继续处理后续标记
  
```shell
    # 示例文件 gflags_test.cmd
    gflags-test-foo
    --port=10000
    --service_name=gflags_test_foo
    gflags-test-bar
    --port=20000
    --service_name=gflags_test_bar
    
    # 如果程序名称是 gflags-test-foo，则 --port=10000 --service_name=gflags_test_foo
    # 如果程序名称是 gflags-test-bar，则 --port=20000 --service_name=gflags_test_bar
    # 实例程序参考这里 https://github.com/sunzhenkai/cooking/blob/master/c%2B%2B/universal/scripts/gflags_test.sh
```

## 其他

**移除帮助信息**

可减少编译源文件时的帮助信息，及二进制文件大小，或一些安全相关的隐患。

```c++
#define STRIP_FLAG_HELP 1    // this must go before the #include!
#include <gflags/gflags.h>
```

# 问题

## NO 1

**描述**

```
ERROR: something wrong with flag 'flagfile' in file '/home/wii/Git/cooking/c++/universal/third/build/gflags-2.2.2/src/gflags.cc'.  One possibility: file '/home/wii/Git/cooking/c++/universal/third/build/gflags-2.2.2/src/gflags.cc' is being linked both statically and dynamically into this executable.
```

**解决**

在编译gflags时，使用 cmake 参数 `-DBUILD_SHARED_LIBS=1` 指定只编译共享库。

# 参考

- https://gflags.github.io/gflags/

