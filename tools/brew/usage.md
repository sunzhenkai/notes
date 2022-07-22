---
title: brew
categories: 
	- [工具,brew]
tags:
	- brew
date: 2021/08/06 00:00:00
update: 2021/08/06 00:00:00
---

# 安装卸载

**安装**

使用清华开源站仓库安装参考[这里](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)。

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**卸载**

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

# 初始化

```shell
brew tap homebrew/cask-versions
```

# 软件

## jdk

```shell
brew install adoptopenjdk8
brew install adoptopenjdk   # 最新 jdk
```

管理多个版本 jdk 参考[这里](https://stackoverflow.com/questions/26252591/mac-os-x-and-multiple-java-versions)。

```shell
# 安装 jenv
brew install jenv
# 配置 jenv
echo 'eval "$(jenv init -)"' >> ~/.bash_profile
# 添加需要管理的的 jdk
jenv add /Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home
```

