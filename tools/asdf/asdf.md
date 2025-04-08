---
title: asdf
categories: 
  - [工具,asdf]
tags:
  - asdf
date: 2025/04/8 00:00:00
---

# 安装

```shell
brew install asdf
```

# 插件

## 列出所有插件

```shell
asdf plugin list all
```

## 安装插件

步骤如下。

```shell
# 1. 先添加
asdf plugin add {plugin-name}
# 2. 再安装
asdf install {plugin-name} {plugin-version}
asdf install {plugin-name} latest # 安装最新版本
```

## 查看已安装

```shell
# 1. 查看已安装 plugins
asdf plugin list
```

## 版本

```shell
# 1. 查看已安装插件版本
asdf list {plugin-name}
# 2. 查看插件所有可用的版本
asdf list all {plugin-name}
# 3. 查看插件最新的版本
asdf latest {plugin-name}
# 4. 查看当前使用 asdf 管理的插件及版本
asdf current  # 列出所有
asdf current {plugin-name}
```

**设置插件版本**

```shell
asdf set {plugin-name} {plugin-version}     # 固化插件版本到当前文件夹
asdf set -u {plugin-name} {plugin-version}  # 固化插件版本到用户目录，对当前用户生效
asdf set -p {plugin-name} {plugin-version}  # 固化插件版本到当前文件夹的父级目录
```

**演示**

```shell
➜  tmp asdf set golang 1.20.4
➜  tmp asdf set -u golang 1.24.2   
➜  tmp go version            
go version go1.20.4 darwin/arm64
➜  tmp cd ..               
➜  ~ go version            
go version go1.24.2 darwin/arm64
# 验证 tmp 子目录下的 golang 版本
➜  ~ cd tmp
➜  tmp mkdir child     
➜  tmp cd child                                                                                                                 11GiB/16GiB 21:47:32 🍎 
➜  child go version                                                                                                             11GiB/16GiB 21:47:34 🍎 
go version go1.20.4 darwin/arm64
```

如果当前目录下的 `.tool-version` 文件内有指定的版本，那么在当前目录下运行时（包含子目录）会使用`.tool-version` 内的版本。