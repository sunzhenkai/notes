---
title: linux usage
categories: 
	- [linux,notes]
tags:
	- Linux
date: 2020/12/21 9:40:00
update: 2020/12/21 9:40:00
---

# 按大小排序打印文件

```shell
$ ls -lSh   # -S: 按大小排序; -h: human readable
$ ls -lShr  # -r: 倒序
$ ls -lShrR # -R: 递归列出子文件夹
```

# 在特定文件内查找内容

**grep**

```shell
$ grep -inr --include pom.xml apollo . # i: 忽略大小写; r: 递归; n: 行号
```

**vim**

```shell
:vimgrep /apollo/g **/pom.xml 
```

# 递归查找特定文件[夹]

```shell
$ find . -name '\.idea'
```

**删除**

```shell
$ find . -name '\.idea' | xargs rm  -r
```

# 目录栈

`dirs` : 查看当前目录栈

- `-v` : 列出目录及其序号
- `-l` : 列出目录全名
- `-c` : 清空目录栈

`pushd` ：改变目录并将原目录压入栈

`popd` : 修改当前目录为栈顶目录并将栈顶目录出栈

```shell
$  ~ dirs
~
$  ~ pushd Downloads 
~/Downloads ~
$  Downloads dirs
~/Downloads ~
$  Downloads popd           
~
$  ~ dirs
~
```

