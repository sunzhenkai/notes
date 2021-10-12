---
title: elastic search dev tool
categories: 
	- [架构, 搜索引擎]
tags:
	- 架构
	- 搜索引擎
	- es
date: 2021/10/08 00:00:00
update: 2021/10/08 00:00:00
---

# 索引

## 查询所有索引 

```shell
GET /_cat/indices
{}
```

# 搜索

## 指定索引

```shell
GET /index_name/_search
{
  "query": {
    "match_all": {}
  }
}
```

