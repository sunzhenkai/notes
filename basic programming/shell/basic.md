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

# 特殊参数

```shell
$!  最后运行的后台线程 id
$?  最后运行的命令的结束码
$$  脚本本身进程 id

$#  参数个数
$@  参数列表. "$@" = "$1" "$2" "$3" "$..."
$*  参数列表. "$*" = "$1 $2 $3 ..." 
$0  脚本文件名
$1~$n  参数

# 参数列表截取
${*:2}  截取第二个参数及之后
${*:2:3}  截取第二、三个参数
```

# getopts

```shell
# opts
:前缀	忽略错误
:后缀	参数后必须有值

# example
:abc:de:	忽略参数错误，-c、-e后必须有值

while getopts ":ab:Bc:" opt; do
    case $opt in
        a) echo "found -a" ; a="ok" ;;
        b) echo "found -b and value is: $OPTARG" ;;
        *) "echo usage" ;;
    esac
done
```

# 函数

```shell
echo() {
	echo "$1"
}

echo Hello
```

# test

`test ` 命令通常被 `[...]` 替代

```shell
# [ ... ]
[ ... ] : 

# if ... else ...
if [ expression ]
then
	...
fi
```

**[] 和 [[]] 的区别**

- 兼容性

  - `[]` 是内置命令 test 的可选项，在 Linux、Unix、POSIX 系统兼容

  - `[[]]` 是 Korn Shell 作为增强功能引入的，被 base、zsh 等支持，但在 POSIX 系统中不兼容

- `[[]]` 于 `[]` 的差异

  - 比较运算符
    - 比如，`[[ 1 < 2 ]]`，等价于 `[ 1 \< 2 ]`
  - 布尔运算符（`-a -> &&`，`-o -> ||`）
    - 比如，`[[ 3 -eq 3 && 4 -eq 4 ]]` 等价于 `[ 3 -eq 3 -a 4 -eq 4 ]`
  - 组合表达式
    - 比如，`[[ 3 -eq 3 && (2 -eq 2 || 1 -eq 1) ]] ` 等价于 `[ 3 -eq 3 -a \( 2 -eq 2 -o 1 -eq 1 \) ]`
  - 模式匹配
    - 比如，`[[ $name = *c* ]]` ，`[]` 中没有对应的匹配运算
  - 正则匹配
    - 比如，`[ $name =~ ^Ali ]` ，`[]` 中没有对应的匹配运算
  - 单词切分（`[[]]` 不会对变量值按空白符切分，`[]` 对应得需要添加 `""` 来达到相似的效果）
    - 比如，`name = "Wukong Sun"`，`[[ $name ]]` 等价于 `[ "$name" ]`

## 参数

### 字符串

```shell
-n 不为空
-z 为空
{string1} = {string2} string1 和 string2 相同
{string1} != {string2} string1 和 string2 不相同
{string1} < {string2} 基于 ASCII 码比较
{string1} > {string2} 基于 ASCII 码比较
```

**正则匹配**

```shell
"{data}" =~ ^{regex}$

# 示例
[[ "$date" =~ ^[0-9]{8}$ ]] && echo "YES"
```

### 变量

```shell
-v 变量是否 set
```

### 数字比较

```shell
{number1} -eq/-ne/-lt/-le/-gt/-ge {number2}
{number1} -eq {number2} 相等
{number1} -ne {number2} 不相等
{number1} -lt {number2} 小于
{number1} -le {number2} 小于等于
{number1} -gt {number2} 大于
{number1} -ge {number2} 大于等于
```

### 文件

```shell
-a/-e 文件是否存在
-b 文件存储在块存储设备
-d 是否是文件夹
-f 文件存在且是常规文件
-h/-L 文件是符号链接
-p 文件是否是使用 mkfifo 创建的命名管道
-r 是否可读（运行命令的用户）
-s 文件存在且不为空
-S 是否是 Socket 文件
-t fd (file descriptor) 是否在终端中打开
-w 是否可写（运行命令的用户）
-x 是否可执行（运行命令的用户）
-O 运行命令的用户是否是文件 Owner
-G 文件是否被运行命令的用户 Group 拥有
{file1} -nt {file2} file1 是否比 file2 更新
{file1} -nt {file2} file1 是否比 file2 更旧
{file1} -ef {file2} file1 是否是 file2 的硬链接
```

### 多表达式

```shell
{expr1} -o {expr2} 或
{expr1} -a {expr2} 且
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

## 比较

```shell
[ "$v" = "value" ]
```

## 截取

```shell
$ s=abcd
# 截取区间是 [left, right]
$ echo ${s:1}
bcd
$ echo ${s:1:2}
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
$ for id in {1..3}; echo $id   # 1 2 3

# 脚本
for id in {1..3}; do
	echo $id
done

# seq [首数] [增量] 尾数
$ seq 1 3 # [1, 3]
$ seq 3   # [1, 3]
$ seq 1 2 5 # 1, 3, 5

$ for i in `seq 3`; do echo $i; done  # 1 2 3
```

# case...esac

```shell
word=a
case $word in
	a)
		echo "a $word"
		;;
	b)
		echo "b $word"
		;;
	*)
		echo "* $word"
		;;
esac
```

# getopts

**参数**

```shell
# opts
:前缀	忽略错误
:后缀	参数后必须有值

# example
:abc:de:	忽略参数错误，-c、-e后必须有值
```

**示例**

```shell
usage() {
    cat <<EOF
Usage: $0 [-a] [-b name] msg
EOF
}

while getopts ":ab:Bc:" opt; do
    case $opt in
        a) echo "found -a" ; a="hello" ;;
        b) echo "found -b and value is: $OPTARG" ;;
        c) echo "found -c and value is: $OPTARG" ;;
        *) usage ;;
    esac
done

shift $(($OPTIND - 1))
```

