---
title: pyenv
categories: 
	- [python, tools]
tags:
	- virtualenv
date: 2022/07/17 00:00:00
---

# 安装

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

# 安装 Python 版本

```shell
pyenv install 3.9.10
```

# 使用版本

```shell
pyenv global 3.9.10
```

# 错误

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

