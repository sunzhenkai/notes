---
title: scylladb
categories: 
  - [架构,存储,scylladb]
tags:
  - scylladb
date: "2025-03-18T00:00:00+08:00"
---

# AQL

[官方文档](https://aerospike.com/docs/tools/aql/aql-help)。

## Insert

```aql
INSERT INTO test.demo (PK, username, email) VALUES ('user1', 'John', 'john@example.com');
```

## Select

```
SELECT * FROM test.demo WHERE PK = 'user1';
```

