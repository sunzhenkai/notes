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

[toc]

# 函数

```shell
echo() {
	echo "$1"
}

echo Hello
```

# 条件判断

```shell
# [ ... ]
[ ... ] : 

# if ... else ...
if [ expression ]
then
	...
fi
```

# 路径及文件

```shell
# 提取文件名
$(basename "/path/to/file")  # file

# 提取文件路径（非绝对路径）
$(dirname "/path/to/file")   # /path/to

# 获取绝对路径
$(pwd)/$(dirname "./path/to/file")

# 脚本路径
BASE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
```

# 数组

```shell
# 定义数组
ARR=(a b c)

# ARR[@]: 数组转换为字符串
echo "${ARR[@]}"
a b c

# ARR[*]
echo "${ARR[*]}"
a b c

# 数组赋值
ANOTHER=("${ARR[@]}") 

# 长度
echo ${#ARR[@]}
3

# 序号
for idx in "${!ARR[@]}"; do
  echo "$idx"
done
```

**[@] VS [*]**

数组的 `[@]` 和 `[*]` 都是取所有元素，但是有所差别。

```shell
# 定义
$ ARR=(a b c)
$ A=("${ARR[@]}")  
$ B=("${ARR[*]}") 

# A
$ echo ${#A[@]} 
3
$ echo ${A[@]} 
a b c

# B
$ echo ${#B[@]}
1
$ echo ${B[@]} 
a b c
```

# 布尔

```shell
FLAG=true
if [[ $FLAG == true ]]; then
	# do something
fi
```

# 字符串

```shell
[ "$v" = "value" ]
```

# 循环

## 数组

```shell
# 命令行
$ countries=(china us); for country in ${countries[@]}; echo $country
china
us

# 脚本
countries=(china us)
for country in ${countries[@]}; do
	echo $country
done
```

## 范围

```shell
$ for id in {1..3}; echo $id
1
2
3

# 脚本
for id in {1..3}; do
	echo $id
done
```

