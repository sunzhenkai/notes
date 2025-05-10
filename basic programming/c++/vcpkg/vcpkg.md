---
title: vcpkg
categories: 
  - [coding, c++, tools, vcpkg]
tags:
  - c++
    - vcpkg
date: "2023-07-19T00:00:00+08:00"
---

# 使用模式

## 项目使用 vcpkg 解决依赖问题

参考[这里](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started?pivots=shell-cmd)。

## 项目作为 port 供其他项目使用

- 首先 [打包应用](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started-packaging?pivots=shell-cmd)
- 将应用添加到 registry

## 创建内部 registry 供组织内使用

- [创建内部 registry](https://learn.microsoft.com/en-us/vcpkg/maintainers/registries)

## 添加 port 到内部 registry

- [为内部 registry 添加 ports 并更新版本数据库](https://learn.microsoft.com/en-us/vcpkg/produce/publish-to-a-git-registry)

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

## vcpkg-configuration.json

### example

```shell
{
  "$schema": "https://raw.githubusercontent.com/microsoft/vcpkg-tool/main/docs/vcpkg-configuration.schema.json",
  "default-registry": {
    "kind": "git",
    "repository": "https://internal/mirror/of/github.com/Microsoft/vcpkg",
    "baseline": "eefee7408133f3a0fef711ef9c6a3677b7e06fd7"
  },
  "registries": [
    {
      "kind": "git",
      "repository": "https://github.com/northwindtraders/vcpkg-registry",
      "baseline": "dacf4de488094a384ca2c202b923ccc097956e0c",
      "packages": [ "beicode", "beison" ]
    }
  ],
  "overlay-ports": [
    "./team-ports",
    "./custom-ports"
   ],
  "overlay-triplets": [ "./my-triplets" ]
}
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

## 项目使用 vcpkg

[官方文档](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started?pivots=shell-cmd)

## Makefile 工程

```cmake
set(MAKE_OPTS "")
if(VCPKG_LIBRARY_LINKAGE STREQUAL "static")
    list(APPEND MAKE_OPTS "STATIC=1")
else()
    list(APPEND MAKE_OPTS "SHARED=1")
endif()
```

```shell
# Configure
# 1. 如果没有 configure.ac 等自动化配置，需要 SKIP_CONFIGURE，且 COPY_SOURCE
# vcpkg_configure_make(SOURCE_PATH "${SOURCE_PATH}" OPTIONS ${MAKE_OPTS} COPY_SOURCE SKIP_CONFIGURE)
vcpkg_configure_make(SOURCE_PATH "${SOURCE_PATH}" OPTIONS ${MAKE_OPTS})
vcpkg_build_make()
vcpkg_fixup_pkgconfig()
```

## 自定义克隆

```cmake
set(GIT_REF 7.0.3)
set(GIT_URL https://github.com/aerospike/aerospike-client-c.git)

# custome clone git repo
set(SOURCE_PATH ${CURRENT_BUILDTREES_DIR}/${GIT_REF})
file(MAKE_DIRECTORY ${SOURCE_PATH})
if (NOT EXISTS "${SOURCE_PATH}/.git")
    message(STATUS "Cloning")
    vcpkg_execute_required_process(
            COMMAND ${GIT} clone ${GIT_URL} ${SOURCE_PATH}
            WORKING_DIRECTORY ${SOURCE_PATH}
            LOGNAME clone
    )
endif ()

message(STATUS "Checkout revision ${GIT_REF}")
vcpkg_execute_required_process(
        COMMAND ${GIT} checkout ${GIT_REF}
        WORKING_DIRECTORY ${SOURCE_PATH}
        LOGNAME checkout
)

message(STATUS "Fetching submodules")
vcpkg_execute_required_process(
        COMMAND ${GIT} submodule update --init
        WORKING_DIRECTORY ${SOURCE_PATH}
        LOGNAME submodule
)
```

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

# 引入包

## cmake targets

通过 CMake Targets 引入目标，适用于基于 CMake 编译的库，且导出目标配置文件（`{target}Config.cmake`）。

```cmake
find_package(target CONFIG REQUIRED)
target_link_libraries(main PRIVATE target)
```

## find_library

针对未提供 CMake 和 PkgConfig 引入方式的库，可使用此方法。

```cmake
find_library(TargetVar NAMES target REQUIRED)
target_link_libraries(main PRIVATE ${TargetVar})
```

示例。

```cmake
find_library(PolarisApi NAMES libpolaris_api.a REQUIRED)
target_link_libraries(main ${PolarisApi})
```

## pkgconfig

```cmake
include(FindPkgConfig)
pkg_check_modules(target REQUIRED IMPORTED_TARGET target)
target_link_libraries(main PRIVATE PkgConfig::brpc)
```

thrift 示例。

```cmake
find_package(PkgConfig REQUIRED)
find_package(Thrift CONFIG)
if(NOT TARGET thrift::thrift)
    pkg_search_module(THRIFT REQUIRED IMPORTED_TARGET GLOBAL thrift)
    add_library(thrift::thrift ALIAS PkgConfig::THRIFT)
endif()
```

# Trouble Shooting

## OUT_SOURCE_PATH

压缩包解压路径在 `{VCPKG_HOME}/buildtrees/{library}/src/ar-{version}-{whatever}.clean`

## 清除安装的包

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

- 找到出现问题的 find_package 语句，并移到后面
- 遍历 CMAKE_PREFIX_PATH 并追加 `lib/pkgconfig` 后加入到 `ENV{PKG_CONFIG_PATH}` 中

或者设置如下内容。

```cmake
set(PKG_CONFIG_USE_CMAKE_PREFIX_PATH TRUE)
```

以 tcmalloc 为例。

```cmake
set(PKG_CONFIG_USE_CMAKE_PREFIX_PATH TRUE)
include(FindPkgConfig)
pkg_check_modules(gperftools REQUIRED IMPORTED_TARGET GLOBAL libtcmalloc)
```

## Boost

### head only library

`vcpkg.json`

```json
{
    "name": "feature-generator-server",
    "version": "0.0.1",
    "dependencies": [
        "boost-core",
        "boost-stacktrace",
        "boost-pfr",
        "boost-..."
    ]
}
```

`CMakeLists.txt`

```cmake
find_package(Boost REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})
```

## patch failed

在更新版本之后出现 patch failed 异常，尝试删除对应的缓存解决。

```shell
$ rm -r {VCPKG_HOME}/buildtrees/protobuf
```

## 引用问题

### case 1 通过查看 share/{lib}/{lib}Config.cmake 查看

```shell
include_directories(${JSON11_INCLUDE_DIRS})
target_link_libraries({target} ${JSON11_LIBRARIES}) 
```

## unable to find "Ninja"

**full message**

```shell
CMake Error: CMake was unable to find a build program corresponding to "Ninja".  CMAKE_MAKE_PROGRAM is not set.  You probably need to select a different build tool.
```

**可能的原因**

- 没有或不是最新的 ninja，从 [这里](https://github.com/ninja-build/ninja/releases) 下载最新 ninja 程序
- 使用的是 ninja-build 程序，需要把 ninja 复制或软链称 ninja-build
- 其他原因，排查错误信息的 `vcpkg-manifest-install.log` 文件
  - git 权限问题
  - 磁盘内存不足

## submodule

在使用 `vcpkg_from_git` 时，不会初始化 submodule，需要自己处理。

```cmake
set(GIT_URL {git-or-http-url})
set(GIT_REF {commit-id-or-tag})

set(SOURCE_PATH ${CURRENT_BUILDTREES_DIR}/${GIT_REF})
file(MAKE_DIRECTORY ${SOURCE_PATH})
message(STATUS "build {lib} [CURRENT_BUILDTREES_DIR=${CURRENT_BUILDTREES_DIR}, SOURCE_PATH=${SOURCE_PATH}]")
if (NOT EXISTS "${SOURCE_PATH}/.git")
    message(STATUS "Cloning")
    vcpkg_execute_required_process(
            COMMAND ${GIT} clone ${GIT_URL} ${SOURCE_PATH}
            WORKING_DIRECTORY ${SOURCE_PATH}
            LOGNAME clone
    )
endif ()

message(STATUS "Fetching submodules")
vcpkg_execute_required_process(
        COMMAND ${GIT} submodule update --init
        WORKING_DIRECTORY ${SOURCE_PATH}
        LOGNAME submodule
)

message(STATUS "Checkout revision ${GIT_REF}")
vcpkg_execute_required_process(
        COMMAND ${GIT} checkout ${GIT_REF}
        WORKING_DIRECTORY ${SOURCE_PATH}
        LOGNAME checkout
)
```

## Checkout Git Tree

检出并保存在其他路径

```shell
mkdir /tmp/<tree-ish>
git archive <tree-ish> | tar -x -C /tmp/<tree-ish>
```

从 remote 检出 

```shell
git archive --remote=https://github.com/user/repo.git <tree-ish> | tar -x -C /tmp/<tree-ish>
```

示例

从 vcpkg 检出 gRPC 1.22.0 的 port 文件到当前目录。

```shell
# 从本地检出
git -C ~/.local/vcpkg archive f9ee8bb31f04f4e6a8c0d3e96fbb98deeb448d45 | tar -x -C .

# 从 remote 检出 (不一定能行)
git archive --remote=git@github.com:grpc/grpc.git f9ee8bb31f04f4e6a8c0d3e96fbb98deeb448d45 | tar -x -C .
```

## `--host` 问题

起因是使用镜像编译，设置如下变量。

```shell
export CC=/usr/bin/gcc10-cc
export CXX=/usr/bin/gcc10-c++
```

编译的时候，有些依赖库会报错。看 config 日志在调用库的 configure 中传入 `--host=gcc10`，部分信息如下。

```shell
config-x64-linux-dbg-err.log:invalid configuration `gcc10': machine `gcc10-unknown' not recognized
config-x64-linux-dbg-config.log:host=gcc10
```

这显然是 vcpkg 在获取 host 时出错了。具体原因未知，解决方式是把 CC 和 CXX 设置为 `/usr/bin/{cc/cxx}`

```shell
ln -s /usr/bin/gcc10-cc /usr/bin/cc
ln -s /usr/bin/gcc10-c++ /usr/bin/c++
export CC=/usr/bin/cc
export CXX=/usr/bin/c++
```

## Makefile 工程 build 失败

1. vcpkg_build_make 默认会构建目标 all

```shell 
CMake Error at scripts/cmake/vcpkg_execute_build_process.cmake:134 (message):
    Command failed: /usr/bin/make STATIC=1 SHARED=0 V=1 -j 1 -f Makefile all
```

可以通过如下命令指定目标。

```shell
vcpkg_build_make(OPTIONS STATIC=1 SHARED=0 DISABLE_PARALLEL BUILD_TARGET build INSTALL_TARGET install)
```

2. 尝试添加 DISABLE_PARALLEL，关闭并行编译

## AR 命令错误

makefile

```makefile
AR= ar rc
...
$(CORE_T): $(CORE_O) $(AUX_O) $(LIB_O)
	$(info CKPT2 : $(AR))
	$(AR) $@ $(sort $?)
	$(RANLIB) $@
```

使用 vcpkg 编译时，命令如下。

```shell
CKPT2 : ar
```

但是手动运行命令时，输入如下。

```shell
CKPT2 : ar rc
```

可以看到，在使用 vcpkg 编译时（vcpkg_build_make），makefile 中指定的 AR 变量没生效。

在 AR 重新定义前，添加打印。

```shell
$(info CKPT3 AR=$(AR))
AR= ar rc
$(info CKPT4 AR=$(AR))
```

输入如下。

```shell
# vcpkg 输出:
CKPT3 AR=ar
CKPT4 AR=ar

# 手动运行输出:
CKPT3 AR=ar
CKPT4 AR=ar rc
```

可以看到，vcpkg 运行时，AR 变量没有修改成功。再去检查 AR 的来源。

```shell
# 打印代码
$(info CKPT6 AR 的来源: $(origin AR))

# vcpkg 运行
CKPT6 AR 的来源: environment override
# 手动运行
CKPT6 AR 的来源: default
```

可以看到，vcpkg 在运行时，定义了环境变量 AR。

**解决方案 一**

```shell
# 修改 makefile 中的赋值语句，添加 override 强制赋值
override AR= ar rc
```

**解决方案 二**

```shell
# 在父 makefile 中添加 unexport
unexport AR
```

**解决方案 三**

```shell
# 定义 AR 参数
vcpkg_build_make(DISABLE_PARALLEL OPTIONS "AR=ar rc")
```

这种方案有可能可以解决问题，但是需要知道的是对所有 ar 命令都加了 rc，可能会造成其他问题。

## Make 工程跳过配置编译出错

```shell
# install prefix fixup: 由于 aerospike client 没有 configure 脚本，所以需要手动设置安装路径 INSTALL_PREFIX
# INSTALL_PREFIX 是代码文件 pkg/install 内定义的
# 这里的 INSTALL_PREFIX 是 {prefix_dir}/{install_dir}
# vcpkg_configure_make 默认会指定 --prefix, 但是这里没有 configure 脚本，添加了 SKIP_CONFIGURE 选项
# 因此这里修复 INSTALL_PREFIX 为 {prefix_dir}/{install_dir}
# 不然这里会报错: https://github.com/microsoft/vcpkg/blob/master/scripts/cmake/vcpkg_build_make.cmake#L177C8-L177C102
# 报错代码： file(RENAME "${CURRENT_PACKAGES_DIR}_tmp${Z_VCPKG_INSTALL_PREFIX}" "${CURRENT_PACKAGES_DIR}") 
string(REGEX REPLACE "([a-zA-Z]):/" "/\\1/" Z_VCPKG_INSTALL_PREFIX "${CURRENT_INSTALLED_DIR}")
set(ENV_INSTALL_PREFIX_ "$ENV{INSTALL_PREFIX}")
set(ENV{INSTALL_PREFIX} "${CURRENT_PACKAGES_DIR}${Z_VCPKG_INSTALL_PREFIX}")
```

> INSTALL_PREFIX 和库有关
