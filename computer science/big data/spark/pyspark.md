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

# 创建列

## 重命名

```python
df_renamed = df.withColumnRenamed('name1', 'name2')
```

## 从其他列新建列

### 数值计算

```python
new_df = df.withColumn('After_discount', df.Course_Fees - df.Discount) 
```

### 使用 UDF

```python
import pyspark.sql.functions as F 
from pyspark.sql.types import IntegerType 
  
# define the sum_col 
def Total(Course_Fees, Discount): 
    res = Course_Fees - Discount 
    return res 
  
new_f = F.udf(Total, IntegerType()) 
new_df = df.withColumn("Total_price", new_f("Course_Fees", "Discount")) 

# 使用 udf
@udf(IntegerType())
def Total(Course_Fees, Discount): 
    res = Course_Fees - Discount 
    return res 
  
# 使用 udf + lambda
function = udf(lambda col1, col2 : col1-col2, IntegerType())
new_df = old_df.withColumn('col_n',function(col('col_1'), col('col_2')))
```

## 计算

### 最大值

```python3
df.agg(max("age")).show()
```

# 转换

## row to json string

```shell
df.toJson()
```

# 写数据

```python
df.write.format('orc').save('/path/to/destination')
df.coalesce(1).write.format('json').save('/path/to/destination') # 写单个文件
```

**文本文件**

```python
df.coalesce(1).write.format("text").option("header", "false").mode("overwrite").save('/path/to/destination')
```

# 报错

```shell
# 代码
from pyspark.sql.functions import *
@F.udf(IntegerType())
def TimeDiff(a, b): 
    return abs(a - b)
    
# 报错
TypeError: Invalid argument, not a string or column: 1 of type <class 'int'>. For column literals, use 'lit', 'array', 'struct' or 'create_map' function.
```

```python
因为使用 from pyspark.sql.functions import * 导入，导致 abs 使用 from pyspark.sql.functions 内的函数
```

## TypeError: Can not infer schema for type: <class 'str'>

`rdd.toDF()` 时报错。

```shell
from pyspark.sql import Row

row = Row("val") # Or some other column name
rdd.map(row).toDF()
```

或者

```python
rdd.map(lambda x: (x, )).toDF()
```

