---
title: pandas usage
categories: 
	- [python, library, pandas]
tags:
	- pandas
date: 2022/06/05 00:00:00
---

[toc]
#  引入

```python
import pandas as pd
```

# 读取文件

## 读取 csv 文件

```shell
df = pd.read_csv('dataset.csv')
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

# 常用操作

```python
# 某一列的所有取值
df['Species'].unique()

# 转换为 np array
df.to_numpy()
```

