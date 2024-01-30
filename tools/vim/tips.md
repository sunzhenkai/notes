---
title: vim tips
categories: 
  - [工具,vim]
tags:
  - vim
date: 2020/12/30 19:00:00
update: 2020/12/30 19:00:00
---

[toc]

# Common

```shell
# 命令
;  			重复上一个动作
:!! 		重复上一条命令
:shell	运行shell

# 复制粘贴
## 复制一个当前单次
byw    b: 到单次首; y: yank; w: for word
## command mode 粘贴内容
C-r"  ": default register

# 查找
## 文件内查找
/{pattern}
## 跨文件查找:q
:vimgrep /{pattern}/g [file]    # :vimgrep /foobar/g **
:cn[f]    下一个匹配[文件]
:cp[f]    上一个匹配[文件]
:cr/cla   回到开始/结束
:copen    打开匹配列表

## 统计有多少匹配
:%s/{pattern}//gn
```

## 编辑

```shell
i  从光标位置输入
```

## 窗口

```shell
:tabnew			新建窗口
g t         下一个窗口
g T         上一个窗口

# 调整高度
:resize/res 60/+5/-5	调整窗口高度 
# 宽度
:vertical resize 80
```

# 插件

## NERDTree

### 目录

```shell
# 目录
## NERDTree
r     刷新光标所在的目录
C     将根路径设置为光标所在的目录
u     设置上级目录为根路径
cd    设置当前工作路径
m     文件操作：复制、删除、移动等
P     大写，跳转到当前根路径
p     小写，跳转到光标所在的上一级路径
x     收起当前打开的目录
X     收起所有打开的目录
```

### 打开文件

```shell
o       在已有窗口中打开文件、目录或书签，并跳到该窗口
go      在已有窗口 中打开文件、目录或书签，但不跳到该窗口
t       在新 Tab 中打开选中文件/书签，并跳到新 Tab
T       在新 Tab 中打开选中文件/书签，但不跳到新 Tab
i       split 一个新窗口打开选中文件，并跳到该窗口
gi      split 一个新窗口打开选中文件，但不跳到该窗口
s       vsplit 一个新窗口打开选中文件，并跳到该窗口
gs      vsplit 一个新 窗口打开选中文件，但不跳到该窗口
```

# 行内移动

```shell
h	 左移一位
l	 右移一位
0	 行首
$  行尾
^  当前行的第一个非空白符位置
fx 移动当当前行的下一个x处
Fx 移动当当前行的上一个x处
tx 移动到x的左边一个位置
w  往后移动一个词
b  往前移动一个词
)  移动到下一个句子
(  移动到上一个句子
```

# 文件内移动

```shell
<C-F>  向下移动一屏
<C-B>  向上移动一屏
G      移动到文件末尾
nG     移动到第n行
gg     文件首
H      移动光标到屏幕上部
M      移动光标到屏幕中部
L      移动光标到屏幕底部
*      移动到光标所在字符串的下个位置
#      移动到光标所在字符串的上个位置
/s     向后搜索字符串s
?s     向前搜索字符串s
ma     打标签，标签名为a
`a     跳转到标签a
`.     跳转到上次编辑的地方
```

# Commands

```shell
# run shell commands
## 1
C-z			vim 后台运行
fg 			调回vim

## 2
:!<cmd>
```

# 查找替换

```shell
# 搜索
[ESC]
/word
n: next; N: previous

# 替换
:%s/foo/bar/g
:5,10s/foo/bar/gc   # with confirm
```

# 多行注释

**注释**

```shell
Esc
Ctrl + v
Shift + i (I)
# select multi lines
# input comments
Esc
```

**取消注释**

```shell
Esc
Ctrl + v
# select 
d / x
```

