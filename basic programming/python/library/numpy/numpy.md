---
title: numpy
categories: 
	- [python, library, numpy]
tags:
	- numpy
date: 2021/08/31 20:00:00
---

# array

```shell
# 一维
>>> np.array([1, 2, 3])
array([1, 2, 3])

# 多维
>>> np.array([[1, 2, 3]], dtype=np.float32)
array([[1., 2., 3.]], dtype=float32)

# df: np.array
# 取 head 数据
df[:3]  

# 基于其他列创建新列
def trans(row):
  return row['old']
df['new'] = df.apply(trans, axis=1)  # axis=0 行; axis=1 列
df['Label'] = pd.Series(data=df.apply(trans, axis=1), dtype='int')
df.concat(pd.Series(data=df.apply(trans, axis=1))

# 选取行
df[:3] # 前三行

# 选取列
df[:, 0] # 选取第一列

# 选取行和列
df[:3, 0] # 选取前三行第一列
```


