---
title: mariadb usage
categories: 
  - [架构, 存储, mariadb]
tags:
  - mariadb
date: "2022-10-01T00:00:00+08:00"
---

# Install

```shell
sudo apt install mariadb-server
sudo mysql_secure_installation
sudo systemctl start mariadb.service
```

# 导入导出

```shell
# 导出
sudo mariadb-dump <db> out.sql

# 导入
sudo mariadb
> source out.sql
```

