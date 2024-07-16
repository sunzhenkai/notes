---
title: vcpkg - 自定义仓库
categories: 
  - [coding, c++, tools, vcpkg]
tags:
  - c++
    - vcpkg
date: 2024/04/22 00:00:00
---

# 使用步骤

- 安装 VCPKG，或更新至最新 VCPKG
- 创建项目，并使用 vcpkg 管理依赖
- 使用 vcpkg 打包项目（overlay port）
- 将项目添加到 Registry

# 安装 VCPKG

```shell
# 下载
$ git clone https://github.com/microsoft/vcpkg.git
# 执行依赖检查、下载 vcpkg 可执行文件
$ cd vcpkg && bootstrap-vcpkg.bat
```

设置环境变量。

```shell
export VCPKG_ROOT="/path/to/vcpkg"
export PATH=$VCPKG_ROOT:$PATH
```

# 更新 VCPKG

```shell
$ cd $VCPKG_ROOT
$ git pull
$ chmod a+x bootstrap-vcpkg.sh
$ ./bootstrap-vcpkg.sh
```

# 创建项目

## 编写工程代码

编写工程源码，以及 `CMakeLists.txt` 文件。

## 创建 manifest 文件 `vcpkg.json` 和 `vcpkg-configuration.json`

```shell
$ vcpkg new --application
```

添加 Git Registry 到 `vcpkg-configuration.json`

```shell
{
  ...
  "registries": [
    {
      "kind": "git",
      "repository": "https://github.com/Microsoft/vcpkg",
      "baseline": "42bb0d9e8d4cf33485afb9ee2229150f79f61a1f",
      "packages": "*"
    }
  ]
}
# or
{
  ...
  "registries": [
    {
      "kind": "git",
      "repository": "https://github.com/Microsoft/vcpkg",
      "baseline": "42bb0d9e8d4cf33485afb9ee2229150f79f61a1f",
      "reference": "master",
      "packages": [
      	"fmt",
      	"spdlog"
      ]
    }
  ]
}
```

- `reference` 是可选项，如果你的 commit id 不在默认分支，则必须使用 `reference` 指定对应的分支，否则会报 `failed to unpack tree object` 错

## 添加依赖包

```shell
$ vcpkg add port fmt
```

## 构建和运行

### 创建 CMakePresets.json

在项目中创建 `CMakePresets.json` 文件。

```shell
{
  "version": 2,
  "configurePresets": [
    {
      "name": "default",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/vcpkg-build",
      "cacheVariables": {
        "CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
      }
    }
  ]
}
```

文件包含一个为 CMake 配置的 `default` 预定配置（Preset），设置 CMAKE_TOOLCHAIN_FILE 变量，允许 CMake 识别 vcpkg 提供的 C++ 库。

### 运行 CMake configuration

```shell
$ cmake --preset=default # 指定预设
```

### 构建工程

```shell
$ cmake --build vcpkg-build
```

# 使用 vcpkg 打包库

## 设置自定义 overlay

在项目目录下，创建 `{project}-vcpkg-custome-overlay`。

```shell
$ mkdir {project}-vcpkg-custome-overlay
```

## 设置 Port 相关文件

### `vcpkg.json`

```shell
$ cd {project}-vcpkg-custome-overlay
$ mkdir {project}-vcpkg-custome-overlay/{project}-library
```

创建 port 的 `vcpkg.json` 配置。

```shell
$ touch {project}-vcpkg-custome-overlay/{project}-library/vcpkg.json
```

```json
{
  "name": "{project}-library",
  "version": "1.0.0",
  "homepage": "https://project.com/home",
  "description": "project description",
  "license": "MIT",
  "dependencies": [
    {
      "name" : "vcpkg-cmake",
      "host" : true
    },
    {
      "name" : "vcpkg-cmake-config",
      "host" : true
    },
    "{other-packages}"
  ]
}
```

