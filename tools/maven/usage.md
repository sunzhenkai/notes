---
title: maven 使用
categories:  
	- [工具,maven]
tags:
	- maven
date: 2021/01/29 00:00:00
update: 2021/01/29 00:00:00
---

# 命令

```shell
# 清理
$ mvn clean

# 打包
$ mvn package

# 依赖树
$ mvn dependency:tree

# 指定 pom
$ mvn --settings YourOwnSettings.xml package
# OR
$ mvn -s YourOwnSettings.xml package
```

