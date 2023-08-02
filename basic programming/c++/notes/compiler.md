---
title: c++ compiler
categories: 
  - [coding, c++]
tags:
  - c++
date: 2022/06/13 00:00:00
---

# 编译选项

```shell
# warning
-Wall			开启警告（all: 应该开启的最小警告集合）
-Wextra		开启扩展警告
-Werror 	所有警告视为错误
-Wno-error=...	关闭某项警告视为错误
-Wno-<...>			关闭某项警告视为错误
```

# 附录

## `-Wall`

```shell
-Waddress -Warray-bounds (only with -O2) -Wc++0x-compat -Wchar-subscripts
-Wenum-compare (in C/Objc; this is on by default in C++) -Wimplicit-int (C and
 Objective-C only) -Wimplicit-function-declaration (C and Objective-C only) 
-Wcomment -Wformat -Wmain (only for C/ObjC and unless -ffreestanding) 
-Wmissing-braces -Wnonnull -Wparentheses -Wpointer-sign -Wreorder -Wreturn-type 
-Wsequence-point -Wsign-compare (only in C++) -Wstrict-aliasing 
-Wstrict-overflow=1 -Wswitch -Wtrigraphs -Wuninitialized -Wunknown-pragmas 
-Wunused-function -Wunused-label -Wunused-value -Wunused-variable 
-Wvolatile-register-var
```

## `-Wextra`

```shell
-Wclobbered -Wempty-body -Wignored-qualifiers -Wmissing-field-initializers
-Wmissing-parameter-type (C only) -Wold-style-declaration (C only) -Woverride-init
-Wsign-compare -Wtype-limits -Wuninitialized -Wunused-parameter (only with -Wunused
 or -Wall) -Wunused-but-set-parameter (only with -Wunused or -Wall)
```

## warn 示例配置

```shell
-Wall -Wextra -Waggregate-return -Wcast-align -Wcast-qual -Wdisabled-optimization -Wdiv-by-zero -Wendif-labels -Wformat-extra-args -Wformat-nonliteral -Wformat-security -Wformat-y2k -Wimplicit -Wimport -Winit-self -Winline -Winvalid-pch -Wjump-misses-init -Wlogical-op -Werror=missing-braces -Wmissing-declarations -Wno-missing-format-attribute -Wmissing-include-dirs -Wmultichar -Wpacked -Wpointer-arith -Wreturn-type -Wsequence-point -Wsign-compare -Wstrict-aliasing -Wstrict-aliasing=2 -Wswitch -Wswitch-default -Werror=undef -Wno-unused -Wvariadic-macros -Wwrite-strings -Wc++-compat -Werror=declaration-after-statement -Werror=implicit-function-declaration -Wmissing-prototypes -Werror=nested-externs -Werror=old-style-definition -Werror=strict-prototypes
```

