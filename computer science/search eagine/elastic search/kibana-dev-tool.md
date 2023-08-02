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

## 所有数据

```shell
GET /<index>/_search
{
  "query": {
    "match_all": {},
    "track_total_hits": true
  }
}
```

> `track_total_hits=true` 返回准确的数量，不然 total.value 最大返回 10000 

## 搜索字段

```json
GET /<index>/_search
{
  "query": {
    "match": {
      "<filed>": "<value>"
    }
  }
}
```

## 正则

```json
GET /<index>/_search
{
  "query": {
    "regexp": {
      "<filed>": "<regepx>"
    }
  }
}

# 不为空
{
  "query": {
    "regexp": {
      "<filed>": ".+"
    }
  }
}
```

## 有值

```json
GET /_search
{
  "query": {
    "exists": {
      "field": "<field>"
    }
  }
}
```

# 更新数据

```json
POST /<index>/_update/<id>
{
  "doc": {
    "<field>": "<value>"
  }
}
```

# 索引

## 创建索引

```json
PUT /<new-index>
{
  "settings": {
    "index.store.type": "mmapfs",
    "index.refresh_interval": "1s",
    "index.number_of_replicas": "5",
    "index.number_of_shards": "2",
    "index.max_result_window": "5000000"
  },
  "mappings": {
    "date_detection": true
  }
}
```

## 删除索引

```json
DELETE /<index>
{
}
```

## 重建索引

```json
POST _reindex
{
  "source": {
    "index": "<source-index>"
  },
  "dest": {
    "index": "<dest-index>"
  }
}
```

