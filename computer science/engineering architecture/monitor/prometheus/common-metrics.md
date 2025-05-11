---
title: prometheus common metric
categories: 
  - [架构, 监控, prometheus]
tags:
  - prometheus
date: "2023-07-18T00:00:00+08:00"
---

# Node Exporter

## CPU 使用率

```shell
# 百分比
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)

avg by (instance) (irate(node_cpu_seconds_total{mode!='idle'}[1m]))
# 区分 mode
avg by (instance,mode) (irate(node_cpu_seconds_total{mode!='idle'}[1m]))
```

[参考](https://www.robustperception.io/understanding-machine-cpu-usage/)