---
title: prometheus 查询语句
categories: 
  - [架构, 监控, prometheus]
tags:
  - prometheus
date: "2021-01-12T00:00:00+08:00"
update: "2021-01-12T00:00:00+08:00"
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
sum(increase(requst_count{counter="...",...}[3d]))

# sum_over_time
sum(sum_over_time(request_count{...}[1d]))
```

# QPS

```shell
# 单机
rate(request_count{label='value',...}[1m])
irate(request_count{label='value',...}[1m])  
# irate 比 rate 更能凸显瞬时值, 或者说 rate 比 irate 更平滑

# 所有机器
sum(rate(request_count{label='value',...}[1m]))
```

# Label Replace

**语法**

```shell
label_replace(query, "dest_label", "replacement", "src_label", "regex")

# 说明
query: 			 查询语句
dest_label:  替换后的 label 名称
replacement: 替换后的 label value 表达式, 支持正则查询后的分组
src_label:   需要替换的 label
regex:       需要替换的 label value 正则表达式
```

**示例**

``` shell
label_replace(up{job="node-exporter"}, "foo", "bar-$1", "job", "node-(.+)")
# 效果
up{foo="bar-exporter"}
# 说明
$1 = exporter

# 使用 time range
rate(label_replace(up{job="node-exporter"}, "foo", "bar-$1", "job", "node-(.+)")[1m:])
```

# ON...GROUP_LEFT

**示例**

统计分可用区的服务可用性。 

```shell
sum(rate(label_replace(no_fail_request{job=~"${cluster}"}, "private_ip_address", "$1", "instance", "(.*):8000$")[1m:]) * on (private_ip_address) group_left(zone) agent_status{instance_state="running",region="${cluster}"}) by (zone) / 
sum(rate(label_replace(total_request{job=~"${cluster}"}, "private_ip_address", "$1", "instance", "(.*):8000$")[1m:]) * on (private_ip_address) group_left(zone) agent_status{instance_state="running",region="${cluster}"}) by (zone)
```

# 过滤不为 0

```shell
avg(metric_name{] != 0) by (region)  # 对值为 0 的指标不进行 avg 计算
avg(metric_name{]) by (region) ！= 0  # 对值为 0 的结果不进行展示
```

