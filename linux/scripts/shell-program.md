---
title: shell 编程
categories: 
	- [linux, shell]
tags:
	- linux
	- shell
date: 2020/10/27 19:00:00
update: 2020/10/27 19:00:00
---

# 函数

```shell
echo() {
	echo "$1"
}

echo Hello
```

# 条件判断

```shell
[ ... ] : 
```

# 路径及文件

```shell
# 提取文件名
$(basename "/path/to/file")  # file

# 提取文件路径（非绝对路径）
$(dirname "/path/to/file")   # /path/to

# 获取绝对路径
$(pwd)/$(dirname "./path/to/file")
```

