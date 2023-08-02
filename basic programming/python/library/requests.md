---
title: python requests
categories: 
  - [python, library]
tags:
  - python
date: 2020/12/08 19:00:00
---

# 安装

```shell
$ pip3 install requests
```

# 引入

```python
import requests
```

# 请求

## 头

```python
headers = {'user-agent': '...'}
requests.get(url, headers=headers)
```

## 参数

```python
# Get
payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
r = requests.get(url, params=payload)

# Post Json
data = {'key': 'value'}
r = requests.post(url, data=json.dumps(data), headers=headers) # OR
r = requests.post(url, json=data)
```

# 读取

```python
# 返回码
r.status_code

# Json 数据
r.json()

# 读取二进制数据
r.content

# 读取图片
from PIL import Image
from io import BytesIO

i = Image.open(BytesIO(r.content))

# 保存到文件
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
```

