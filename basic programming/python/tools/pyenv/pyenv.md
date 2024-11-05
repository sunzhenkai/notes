---
title: pyenv
categories: 
  - [python, tools]
tags:
  - virtualenv
date: 2022/07/17 00:00:00
---

# 安装

## 脚本安装

```shell
curl https://pyenv.run | bash
```

## HomeBrew 安装

```shell
# 安装 brew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 pyenv
brew install pyenv
```

# 生效

```shell
eval "$(pyenv init -)"
```

# Python 版本管理

## 可安装版本

```shell
pyenv install -l
```

## 安装

```shell
pyenv install 3.9.10
```

## 使用版本

```shell
pyenv global 3.9.10
```

# 问题排查

## 依赖

```shell
sudo apt install libreadline-dev libbz2-dev libncurses-dev libffi-dev libssl-dev sqlite3 libsqlite3-dev
```

## openssl 错误

```shell
...
ERROR: The Python ssl extension was not compiled. Missing the OpenSSL lib?
...
```

**解决**

```shell
PYTHON_BUILD_HOMEBREW_OPENSSL_FORMULA=openssl@1.0 pyenv install 2.7.16

# 或者尝试
CFLAGS=-I/usr/include/openssl LDFLAGS=-L/usr/lib pyenv
```

