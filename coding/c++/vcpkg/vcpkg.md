---
title: vcpkg
categories: 
	- [coding, c++, tools, vcpkg]
tags:
	- c++
    - vcpkg
date: 2023/07/19 00:00:00
---

# 安装

[参考](https://vcpkg.io/en/getting-started)

**安装依赖**

```shell
# arch
$ sudo pacman -S curl zip unzip tar cmake ninja
```

**安装 vcpkg**

```shell
$ git clone https://github.com/Microsoft/vcpkg.git
$ ./vcpkg/bootstrap-vcpkg.sh
```

# 使用

## 软件包搜索

- [Browse packages](https://vcpkg.io/en/packages)

## Manifest 模式

- [Manifest Mode](https://learn.microsoft.com/en-us/vcpkg/users/manifests)
- [Manifest mode: CMake example](https://learn.microsoft.com/en-us/vcpkg/examples/manifest-mode-cmake)

