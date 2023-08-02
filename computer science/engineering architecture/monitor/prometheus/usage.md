---
title: prometheus usage
categories: 
  - [架构, 监控, prometheus]
tags:
  - prometheus
date: 2021/11/10 00:00:00
update: 2021/11/10 00:00:00
---

# 异常报警

- 指标使用 counter，出现异常时 inc 指标值
- 通过 increase 方法，查询某一段时间内指标增加值，如果 > 0 或达到自定义条件，触发报警