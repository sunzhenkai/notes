---
title: mongo tools
categories: 
	- [架构, 存储, mongodb]
tags:
	- mongodb
date: 2022/1/7 00:00:00
update: 2022/1/7 00:00:00
---

# 工具

从 [这里](https://www.mongodb.com/try/download/shell) 下载。

- MongoDB Shell 

# Mongo Shell

```shell
# 下载
$ wget https://downloads.mongodb.com/compass/mongosh-1.1.9-linux-x64.tgz

# 解压
$ tar -xf mongosh-1.1.9-linux-x64.tgz
$ cd mongosh-1.1.9-linux-x64

# 查看帮助
$ ./bin/mongosh -h
```

## 参数

```shell
# 格式
$ mongosh [options] [db address] [file names (ending in .js or .mongodb)]

# options
-u username
-p password

# example
$ mongosh mongodb://192.168.0.5:9999/ships
```

## 读取 secondary 节点

参考 [这里](https://docs.mongodb.com/mongodb-shell/reference/compatibility/) 和 [这里](https://docs.mongodb.com/manual/reference/connection-string/#mongodb-urioption-urioption.readPreference)。

> ### Read Operations on a Secondary Node[![icons/link.png](https://docs.mongodb.com/mongodb-shell/assets/link.png)](https://docs.mongodb.com/mongodb-shell/reference/compatibility/#read-operations-on-a-secondary-node)
>
> When using the legacy mongo shell to connect directly to [secondary](https://docs.mongodb.com/manual/reference/glossary/#std-term-secondary) replica set member, you must run `mongo.setReadPref()` to enable secondary reads.
>
> When using `mongosh` to connect directly to a [secondary](https://docs.mongodb.com/manual/reference/glossary/#std-term-secondary) replica set member, you can read from that member if you specify a [read preference](https://docs.mongodb.com/manual/core/read-preference/) of either:
>
> - [`primaryPreferred`](https://docs.mongodb.com/manual/core/read-preference/#mongodb-readmode-primaryPreferred)
> - [`secondary`](https://docs.mongodb.com/manual/core/read-preference/#mongodb-readmode-secondary)
> - [`secondaryPreferred`](https://docs.mongodb.com/manual/core/read-preference/#mongodb-readmode-secondaryPreferred)
>
> ```shell
> mongodb://mongos1.example.com,mongos2.example.com/?readPreference=secondary&readPreferenceTags=dc:ny,rack:r1&readPreferenceTags=dc:ny&readPreferenceTags=
> ```

```shell
# 连接时添加 readPreference 参数
$ mongosh mongodb://192.168.0.5:9999/ships/?readPreference=secondary
```

