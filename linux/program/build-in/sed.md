---
 title: sed
categories: 
	- [linux,程序]
tags:
	- sed
date: 2021/01/11 00:00:00
update: 2021/01/11 00:00:00
---

# 参数

`-E`

- 使用扩展语法
- 扩展语法和基础语法区别主要在于少量字符的差异，`?`、`+`、`()`、`{}`，在基础语法中需要转义来作为特殊字符；相反，在扩展语法中，需要转义以匹配无特殊含义的文本字符

# 示例

## 替换

```shell
$ cat msg
{
'localhost' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
}

# 替换文件内容并打印
$ sed '/localhost/p; s/localhost/dev.ops/' msg
{
'localhost' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
'dev.ops' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
}

# 替换文件内容并将输出重定向到新文件
$ sed '/localhost/p; s/localhost/dev.ops/' msg > new_msg
$ cat new_msg
{
'localhost' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
'dev.ops' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
}
# 源文件并未更改
$ cat msg
{
'localhost' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
}

# 在源文件修改并保存源文件至备份文件
$ sed -i 'msg_backup' '/localhost/p; s/localhost/dev.ops/' msg
$ ls
msg		msgmsg_backup	new_msg
# 打印源文件备份
$ cat msgmsg_backup
{
'localhost' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
}
# 打印源文件
$ cat msg
{
'localhost' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
'dev.ops' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
}

# 直接修改源文件并且不保存备份
$ sed -i '/localhost/p; s/localhost/dev.worker/' msgmsg_backup
# $ sed -i '' '/localhost/p; s/localhost/dev.worker/' msgmsg_backup	# os x
$ cat msgmsg_backup
{
'localhost' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
'dev.worker' => ['domain_name' => 'default', 'domain_type' => 'mobile'],
}

$ ls
msg		msgmsg_backup	new_msg

#### Other Examples
## 正则替换
$ cat script/config.sh
workers=6666
threads_compute=10
threads=101
$ sed -i "s/workers=[0-9]*/workers=9/" ./script/config.sh
$ cat script/config.sh
workers=9
threads_compute=10
threads=101
```

# 替换子串

```shell
sed -i 's/head/heap/g' Heap.cpp
# sed -i '' 's/head/heap/g' Heap.cpp	# 不保留文件备份
```

# 替换前复制行

```shell
sed '/localhost/p; s/localhost/dev.ops/' FILENAME
```

# group 替换

```shell
$ echo "hello wii." | sed -E 's/hello ([a-z]+).*/\1/'
wii
# OR
$ echo "hello wii." | sed 's/hello \([a-z]\+\).*/\1/'   # 注: 不同系统，+ 号的行为可能不一致，这条命令在 big sur (mac os) 中无法输出预想结果
wii
```

以上有个问题，如果为匹配到数据，最终打印原始数据，比如。

```shell
$ echo "hello wii." | sed -E 's/hi ([a-z]+).*/\1/'
hello wii.
```

`/patt/!d;s//repl/`可实现匹配不到打印空，如下。

```shell
$ echo "hello wii." | sed -E '/hi ([a-z]+).*/!d;s//\1/' 
# empty
```

# 问题

`sed: 1:  ... : extra characters at the end of H command`

- edit in place on OSX without keeping a backup, use `-i ''`:

  ```shell
  sed -i '' -e '/localhost/p; s/localhost/dev.ops/' FILENAME
  ```

# **参考**

- [Ref 1](https://unix.stackexchange.com/questions/112023/how-can-i-replace-a-string-in-a-files)