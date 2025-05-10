---
title: mariadb 常见问题
categories: 
  - [架构, 存储, mariadb]
tags:
  - mariadb
date: "2021-08-30T00:00:00+08:00"
update: "2021-08-30T00:00:00+08:00"
---

# too many connections

客户端报错 `too many connections`，问题修复参考[这里](https://www.cnblogs.com/kevingrace/p/6226324.html).

**查看当前连接数限制**

```shell
$ mysql -u root -p
> show variables like "max_connections";
+-----------------+-------+
| Variable_name | Value |
+-----------------+-------+
| max_connections | 214 |
+-----------------+-------+
```

**临时配置**

```shelll
> set GLOBAL max_connections=1024;
```

**永久配置**

```shell
# step 1: 修改数据库最大连接数
# vim /etc/my.cnf
[mysqld]
# ...
max_connections=1024

# step 2: 修改 mariadb 默认打开文件数限制
# vim /usr/lib/systemd/system/mariadb.service
[Service]
# ...
LimitNOFILE=10000
LimitNPROC=10000
```

