---
title: python argparse
categories: 
	- [python, notes]
tags:
	- python
date: 2021/09/29 00:00:00
update: 2021/09/29 00:00:00
---

# 创建解析对象

```python
parser = argparse.ArgumentParser()
```

# kv

```python
parser.add_argument('-a', '--age', required=True)      # 必选
parser.add_argument('-p', '--product', required=False)  # 非必选
```

**example**

```python
>>> import argparse
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('-a', '--age', required=True)
...
>>> parser.add_argument('-p', '--product', required=False)
...
>>> parser.parse_args('-a 10'.split())
Namespace(age='10', product=None)
>>> parser.parse_args('-a 10 -p wii'.split())
Namespace(age='10', product='wii')
>>> parser.parse_args('-p wii'.split())
usage: [-h] -a AGE [-p PRODUCT]
: error: the following arguments are required: -a/--age
```

# 标记

```python
parser.add_argument('-a', '--age', action='store_true')         # 如果指定则为 True, 否则为 False
parser.add_argument('-n', '--name', action='store_false')       # 如果指定则为 False, 否则为 True
parser.add_argument('-m', '--price', action='store_const', const=10)  # 如果指定则为 const 的值, 否则为 None
```

**example**

```shell
>>> import argparse
>>> parser = argparse.ArgumentParser()
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('-a', '--age', action='store_true')
...
>>> parser.add_argument('-n', '--name', action='store_false')
...
>>> parser.add_argument('-m', '--price', action='store_const', const=10)
...
>>> parser.parse_args('-anm'.split())
Namespace(age=True, name=False, price=10)
>>> parser.parse_args('-a'.split())
Namespace(age=True, name=True, price=None)
>>> parser.parse_args('-m'.split())
Namespace(age=False, name=True, price=10)
>>> parser.parse_args('-n'.split())
Namespace(age=False, name=False, price=None)
>>> parser.parse_args(''.split())
Namespace(age=False, name=True, price=None)
```

