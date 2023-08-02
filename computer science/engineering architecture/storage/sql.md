---
title: SQL
categories: 
  - [架构, 存储]
tags:
  - SQL
date: 2021/01/12 00:00:00
update: 2021/01/12 00:00:00
---

# 创建表

**语法**

```SQL
CREATE TABLE 表名称 (
    列名称1 数据类型,
    列名称2 数据类型,
    列名称3 数据类型,
    ....
)
```

**示例**

```sql
CREATE TABLE `syscontroldb`.`sys_user` (
  `id` INT(11) NOT NULL COMMENT '用户DI，系统唯一标识',
  `userName` VARCHAR(45) NOT NULL COMMENT '用户名，系统唯一',
  `password` VARCHAR(45) NOT NULL COMMENT '用户密码，加密',
  `customerID` INT(11) NOT NULL COMMENT '所属用户代码',
  `tel` VARCHAR(20) NULL COMMENT '电话号码',
  `status` INT(3) NOT NULL COMMENT '用户状态，0正常，1注销，2暂停' DEFAULT 1,
  PRIMARY KEY (`id`))
COMMENT = '系统用户表';
```

# Select

```sql
SELECT * from <table> WHERE <field>=<value>
```

# Add

```sql
INSERT INTO <table> (<field>, <field>, ...) VALUES (<value>, <value>, ...)
```

# Updata

```sql
UPDATE <table> SET <field>=<value>,<field>=<value> WHERE <field>=<value>
```

# Join

## left

```sql
# 别名
SELECT a.id, b.id FROM zj_classify a left join zj_classify b on b.parent = a.id ;
```