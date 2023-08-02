---
title: mongoldb
categories: 
  - [架构, 存储, mongodb]
tags:
  - mongodb
date: 2022/1/4 00:00:00
update: 2022/1/4 00:00:00
---

# 安装

```shell
# aliyun linux 3
vim /etc/yum.repos.d/mongodb-org-6.0.repo
# 输入如下内容
[mongodb-org-6.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/8/mongodb-org/6.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc

# 安装
sudo yum install -y mongodb-org mongodb-database-tools mongodb-mongsh

# 管理
sudo systemctl start mongod
sudo systemctl status mongod
sudo systemctl enable mongod
sudo systemctl stop mongod
sudo systemctl restart mongod

# 使用 mongo db
mongosh 
```

- [参考](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-red-hat/)

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