关于 `vcpkg.json` 更多的说明，参考[这里](https://learn.microsoft.com/en-us/vcpkg/reference/vcpkg-json)。

### `usage`

创建 usage 文件。

```shell
$ touch {project}-vcpkg-custome-overlay/{project}-library/usage
```

```shell
{project}-library provides CMake targets:

find_package({project}_lib CONFIG REQUIRED)
target_link_libraries(main PRIVATE {project}::{project})
```

关于 usage 文件的更多说明，参考 [这里](https://learn.microsoft.com/en-us/vcpkg/maintainers/handling-usage-files)。

### `portfile.cmake`

```shell
$ touch {project}-vcpkg-custome-overlay/{project}-library/portfile.cmake
```

```shell
vcpkg_check_linkage(ONLY_STATIC_LIBRARY)

vcpkg_from_github(
    OUT_SOURCE_PATH SOURCE_PATH
    REPO {user}/{project}
    REF "${VERSION}"
    SHA512 0  # This is a temporary value. We will modify this value in the next section.
    HEAD_REF {project}-lib
)


vcpkg_cmake_configure(
    SOURCE_PATH "${SOURCE_PATH}"
)

vcpkg_cmake_install()

vcpkg_cmake_config_fixup(PACKAGE_NAME "{project}_lib")

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

file(INSTALL "${SOURCE_PATH}/LICENSE" DESTINATION "${CURRENT_PACKAGES_DIR}/share/${PORT}" RENAME copyright)
configure_file("${CMAKE_CURRENT_LIST_DIR}/usage" "${CURRENT_PACKAGES_DIR}/share/${PORT}/usage" COPYONLY)
```

关于 `portfile.cmake` 文件的详细说明，参考[这里](https://learn.microsoft.com/en-us/vcpkg/contributing/maintainer-guide)。

附，从 gitlab 下载。

```cmake
vcpkg_from_git(
        OUT_SOURCE_PATH SOURCE_PATH
        URL git@gitlab.compony.com:group/repo.git
        REF {commit-id} # 必须是 commit id
        HEAD_REF main
)
```

#### 更新 `portfile.cmake` 的 SHA512 

第一次运行 `vcpkg install ...` 获取 SHA512。

```shell
$ vcpkg install {project}-library --overlay-ports=/path/to/{project}-vcpkg-custom-overlay
```

在输出中找到如下内容。

```shell
Expected hash: 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
Actual hash: 4202125968a01219deeee14b81e1d476dab18d968425ba36d640816b0b3db6168f8ccf4120ba20526e9930c8c7294e64d43900ad2aef9d5f28175210d0c3a417
```

拷贝 "Actual hash" 的值，覆盖 `portfile.cmake` 的 `SHA512` 的值。

#### 添加编译选项（definitions）

```cmake
vcpkg_cmake_configure(
        SOURCE_PATH "${SOURCE_PATH}"
        OPTIONS -D...=... -D...=... ...
)
```

## 打包安装库

再次运行 `vcpkg install ...`。

```shell
$ vcpkg install {project}-library --overlay-ports=/path/to/{project}-vcpkg-custom-overlay
```

**注意** 依赖要在 `{project}-vcpkg-custom-overlay/vcpkg.json` 中添加，比如。

```json
{
  ...
  "dependencies": [
    {
      "name": "vcpkg-cmake",
      "host": true
    },
    {
      "name": "vcpkg-cmake-config",
      "host": true
    },
    "protobuf"
  ]
}
```

### 再次运行

```shell
$ vcpkg remove {project}-library # 先移除再重新安装
```

## 验证 Port Build

### 修改代码

复用或新建工程，修改如下内容。

```shell
# file: {project}/vcpkg.json
{
    "dependencies": [
        "...",
        "{project}-library"
    ]
}
```

```shell
# file: {project}/vcpkg-configuration.json
{
  "default-registry": {
  	...
  },
  "registries": [
    ...
  ],
  "overlay-ports": [
    "/path/to/{project}-vcpkg-custom-overlay"
  ]
}
```

修改 `CMakeLists.txt`，添加库依赖。

```cmake
...
find_package({project}_lib CONFIG REQUIRED)  # Add this line
add_executable({project} main.cpp)
target_link_libraries({project} PRIVATE {project}_lib::{project}_lib)  # Add this line
```

### 配置（Configuration）

```shell
$ cmake --preset=default # 需预先配置 CMakePresets.json, 见上文
```

### 构建（Build）

```shell
$ cmake --build vcpkg-build
```

### 运行

```shell
$ ./vcpkg-build/{project}
```

# 创建 Git Registry

```shell
$ mkdir ports
$ mkdir versions
$ vim versions/baseline.json
{
  "default": {}
}
```



# 向 Repository 添加 Port

[完整示例](https://github.com/northwindtraders/vcpkg-registry)，新增依赖库需要修改 / 新增如下文件。

```shell
ports
  - {port-name}
    - portfile.cmake
    - vcpkg.json
versions
  - {port-name-first-char}-
    - {port-name}.json
  - baseline.json
```

没个仓库都会有 `versions/baseline.json` 文件，包含在一个特定  commit 的一系列 Ports 的最新版本。

## 拷贝 Overlay Port 到 Repository（Registry）

拷贝 Overlay Port 到 Repository 的 `ports` 目录。

```shell
xcopy <path/to/{project}-library> <ports/{project}-library> /E
```

## Commit 

注意，Ports 和 Version 不能同时添加。

### Commit Ports

```shell
$ git add ports/<{project}-library>
$ git commit -m '...'
```

### Commit Version

```shell
# 更新版本
$ vcpkg --x-builtin-ports-root=./ports --x-builtin-registry-versions-dir=./versions x-add-version --all --verbose --overwrite-version
$ git commit -m '...version'

# 查看帮助
$ vcpkg x-add-version --help

# 跳过格式检查
--skip-formatting-check
--skip-version-format-check

# 格式化
vcpkg format-manifest /path/to/vcpkg.json

# 注: 下面代码仅适用于更新微软 open-source ports，且将 ports 复制到 $VCPKG_ROOT/ports 下
# $ vcpkg x-add-version vcpkg-sample-library
```

# 更新 Registry 中已经存在的库版本

- 从 Registry 拷贝 `ports/{library}` 到 Custome Overlay 目录
- 更新版本、`portfile.cmake`，再走一遍添加 Port 到 Registry 的流程

# 创建 Port

## 创建 Helper Ports / Script Ports

Helper Ports / Script Ports 类似于 `vcpkg-cmake` ，暴露函数以便在构建阶段使用。文档见这里 [Author helper ports](https://learn.microsoft.com/en-us/vcpkg/maintainers/authoring-script-ports)，[Port 集成](https://github.com/microsoft/vcpkg/tree/master/ports/vcpkg-cmake)。gs

# 附录

- [基于 vcpkg 安装和使用包](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started?pivots=shell-cmd)
- [使用 vcpkg 打包库](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started-packaging?pivots=shell-cmd)

# Trubleshooting

## `debug/share` 目录不存在

### 原因

没有文件写入到 share 目录（license 文件拷贝貌似不在 debug 拷贝）。

通常，依赖库在 install 时指定 export target，并 install(export target ...)，会生成对应库的 `{lib}Config.cmake` ，并拷贝到 share 目录下，示例如下。

```cmake
install(TARGETS {lib}
        EXPORT {lib}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib)
install(EXPORT {lib} DESTINATION share/{lib} FILE {lib}Config.cmake)
```

### 修复

方案一，手动创建目录，在 portfile.cmake 中添加。

```shell
file(MAKE_DIRECTORY ${CURRENT_PACKAGES_DIR}/debug/share/{lib})
```

方案二，依赖库添加 install export

方案三，依赖库添加 install pkgconfig file

## failed to unpack tree object

```shell
-- Running vcpkg install
Fetching registry information from https://github.com/sunzhenkai/vcpkg-example-registry (master)...
error: failed to execute: /usr/bin/git --git-dir=/home/wii/.cache/vcpkg/registries/git/.git --work-tree=/home/wii/.cache/vcpkg/registries/git-trees/68d1cfd34c43686c9f60c0d0f780525f29bb046f_3332708.tmp -c core.autocrlf=false read-tree -m -u 68d1cfd34c43686c9f60c0d0f780525f29bb046f
error: git failed with exit code: (128).
fatal: failed to unpack tree object 68d1cfd34c43686c9f60c0d0f780525f29bb046f
```

**原因**

git registry 中依赖库的 `versions/{x}-/{port}.json` 里面的 `git-tree` 值，是在非默认分支打的，默认克隆 HEAD，或者指定的是默认分支，导致 check out 不出来对应的数据。

**解决办法**

需要更新 Git Registry 中 port 版本的 git-tree 数据，命令如下。

```shell
vcpkg --x-builtin-ports-root=./ports --x-builtin-registry-versions-dir=./versions x-add-version --all --verbose --overwrite-version
```

## 多编译器

如果系统安装多个版本的 gcc/g++，想使用特定的编译器，可以通过下面命令指定。也可用来解决，多个编译器版本时，不同依赖库使用不同编译器的问题（会有查找编译器程序的差异）。

```shell
export CC=/path/to/gcc
export CXX=/path/to/g++
```

# CMake 工程测试

```shell
$ mkdir build
$ cd build
$ cmake ..
$ make -j
$ cmake --install . --prefix="$PWD"  # 安装到当前目录
```

- [创建私有仓库](https://learn.microsoft.com/en-us/vcpkg/maintainers/registries)
- [添加仓库到 Git 仓库](https://learn.microsoft.com/en-us/vcpkg/produce/publish-to-a-git-registry)
- [完整示例](https://github.com/sunzhenkai/vcpkg-full-example)
