---
title: pyenv
categories: 
  - [python, notes]
tags:
  - python
date: 2021/12/08 00:00:00
update: 2021/12/08 00:00:00
---

# 安装

```shell
# brew
brew install pyenv

# 脚本
curl https://pyenv.run | bash
```

# 列出所有可安装版本

```shell
$ pyenv install -l
```

# 安装某个版本

```shell
$ pyenv install <version>  # e.g 3.8.9
# 使用国内源安装
$ v=3.8.9;wget https://npm.taobao.org/mirrors/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v 
```

# 设置全局版本

```shell
pyenv global 3.8.9
```

# 查看 安装的版本

```shell
pyenv versions
```

# 回滚系统默认

```shell
pyenv global system
```

