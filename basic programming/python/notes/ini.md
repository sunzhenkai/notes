---
title: python ini config
categories: 
  - [python, notes]
tags:
  - python
date: 2021/11/25 00:00:00
update: 2021/11/25 00:00:00
---

# 加载

```shell
from configparser import ConfigParser

cp = ConfigParser()
cp.read('config.ini')

# 读取 section
cp.get('section', 'item')
```

