---
title: cassandra - cql
categories: 
	- [架构,存储,cassandra]
tags:
	- cassandra
date: 2022/07/06 00:00:00
---

[toc]

# 语法

[CQL](https://docs.datastax.com/en/cql-oss/3.3/cql/cqlIntro.html)。

# Datacenter

```CQL
use system;
select data_center from local;
```

# Role / User

## 创建

```shell
CREATE ROLE [IF NOT EXISTS] role_name 
[WITH SUPERUSER = true | false
 | LOGIN = true | false  
 | PASSWORD =  'password' 
 | OPTIONS = option_map]
```

**示例**

```shell
CREATE ROLE IF NOT EXISTS 'root' WITH SUPERUSER = true AND LOGIN = false;
CREATE ROLE IF NOT EXISTS 'root' WITH SUPERUSER = true AND PASSWORD = 'root';
```

## 修改权限

```shell
ALTER ROLE role_name 
[WITH [PASSWORD = 'password']
   [LOGIN = true | false] 
   [SUPERUSER = true | false] 
   [OPTIONS = map_literal]]
```

**示例**

```cql
ALTER ROLE root WITH PASSWORD = 'NewPassword';
```

# Key Space

## 查询

```shell
desc keyspaces;
```

## 创建

```sql
CREATE  KEYSPACE [IF NOT EXISTS] keyspace_name 
   WITH REPLICATION = { 
      'class' : 'SimpleStrategy', 'replication_factor' : N } 
     | 'class' : 'NetworkTopologyStrategy', 
       'dc1_name' : N [, ...] 
   }
   [AND DURABLE_WRITES =  true|false] ;
```

**示例**

```sql
CREATE  KEYSPACE IF NOT EXISTS "trace" WITH REPLICATION = {
		'class' : 'NetworkTopologyStrategy', 
   	'vg' : 2
}
```

# Table

## 创建

```cql
CREATE TABLE [IF NOT EXISTS] [keyspace_name.]table_name ( 
   column_definition [, ...]
   PRIMARY KEY (column_name [, column_name ...])
[WITH table_options
   | CLUSTERING ORDER BY (clustering_column_name order])
   | ID = 'table_hash_tag'
   | COMPACT STORAGE]
```

数据类型参考[这里](https://docs.datastax.com/en/cql-oss/3.3/cql/cql_reference/cql_data_types_c.html)。

## 删除

```cql
DROP TABLE [IF EXISTS] keyspace_name.table_name
```

## 修改

### 添加列

```cql
ALTER TABLE [keyspace_name.] table_name 
[ALTER column_name TYPE cql_type]
[ADD (column_definition_list)]
[DROP column_list | COMPACT STORAGE ]
[RENAME column_name TO column_name]
[WITH table_properties];
```

**示例**

```cql
ALTER TABLE trace.ranker ADD rid TEXT;
```

