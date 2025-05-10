---
title: mac usage
categories: 
  - [linux, Mac]
tags:
  - usage
date: "2020-10-27T19:00:00+08:00"
update: "2020-10-27T19:00:00+08:00"
---

# 初始化

## homebrew

```shell
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## node

参见 `前端/node`。

# 工具

## homebrew

- 安装路径
  - `/usr/local/Cellar`
  - `/usr/local/Caskroom`

- 源
  - [清华源使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)

## commond line tools

```shell
# install
$ xcode-select --install

# delete
$ sudo rm -rf `xcode-select -p` # 一般会在文件夹 /Library/Developer/CommandLineTools 内

# Problems
## Can’t install the software because it is not currently available from the Software Update server.
# 手动下载
https://developer.apple.com/download/more/?=command%20line%20tools
```

# 问题

## 拷贝文件导致图标变灰无法访问

尝试 [这里](https://blog.csdn.net/evandeng2009/article/details/53242196) 无果。

```shell
# 仅适用文件夹
# 命令行输入如下内容
exitFun() {
  echo "ERROR: failed, due to $1"
  exit 1
}

fix() {
    [ ! -d "${1}" ] && exitFun "target is not folder"
    mv "${1}" "${1}_back"
    mkdir "${1}"
    mv "${1}_back"/* "${1}/"
    mv "${1}_back"/.[^.]* "${1}/"
    rmdir "${1}_back"
}

# 修复，输入 fix <文件夹目录> OR 输入 fix [拖拽文件夹至终端]
$ fix <path>	
```

