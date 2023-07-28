---
title: brpc
categories: 
	- [coding, c++, library]
tags:
	- c++
	- brpc
date: 2021/01/06 21:00:00
---

# 编译

```shell
$ bash config_brpc.sh --headers="/path/to/deps/include/" --libs="/path/to/deps/lib/" --with-glog --with-thrift
$ make -j ${make_thread_num}
$ cp -a output/include/* "/path/to/install/include/"
$ cp -a output/lib/* "/path/to/install/lib/"
$ cp -a output/bin/* "/path/to/install/lib/"
```

# 问题

## NO 1

**描述**

```
ERROR: something wrong with flag 'flagfile' in file '/home/wii/Git/cooking/c++/universal/third/build/gflags-2.2.2/src/gflags.cc'.  One possibility: file '/home/wii/Git/cooking/c++/universal/third/build/gflags-2.2.2/src/gflags.cc' is being linked both statically and dynamically into this executable.

或者

Ignoring RegisterValidateFunction() for flag pointer 0x7f3d0b54893c: no flag found at that address
...
```

**解决**

gflags静态库和共享库同时存在导致。gflags 是选择手动编译，在编译时为cmake指定`-DBUILD_SHARED_LIBS=1`只编译共享库，如果是使用命令安装，可以尝试先移除`/usr/local/lib/libgflag.a` 和 `/usr/local/lib/libgflag_nothread.a`。

