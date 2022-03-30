---
title: mongoldb
categories: 
	- [架构, 存储, mongodb]
tags:
	- mongodb
date: 2022/1/4 00:00:00
update: 2022/1/4 00:00:00
---

# docker

```shell
docker pull mongo
docker run -itd --name mongo -p 27017:27017 mongo
```

# 导出

在[这里](https://www.mongodb.com/try/download/database-tools)下载 Mongodb Database tools。

```shell
# 导出
$ mongodump --uri "mongodb://usersname:password@127.0.0.1:27100/dbname?replicaSet=replica_name&authSource=admin" --out "/path/to/save"

$ mongodump --uri "mongodb://127.0.0.1" --out data-dump --db library --collection booksion
```

# 导入

```shell
$ mongorestore --nsInclude=<db>.<table> /path/to/data.bson
```

# 操作

文档参考[这里](https://www.mongodb.com/docs/mongodb-shell/run-commands/)。

```shell
# 1. 创建数据库. 使用 use 即可创建 database
> use <db-name>

# 2. 创建集合. 使用插入数据语法, 不存在集合则创建 
> db.test.insertOne( { x: 1 } );
```

