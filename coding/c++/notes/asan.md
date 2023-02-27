---
title: c++ - debug, asan
categories: 
	- [coding, c++]
tags:
	- c++
date: 2020/11/10 21:00:00
---

# 使用

## 编译选项

```shell
-fsanitize=address						# 开启内存越界检测
-fsanitize-recover=address		# 内存出错后继续运行, 需配合运行选项 halt_on_error=0
-fno-stack-protector 					# 去使能栈溢出保护
-fno-omit-frame-pointer 			# 去使能栈溢出保护
-fno-var-tracking 						# 默认选项为-fvar-tracking，会导致运行非常慢
-g1														# 表示最小调试信息，通常debug版本用-g即-g2
```

**示例**

```shell
ASAN_CFLAGS += -fsanitize=address -fsanitize-recover=address
ASAN_CFLAGS += -fno-stack-protector -fno-omit-frame-pointer -fno-var-tracking -g1
```

## 链接选项

```shell
ASAN_LDFLAGS += -fsanitize=address -g1 # 如果使用gcc链接，此处可忽略
```

## 运行选项

ASAN_OPTIONS是Address-Sanitizier的运行选项环境变量。

```shell
halt_on_error=0 					# 检测内存错误后继续运行
detect_leaks=1 						# 使能内存泄露检测
malloc_context_size=15 		# 内存错误发生时，显示的调用栈层数为15
log_path=/tmp/asan.log 		# 内存检查问题日志存放文件路径
suppressions=$SUPP_FILE		# 屏蔽打印某些内存错误
```

**示例**

```shell
export ASAN_OPTIONS=halt_on_error=0:use_sigaltstack=0:detect_leaks=1:malloc_context_size=15:log_path=/tmp/asan.log:suppressions=$SUPP_FILE
```

