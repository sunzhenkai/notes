---
title: pandas
categories: 
  - [machine learning, tools, pandas]
tags:
  - machine learning
  - pandas
date: "2022-06-05T00:00:00+08:00"
---

# 安装

```shell
pip3 install pandas
```

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

# 导入导出

## 读取 csv 文件

```shell
df = pd.read_csv('dataset.csv')
df = pandas.read_csv('data.csv', delimiter='\t') # 指定 delimiter
df = pd.read_csv("fn", index_col=None, header=0)
```

## 从数组创建

```shell
>>> import pandas as pd
>>> arr = [[1, 2], [3, 4]]
>>> df = pd.DataFrame(arr, columns=['x', 'y'])
>>> df
   x  y
0  1  2
1  3  4
```

## 转换为 numpy 对象

```shell
# 转换为 np array
df.to_numpy()
```

## 导出到文件

```shell
df.to_csv('output.cvs')
```

# 数据透视

```shell
# 描述数据
data.describe()
data.info()

# 打印前 n 行
df.head(n)

# 打印列
data.columns
```

# 数据操作

## 列操作

**读操作**

```shell
# 选取一列
data.<ColumnName>

# 选取多列
data[[<ColumnName>, <ColumnName>, <...>]]
# 过滤列
data.loc[:, df.columns != '<column_name>']

# 通过索引选取
df.iloc[:, 0]	# 第1列

# 对列取 unique
df[<ColumnName>].unique()

# 按类型选取列
df.select_dtypes(include=['float64', 'bool'])
df.select_dtypes(include='number') # 选取所有数字类型的列
```

**转换操作**

```shell
# 转换所有列
df = df.apply(pd.to_numeric)
df = df.apply(pd.to_numeric, errors='ignore')	 # 忽略异常

# 转换特定列
df[['a', 'b']] = df[['a', 'b']].apply(pd.to_numeric)

# 一列转换为多列
df[['a', 'b', 'c']] = df['label'].apply(lambda x: pd.Series(x.split(',')))
```

**Drop 列**

```python
# drop 有 nan 的列
df.dropna(axis=1, how='any')
```

## 行操作

**排序**

```shell
df = df.sort_values(by=[<ClomunName>], ascending=False)
```

**过滤**

```python
# loc
df.loc[df['column_name'] == some_value]
df.loc[df['column_name'].isin(some_values)]
df.loc[(df['column_name'] >= A) & (df['column_name'] <= B)]

# 按列值过滤
df[df['部门'].isin(['市场部']) & ~df['省份'].isin(['北京'])] # 部门=市场部 & 省份!=北京
t_df = t_df[t_df.服务名称 == '离线计算平台']
```

**连接**

```python
# 用法
merge(left, right, how='inner', on=None, left_on=None, right_on=None,
      left_index=False, right_index=False, sort=True,
      suffixes=('_x', '_y'), copy=True, indicator=False)

# 左连接
merge(data_x, data_y, how='left', on='uid')
```

# 示例

```shell
# 读取 Cell
data['age'][6]  # 读取 data 的 age 列第 6 行数据
```

