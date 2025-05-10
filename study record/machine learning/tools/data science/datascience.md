---
title: 数据科学基础开发环境
categories: 
    - 机器学习
tags:
    - 机器学习
date: "2023-07-27T00:00:00+08:00"
update: "2023-07-27T00:00:00+08:00"
---

基于 Docker Compose 搭建了常用的大数据工具，可以作为大数据及 AI 相关的开发环境。

# Spark

## pyspark 创建 session

```shell
spark = pyspark.sql.SparkSession.builder.master("spark://datascience-spark:7077").getOrCreate()
```

## 访问 Hadoop

```shell
# 只需要指定 hadoop name node 的地址即可
# namenode 是 hadoop namenode 的机器名，这里可以反解出 ip
df = spark.read.json("hdfs://namenode/sample.json") 
```

