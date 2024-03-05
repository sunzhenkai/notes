---
title: pyspark
categories: 
  - [big data, spark]
tags:
  - spark
date: 2022/06/04 00:00:00
update: 2022/06/04 00:00:00
---

# 常用操作

## 以文本形式保存 DataFrame 一列

```python
# dateframe
data = df.rdd.map(lambda x: x.{column}).collect()
data_rdd = spark.sparkContext.parallelize(data)
data_rdd.coalesce(1).saveAsTextFile('hdfs://path')
```

## 处理 WrappedArray

```python
row.scores[0]
```

## Join 时重复行保留一个

```python
df_a.join(df_b, on=[{column}]) # 使用 on
```

# 过滤

## 多条件过滤

```python
df.filter((condition1) & (condition2))
```

## 包含字符串

```python
df.filter(col('name').contains('sun'))
```

## 值比较

```python
df.filter(col('name') == "wii")
```

## Null 判断

```python
df.filter(col('name').isNull())
df.filter(col('name').isNotNull())
```

## In 判断

```python
df.filter(col('name').isin(["wii", "bovenson"]))
```

