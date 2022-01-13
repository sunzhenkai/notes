---
title: mongoldb
categories: 
	- [架构, 存储, mongodb]
tags:
	- mongodb
date: 2022/1/4 00:00:00
update: 2022/1/4 00:00:00
---

# 导出

在[这里](https://www.mongodb.com/try/download/database-tools)下载 Mongodb Database tools。

```shell
# 导出
$ mongodump --uri "mongodb://usersname:password@127.0.0.1:27100/dbname?replicaSet=replica_name&authSource=admin" --out "/path/to/save"

$ mongodump --uri "mongodb://127.0.0.1" --out creative-dump --db library --collection booksion
```

# 导入

```shell
$ mongorestore --nsInclude=<db>.<table> /path/to/data.bson
```



