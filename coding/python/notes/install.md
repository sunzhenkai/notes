---
title: install python from source
categories: 
	- [python, notes]
tags:
	- python
date: 2022/08/24 00:00:00
---

# 从源码安装 Python3

**设置版本**

```shell
export PYTHON_VERSION=3.9.13
export PYTHON_MAJOR=3
```

**下载**

```shell
wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
tar -xvzf Python-${PYTHON_VERSION}.tgz --no-check-certificate
cd Python-${PYTHON_VERSION}
```

**配置**

```shell
./configure \
    --prefix=/opt/python/${PYTHON_VERSION} \
    --enable-shared \
    --enable-ipv6 \
    LDFLAGS=-Wl,-rpath=/opt/python/${PYTHON_VERSION}/lib,--disable-new-dtags \
    --enable-optimizations
```

**编译安装**

```shell
make
sudo make install
```

**安装 pip**

> 安装 python 3.9.13 时已安装 pip

```shel
curl -O https://bootstrap.pypa.io/get-pip.py
sudo /opt/python/${PYTHON_VERSION}/bin/python${PYTHON_MAJOR} get-pip.py
```

