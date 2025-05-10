---
title: kudu - usage
categories: 
  - [架构,存储,kudu]
tags:
  - kudu
date: "2022-06-29T00:00:00+08:00"
update: "2022-06-29T00:00:00+08:00"
---

# 安装

新版本安装参考[这里](https://kudu.apache.org/docs/installation.html)。

## centos

**build**

```shell
#!/bin/bash
sudo yum -y install autoconf automake curl cyrus-sasl-devel cyrus-sasl-gssapi \
  cyrus-sasl-plain flex gcc gcc-c++ gdb git java-1.8.0-openjdk-devel \
  krb5-server krb5-workstation libtool make openssl-devel patch pkgconfig \
  redhat-lsb-core rsync unzip vim-common which
sudo yum -y install centos-release-scl-rh
sudo yum -y install devtoolset-8
git clone https://github.com/apache/kudu
cd kudu
build-support/enable_devtoolset.sh thirdparty/build-if-necessary.sh
mkdir -p build/release
cd build/release
../../build-support/enable_devtoolset.sh \
  ../../thirdparty/installed/common/bin/cmake \
  -DCMAKE_BUILD_TYPE=release \
  ../..
make -j4
```

> 对于 centos 7 默认 gcc 是 4.8，用 `yum install gcc72-c++` 升级到 gcc-g++ 7.2

**package**

```shell
# 下载 repo 配置
$ wget http://archive.cloudera.com/kudu/redhat/7/x86_64/kudu/cloudera-kudu.repo -P /etc/yum.repos.d/
# 安装
$ yum update & yum install kudu
```

