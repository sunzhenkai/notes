---
title: mongodb query
categories: 
  - [架构, 存储, mongodb]
tags:
  - mongodb
date: "2022-01-07T00:00:00+08:00"
update: "2022-01-07T00:00:00+08:00"
---

# 进入交互界面

```shell
$ mongo
```

# 查询

```shell
# 查看数据库
> show dbs;
local    0.000GB
test     0.000GB

# 进入数据库
> use test;

# 查看集合
> show collections; # 或者 show tables;

# 查询集合
> db.test.findOne()

# 统计数量
> db.test.count({...})

# 指定字段
db.user.find({"status": 1, "updated": {"$gt" : 1672831786 }}, {updated: 1})
```

> 和关系型数据库对应，collections - table，doc - row。

## 类型查询

可用类型查看[这里](https://docs.mongodb.com/manual/reference/operator/query/type/#available-types)。

```shell
> db.test.findOne({id: {$type: 'int'}})
> db.test.findOne({id: {$not: {$type: 'int'}}})
```

