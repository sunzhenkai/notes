---
title: django startup
categories: 
	- [python, library, django]
tags:
	- django
date: 2020/12/10 19:00:00
---

# 安装

```shell
# 安装最新
$ pip3 install django

# 指定版本
$ pip3 install django==3.0.7
```

# 创建应用

```shell
# 创建Project
$ django-admin startproject mysite

# 创建应用
$ python3 manage.py startapp polls
```

# 配置

## 数据库

### MySQL

**使用 pymysql 库替代 mysqldb**

```shell
# 安装
$ pip install pymysql

# 替换
## settings.py 中添加
import pymysql
pymysql.version_info = (1, 4, 13, 'final', 0)
pymysql.install_as_MySQLdb()
```

**配置**

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test-db',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'root'
    }
}
```

