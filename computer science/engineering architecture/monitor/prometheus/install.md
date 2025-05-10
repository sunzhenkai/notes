---
title: prometheus setup
categories: 
  - [架构, 监控, prometheus]
tags:
  - prometheus
date: "2021-11-06T00:00:00+08:00"
update: "2021-11-06T00:00:00+08:00"
---

# configuration

```yaml
...
```

# start

```shell
nohup ./prometheus --config.file prometheus.yml &
nohup ./prometheus --config.file prometheus.yml --storage.tsdb.path /path/to/data &  # 指定数据保存路径
```

