---
title: cmake troubleshoot
categories: 
  - [工具,cmake]
tags:
  - cmake
date: 2024/02/27 00:00:00
update: 2024/02/27 00:00:00
---

# Cmake 工程测试不通过

## 错误信息

```shell
Performing C SOURCE FILE Test CMAKE_HAVE_LIBC_PTHREAD failed with the following output:
Change Dir: /tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-ZS4h4J

Run Build Command(s):/usr/bin/gmake -f Makefile cmTC_48078/fast && /usr/bin/gmake  -f CMakeFiles/cmTC_48078.dir/build.make CMakeFiles/cmTC_48078.dir/build
gmake[1]: Entering directory `/tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-ZS4h4J'
Building C object CMakeFiles/cmTC_48078.dir/src.c.o
/opt/scylladb/bin/gcc -DCMAKE_HAVE_LIBC_PTHREAD  -fdiagnostics-color=always -o CMakeFiles/cmTC_48078.dir/src.c.o -c /tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-ZS4h4J/src.c
Linking C executable cmTC_48078
/data/zhenkai.sun/app/cmake-3.25.1-linux-x86_64/bin/cmake -E cmake_link_script CMakeFiles/cmTC_48078.dir/link.txt --verbose=1
/opt/scylladb/bin/gcc CMakeFiles/cmTC_48078.dir/src.c.o -o cmTC_48078
CMakeFiles/cmTC_48078.dir/src.c.o: In function `main':
src.c:(.text+0x2d): undefined reference to `pthread_create'
src.c:(.text+0x39): undefined reference to `pthread_detach'
src.c:(.text+0x45): undefined reference to `pthread_cancel'
src.c:(.text+0x56): undefined reference to `pthread_join'
collect2: error: ld returned 1 exit status
gmake[1]: *** [cmTC_48078] Error 1
gmake[1]: Leaving directory `/tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-ZS4h4J'
gmake: *** [cmTC_48078/fast] Error 2


Source file was:
#include <pthread.h>

static void* test_func(void* data)
{
  return data;
}

int main(void)
{
  pthread_t thread;
  pthread_create(&thread, NULL, test_func, NULL);
  pthread_detach(thread);
  pthread_cancel(thread);
  pthread_join(thread, NULL);
  pthread_atfork(NULL, NULL, NULL);
  pthread_exit(NULL);

  return 0;
}

Performing C++ SOURCE FILE Test StdAtomic_EXPLICIT_LINK failed with the following output:
Change Dir: /tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-pPTD7R

Run Build Command(s):/usr/bin/gmake -f Makefile cmTC_f3ae9/fast && /usr/bin/gmake  -f CMakeFiles/cmTC_f3ae9.dir/build.make CMakeFiles/cmTC_f3ae9.dir/build
gmake[1]: Entering directory `/tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-pPTD7R'
Building CXX object CMakeFiles/cmTC_f3ae9.dir/src.cxx.o
/opt/scylladb/bin/g++ -DStdAtomic_EXPLICIT_LINK  -w -g -pthread -fno-omit-frame-pointer -Werror=return-type -fsanitize=address -fdiagnostics-color=always -std=gnu++1z -o CMakeFiles/cmTC_f3ae9.dir/src.cxx.o -c /tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-pPTD7R/src.cxx
Linking CXX executable cmTC_f3ae9
/data/zhenkai.sun/app/cmake-3.25.1-linux-x86_64/bin/cmake -E cmake_link_script CMakeFiles/cmTC_f3ae9.dir/link.txt --verbose=1
/opt/scylladb/bin/g++ -w -g -pthread -fno-omit-frame-pointer -Werror=return-type -fsanitize=address CMakeFiles/cmTC_f3ae9.dir/src.cxx.o -o cmTC_f3ae9  -latomic
/usr/bin/ld: cannot find /opt/scylladb/lib64/libatomic.so.1.2.0
collect2: error: ld returned 1 exit status
gmake[1]: *** [cmTC_f3ae9] Error 1
gmake[1]: Leaving directory `/tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-pPTD7R'
gmake: *** [cmTC_f3ae9/fast] Error 2


Source file was:
int main() {}

Performing C++ SOURCE FILE Test StdFilesystem_NO_EXPLICIT_LINK failed with the following output:
Change Dir: /tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-DLboHE

Run Build Command(s):/usr/bin/gmake -f Makefile cmTC_29ea1/fast && /usr/bin/gmake  -f CMakeFiles/cmTC_29ea1.dir/build.make CMakeFiles/cmTC_29ea1.dir/build
gmake[1]: Entering directory `/tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-DLboHE'
Building CXX object CMakeFiles/cmTC_29ea1.dir/src.cxx.o
/opt/scylladb/bin/g++ -DStdFilesystem_NO_EXPLICIT_LINK  -w -g -pthread -fno-omit-frame-pointer -Werror=return-type -std=c++17 -fdiagnostics-color=always -std=gnu++1z -o CMakeFiles/cmTC_29ea1.dir/src.cxx.o -c /tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-DLboHE/src.cxx
Linking CXX executable cmTC_29ea1
/data/zhenkai.sun/app/cmake-3.25.1-linux-x86_64/bin/cmake -E cmake_link_script CMakeFiles/cmTC_29ea1.dir/link.txt --verbose=1
/opt/scylladb/bin/g++ -w -g -pthread -fno-omit-frame-pointer -Werror=return-type -std=c++17 CMakeFiles/cmTC_29ea1.dir/src.cxx.o -o cmTC_29ea1
CMakeFiles/cmTC_29ea1.dir/src.cxx.o: In function `std::experimental::filesystem::v1::path::path<char [6], std::experimental::filesystem::v1::path>(char const (&) [6])':
/opt/scylladb/include/c++/7/experimental/bits/fs_path.h:198: undefined reference to `std::experimental::filesystem::v1::path::_M_split_cmpts()'
collect2: error: ld returned 1 exit status
gmake[1]: *** [cmTC_29ea1] Error 1
gmake[1]: Leaving directory `/tmp/tmp.yyGw1J1RRP/cmake-build-release-devsdksg/CMakeFiles/CMakeScratch/TryCompile-DLboHE'
gmake: *** [cmTC_29ea1/fast] Error 2
```

## 解决方案

### ninja-build 版本低

升级 ninja-build 版本，从 `1.7.2` 升级到 `1.11.1` 后问题解决。最新版，从[这里](https://github.com/ninja-build/ninja/releases)下载。