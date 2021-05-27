---
title: panda
categories: 
	- [python, library]
tags:
	- panda
date: 2020/12/04 20:00:00
---

#  引入

```python
import pandas as pd
```

# 配置

```python
# 修改print时显示列行列数
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)
```

# 过滤

```python
# 按列值过滤
df[df['部门'].isin(['市场部']) & ~df['省份'].isin(['北京'])] # 部门=市场部 & 省份!=北京
```

# 转换

```python
# 转换所有列
df = df.apply(pd.to_numeric)
df = df.apply(pd.to_numeric, errors='ignore')	 # 忽略异常

# 转换特定列
df[['a', 'b']] = df[['a', 'b']].apply(pd.to_numeric)

# 一列转换为多列
df[['a', 'b', 'c']] = df['label'].apply(lambda x: pd.Series(x.split(',')))
```





