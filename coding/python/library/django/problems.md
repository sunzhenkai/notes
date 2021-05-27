---
title: django 常见问题
categories: 
	- [python, library, django]
tags:
	- django
date: 2020/12/24 19:00:00
---

# 启动时执行一次

```python
# 在 app 目录下的 apps.py 中定义 Config

from django.apps import AppConfig


class JobConfig(AppConfig):
    name = 'job'

    def ready(self):
        from jobs import scheduler  # jobs 为 app 名称
        scheduler.start()           # scheduler.start() 是要做的事情; 这里是启动一个定时器
        
# 在 app 目录下的 __init__.py 中添加
import os

if os.environ.get('RUN_MAIN', None) != 'true':    # 加这个判断，可以防止执行多次
    default_app_config = 'jobs.apps.JobConfig'

# 注: 使用manage.py时，也有可能会运行
```

# CORS

```shell
# install django-cors-headers
$ pip install django-cors-headers

# add apps in settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

# add middleware in settings.py
MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

# add config in settings.py
CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3030',
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://*.example.com:3030',
]
```

