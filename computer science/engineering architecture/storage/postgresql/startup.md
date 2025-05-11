---
title: postgresql - startup
categories: 
  - [架构, 存储, postgresql]
tags:
  - mysql
date: "2023-08-08T00:00:00+08:00"
---

# 命令

## 登录

```shell
# login
$ psql -U postgres  # 指定用户，无密码
```

## 用户操作

```shell
CREATE USER root WITH CREATEDB CREATEUSER PASSWORD 'root';
```

## role 操作

```shell
CREATE ROLE root WITH LOGIN CREATEDB CREATEROLE SUPERUSER PASSWORD 'root';

# 查看
SELECT * FROM pg_roles;
```

## 数据库操作

```shell
CREATE DATABASE dolphinscheduler;
```

