---
title: python - generate wheel
categories: 
  - [python, notes]
tags:
  - python
date: "2022-06-20T00:00:00+08:00"
update: "2022-06-20T00:00:00+08:00"
---

# 安装

```shell
$ pip3 install wheel setuptools
```

# 创建 `setup.py`

```python
from setuptools import setup

setup(
    name='abtest',
    version='1.0',
    packages=['.abtest'],
)
```

**`setup.py` 示例**

```shell
import os.path

from setuptools import setup

REQUIREMENTS = 'requirements.txt'
requires = []
if os.path.isfile(REQUIREMENTS):
    with open(REQUIREMENTS, 'r') as f:
        requires = f.read().splitlines()

# VERSION i.e. 1.3
with open('VERSION', 'r') as f:
    v = f.read()
    setup(
        name='abtest',
        version=v.strip(),
        packages=['abtest', 'data', 'model', 'utils'], # 指定 package
        install_requires=requires # 指定依赖基本版本
    )
```

# 打包工程

```shell
python setup.py bdist_wheel --universal
```

