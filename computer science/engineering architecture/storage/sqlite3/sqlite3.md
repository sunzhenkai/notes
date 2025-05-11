---
title: sqlite3
categories: 
  - [架构, 存储]
tags:
  - 架构
  - 存储
date: "2022-07-20T00:00:00+08:00"
update: "2022-07-20T00:00:00+08:00"
---

# 打开 db 文件

```shell
sqlite3 db.sqlite3
```

# Query

参考 [sqlite.org/cli](https://www.sqlite.org/cli.html)。

## 查看表

```shell
.tables
# OR
SELECT name FROM sqlite_master WHERE type='table';
```

## 查看表创建语句

```shell
.schema <tablename>   # 去掉 <> , 不用 ; 结尾
```

