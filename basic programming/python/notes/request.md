---
title: python - request
categories: 
	- [python, notes]
tags:
	- python
date: 2022/06/20 00:00:00
update: 2022/06/20 00:00:00
---

# 引入

```python
import urllib.request
```

# 发送请求

```shell
q = urllib.request.Request(url=url, method='GET')
with urllib.request.urlopen(q) as f:
	status = f.status
	data = f.read().decode('utf-8')
```

