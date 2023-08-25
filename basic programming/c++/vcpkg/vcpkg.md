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

# 概念

- port
- version
- Registries
  - vcpkg 使用 registries 来管理 ports 和 versions
  - 参考
    - [创建 Registries](https://learn.microsoft.com/en-us/vcpkg/maintainers/registries)
    - [Registries 配置 (Manifest mode)](https://learn.microsoft.com/en-us/vcpkg/reference/vcpkg-configuration-json)
    - [示例 Registries](https://github.com/northwindtraders/vcpkg-registry)
- Triplet
  - 在 vcpkg 中，使用 triplets 来表示每个库的 **目标配置集合**

# 使用

## 引入 CMAKE_TOOLCHAINE_FILE

```shell
# 命令行
cmake ... -DCMAKE_TOOLCHAIN_FILE=/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake

# CMakeLists.txt 内
## NOTE: 要在 project 之前
set(CMAKE_TOOLCHAIN_FILE /path/to/vcpkg/scripts/buildsystems/vcpkg.cmake)
```



## 软件包搜索

- [Browse packages](https://vcpkg.io/en/packages)

## Manifest 模式

- [Manifest Mode](https://learn.microsoft.com/en-us/vcpkg/users/manifests)
- [Manifest mode: CMake example](https://learn.microsoft.com/en-us/vcpkg/examples/manifest-mode-cmake)

**示例**

```json
{
  "name": "cook-cpp",
  "version": "0.0.1",
  "dependencies": [
    "boost",
    "fmt",
    "spdlog"
  ],
  "overrides": [
    {
      "name": "boost",
      "version": "1.82.0"
    },
    {
      "name": "fmt",
      "version": "9.1.0"
    },
    {
      "name": "spdlog",
      "version": "1.11.0"
    }
  ],
  "builtin-baseline": "21bbb14c4113b89cd06402e852e075341722304f"
}
```

- buildin-baseline 
  - vcpkg 的 commit id
  - 如果要制定版本（使用 overrides），则必须设置该项

### 配置文件

- `vcpkg.json`
- `vcpkg-configuration.json`

## 添加内部库

- [参考一](https://zhuanlan.zhihu.com/p/642660026)

# Registries

## 获取 SHA512

```shell
vcpkg hash /path/to/source.tar.gz
```

## 获取 versions 的 git-tree

- 添加 `ports/<library>` 目录及配置（profile.cmake、vcpkg.json） 等 
- 提交 commit
- 使用如下命令获取 git-tree

```shell
git rev-parse HEAD:ports/<library>
```

## Patch

```shell
# 生成
git diff > patch
# 应用
git apply patch
```

**注意**

- **不要直接复制 patch 内容**，容易出现 `error: corrupt patch at line *` 的问题

# Trouble Shooting

## OUT_SOURCE_PATH

压缩包解压路径在 `{VCPKG_HOME}/buildtrees/{library}/src/ar-{version}-{whatever}.clean`

## 清除

```shell
rm -r {VCPKG_HOME}/buildtrees/{library}
rm -r {VCPKG_HOME}/packages/{library}
```

## `patch failed: error: corrupt patch at line`

- patch 文件过期，内容不对，需要重新生成 patch 文件
- 不可见字符问题
  - 不要直接拷贝 patch 内容，要复制 patch 文件
    - 复制粘贴有可能导致不可见字符变更
    - 部分 IDE 会自动优化不可见字符，导致 patch 文件失效

## pkg_check_modules 无法找到包

**错误信息**

```shell
-- Checking for module 'cassandra_static'
--   No package 'cassandra_static' found
CMake Error at /snap/cmake/1328/share/cmake-3.27/Modules/FindPkgConfig.cmake:607 (message):
  A required package was not found
```

**解决**

正常来说，vcpkg 安装的包，如果有 pkgconfig 是可以通过 pkg_check_modules 找到的。出现问题的原因是 find_package 引入包时意外导致 pkg_check_modules 不可用，解决方案有两个。

- 找到因为问题的 find_package 语句，并移到后面
- 遍历 CMAKE_PREFIX_PATH 并追加 `lib/pkgconfig` 后加入到 `ENV{PKG_CONFIG_PATH}` 中
