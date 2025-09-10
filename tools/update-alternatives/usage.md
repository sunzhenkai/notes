---
title: update-alternatives
categories: 
  - [工具,update-alternatives]
tags:
  - update-alternatives
date: "2020-12-30T00:00:00+08:00"
update: "2020-12-30T00:00:00+08:00"
---

# 安装

```shell
$ sudo pacman -S dpkg
```

# 使用

## `--slave`

在更新一个程序后，往往需要同步更改其他程序，比如修改 gcc 为 gcc11，则需要同步修改 g++、gcov 等，可以使用 slave 来实现。

```shell
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 110 --slave /usr/bin/g++ g++ /usr/bin/g++-11 --slave /usr/bin/gcov gcov /usr/bin/gcov-11 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-11 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-11
```

# 示例

```shell
# 添加一个 alt
#                                  链接创建路径 名称   实际文件路径     优先级
sudo update-alternatives --install /usr/bin/cc cc /usr/bin/gcc-4.9 10  
```

```shell
sudo update-alternatives --config cc  # 选择并设置默认版本
```

