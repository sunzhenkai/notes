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

# 设置

## 允许远程连接

### 设置bind-address

```shell
# mariadb
/etc/mysql/mariadb.conf.d/50-server.cnf

# 修改bind-address
bind-address = 0.0.0.0
```

**重启**

```shell
sudo systemctl restart mariadb
```

# 权限

## 查看登录权限

```shell
SELECT User, Host FROM mysql.user;
```

## 添加用户

```sql
-- 添加用户
CREATE USER '用户名'@'允许登录的主机' IDENTIFIED BY '用户密码';
-- 授予数据库权限
GRANT SELECT, INSERT ON {DB}.* TO '{User}'@'{Host}';
```

## 修改用户在特定 Host 的登录密码

```sql
ALTER USER '用户名'@'主机' IDENTIFIED BY '新密码';
-- 刷新权限
FLUSH PRIVILEGES; 
```

## 授予权限

所有权限

```sql
GRANT ALL PRIVILEGES ON *.* TO '{User}'@'{Host}' WITH GRANT OPTION;
```

数据库的查询、插入权限

```sql
GRANT SELECT, INSERT ON {DB}.* TO '{User}'@'{Host}';
```

最后，刷新权限

```sql
FLUSH PRIVILEGES;
```

# 数据库

## 导入

```sql
```

