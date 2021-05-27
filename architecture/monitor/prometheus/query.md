---
title: prometheus 查询语句
categories: 
	- [架构, 监控, prometheus]
tags:
	- prometheus
date: 2021/01/12 00:00:00
update: 2021/01/12 00:00:00
---

# 分组求和

```sql
# 语法
sum by(cluster)(rate(...))

# 对应用 <app> 最进一分钟的counter标签值为 <search> 的数据，以 cluster 为分组进行求和
sum by(cluster)(rate(<app>_timer_count{counter="search"}[1m]))
```

# 一段时间内总量

```sql
 # 3天内请求总量
sum(increase(requst_count{counter="...",...}}[3d]))
```

