---
title: python random
categories: 
  - [python, notes]
tags:
  - python
date: 2021/08/25 00:00:00
update: 2021/08/25 00:00:00
---

# 常用

## 从数组中选取

```shell
# 定义数组
>>> l = [1, 2, 3, 4, 5, 6, 7]
# 随机选一个
>>> random.choice(l)  			
6
# 随机选多个，可重复
>>> random.choices(l, k=3)
[7, 4, 7]
# 随机选多个，不重复
>>> random.sample(l, 3)
[3, 5, 7]
```

