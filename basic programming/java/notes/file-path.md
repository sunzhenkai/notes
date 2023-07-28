---
title: file & path
categories: 
	- [coding,java,notes]
tags:
	- java
date: 2021/11/17 00:00:00
update: 2021/11/17 00:00:00
---

# 用户目录

```shell
# 用户目录转换绝对路径
path.replaceFirst("^~", System.getProperty("user.home"))
# ~/foo -> /home/user/foo
```

