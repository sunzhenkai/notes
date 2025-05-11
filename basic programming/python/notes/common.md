---
title: python common notes
categories: 
  - [python, notes]
tags:
  - python
date: "2021-10-06T00:00:00+08:00"
update: "2021-10-06T00:00:00+08:00"
---

# package

```python
import pathlib
import sys
from os.path import dirname, abspath

PROJECT_BASE_PATH = dirname(abspath(pathlib.Path(__file__).absolute()))
sys.path.append(PROJECT_BASE_PATH)
```

# path

## 判断路径是否存在

```python
os.path.exists('path')
```

## 获取 Home 路径

```python
from pathlib import Path
Path.home() # 用户目录
```

# json

## 序列化类

```python3
json.dumps(obj, default=vars)  # 使用 vars 序列化对象, 打印对象的所有属性
```

# **multiprocessing**

## 共享自定义对象

```python3
class A():
	pass

AProxy = MakeProxyType('A', public_methods(A))
setattr(multiprocessing.managers, 'A', AProxy)
SyncManager.register('A', A, AProxy)
manager = SyncManager()
manager.start()
shared_a = manager.A()
```

