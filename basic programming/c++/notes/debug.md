---
title: c++ debug
categories: 
  - [coding, c++]
tags:
  - c++
date: "2021-03-11T00:00:00+08:00"
update: "2021-03-11T00:00:00+08:00"
---

# addr2line

```shell
addr2line -f -e path/to/binary <address>
```

# nm

列出对象文件中的符号

```shell
nm libssl.a 
nm -an libssl.a 
```

```shell
# 安装
$ yum install binutils
```

# ldd

```shell
$ ldd main
	linux-vdso.so.1 (0x00007ffe5458c000)
	libresolv.so.2 => /lib/x86_64-linux-gnu/libresolv.so.2 (0x00007f74d9d1a000)
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f74d9c33000)
	libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f74d9a07000)
	libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f74d99e7000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f74d97be000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f74dc649000)
```

# strings

strings 程序的主要功能是找出文件（包括文本文件、二进制文件等）内容中的可打印字符串。

```shell
strings /usr/lib/libstdc++.so.6 | grep GLIBCXX
```

