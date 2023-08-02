---
title: prometheus metric
categories: 
  - [架构, 监控, prometheus]
tags:
  - prometheus
date: 2021/10/14 00:00:00
update: 2021/10/14 00:00:00
---

# metric

| 指标类型  | 说明                           | 场景举例               |
| --------- | ------------------------------ | ---------------------- |
| Counter   | 累计计数器，只能增加或置零     | 请求数、错误数         |
| Gauge     | 数值指标监控，可增加也可以减小 | 温度、线程数量         |
| Histogram | 直方图采样统计，可设置分位统计 | 请求耗时、返回数据大小 |
| Summary   |                                |                        |

## Counter

Counter 用于累计指标，表示一个只能递增或置零的单调递增计数器。

## Gauge

Gauge 用于数值指标，统计值可以增加也可以减小。

## Histogram

Histogram 用于对指标进行采样观察，可以设置需要统计的分位值。在抓取时，Histogram 指标会返回多个时序。

- 观察桶的累计计数，指标名称为 `<basename>_bucket{le="<upper inclusive bound>"}`
- 所有采样数据值的总和，指标名称为 `<basename>_sum`
- 所有采样数据的总数，指标名称为 `<basename>_count` ，和 `<basename>_bucket{le="+Inf"}` 值一致

## Summary

和 Histogram 相似，Summary 对观察指标进行采样，在提供所有采用数据总数和值的总和的同时，在滑动窗口时间内计算可配置的分位数。在抓取时，Summary 指标会返回多个时序。

- 流式传输观察到的事件的 φ-分位数 (0 ≤ φ ≤ 1)，指标名称为 `<basename>{quantile="<φ>"}`
- 所有采样数据值的总和，指标名称为 `<basename>_sum`
- 所有采样数据的总数，指标名称为 `<basename>_count` 

# 对比

## Histogram & Summary

Histogram 和 Summary 都是采样观察，常用于请求耗时及响应大小统计。两者会统计样本数量以及样本值的总和，以便计算统计值的平均值。原则上，两者可用于观测有负值的指标，这种情况下观测值的总和可能会上下波动，不再使用 `rate()` 方法。对于这种场景如果想用 `rate()` ，可以用两个独立的 Summary 指标，一个统计整数，一个统计负数，然后再使用 PromQL 进行组合。

如果想统计最近五分钟的平均请求耗时，指标是 Summary 或者 Histogram 都可，指标名称为 `http_request_duration_seconds`，那么表达式如下。

```sql
 rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

### Apdex score

使用 Histogram 而不是用 Summary 的一个直接场景，是计算一个指标落入特定分桶样本数量的值。比如，有一个 SLO 指标，95% 的请求要在 300ms 内返回。配置一个包含 300ms 以上的分桶，可以直接表示 300ms 以内的相对请求数量，并且很容易地在值小于 0.95 时报警。下面的表达式可以计算 5 分钟内请求耗时在 300ms 以内的比例。

```sql
  sum(rate(http_request_duration_seconds_bucket{le="0.3"}[5m])) by (job)
/
  sum(rate(http_request_duration_seconds_count[5m])) by (job)
```

可以用同样的方式计算  [Apdex score](https://en.wikipedia.org/wiki/Apdex)。配置分桶，包含目标耗时（比如，0.3s）和最大容忍耗时（一般 4 倍于目标耗时，比如 1.2s），下面表达式可以计算 Apdex Score。

```sql
(
  sum(rate(http_request_duration_seconds_bucket{le="0.3"}[5m])) by (job)
+
  sum(rate(http_request_duration_seconds_bucket{le="1.2"}[5m])) by (job)
) / 2 / sum(rate(http_request_duration_seconds_count[5m])) by (job)
```

### 分位数（Quantiles）

Histogram 和 Summary 都可以计算 φ 分位数，0 ≤ φ ≤ 1。 φ 分位数是 N 个观察值排序后位于  φ * N 位置的数的值。两者计算分位数最重要的不同是，Summary 在客户端流式计算  φ 分位数并直接上传；Histogram 暴露分桶的观测值数量，在使用 [`histogram_quantile()`](https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile) 方法获取分位值时计算发生在 server 端。

| 项目               | Histogram                | Summary                                                      |
| ------------------ | ------------------------ | ------------------------------------------------------------ |
| 请求配置           | 选择符合观测值的合适分桶 | 选择想要的分位数，并设置时间窗口；其他分位数和时间窗口不能再通过表达式计算 |
| 客户端性能         | 高                       | 低                                                           |
| 服务端性能         | 低                       | 高                                                           |
| 时序数量           | 每个分桶一个时序         | 每个分位一个时序                                             |
| 分桶误差           | 受限于桶的宽度           | 受限于 φ 可配置值                                            |
| 指定分位和滑动窗口 | PramQL 表达式            | 客户端配置                                                   |
| 聚合               | PramQL 表达式            | 通常不可聚合                                                 |

注意聚合差异的重要性，重新回到 SLO 的问题，这次不再关注 300ms 以内请求的比例是否达到 95%，而是 95 分位本身（95% 的请求可以在多上时间返回）。为了达到这个目的，可以设置一个 Summary 并配置 95 分位，也可以设置一个 Histogram 并在 300ms 附近设置一部分分桶（比如 `{le="0.1"}`， `{le="0.2"}`， `{le="0.3"}`， 和 `{le="0.45"}`）。如果服务有多个实例，期望将结果聚合并得到一个整体的 95 分位值。那么，如果是 Summary 使用下面表达式计算平均值是没有意义的。

```sql
avg(http_request_duration_seconds{quantile="0.95"}) // BAD!
```

如果是 Histogram，可以使用下面的表达式。

```sql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) // GOOD.
```

通过对原始数据进行聚合，再计算分位值，是比较合理的。

# 文档

- [指标类型](https://prometheus.io/docs/concepts/metric_types/)
- [Histogram 和 Summary](https://prometheus.io/docs/practices/histograms/)

