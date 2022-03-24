---
title: python common notes
categories: 
	- [python, notes]
tags:
	- python
date: 2021/10/06 00:00:00
update: 2021/10/06 00:00:00
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

# json

## 序列化类

```python3
json.dumps(obj, default=vars)  # 使用 vars 序列化对象, 打印对象的所有属性
```

