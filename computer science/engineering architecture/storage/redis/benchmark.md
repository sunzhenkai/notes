---
title: redis benchmark
categories: 
  - [架构, 存储, redis]
tags:
  - 架构
  - 存储
date: 2021/03/23 00:00:00
update: 2020/03/23 00:00:00
---

# 工具

针对 redis 的 benchmark，可使用 redis 自带的  `redis-benchmark` 工具。

# redis-benchmark

## 命令及参数

```shell
# 命令
$ redis-benchmark [option] [option value]
```

### 参数

| 参数  | 说明                                       | 默认值    | 示例      |
| ----- | ------------------------------------------ | --------- | --------- |
| -h    | 主机                                       | 127.0.0.1 |           |
| -p    | 端口                                       | 6379      |           |
| -a    | 密码                                       |           |           |
| -s    | 指定服务器socket                           |           |           |
| -c    | 客户端并发连接数                           | 50        |           |
| -n    | 请求数                                     | 10000     |           |
| -d    | 以字节的形式指定 SET/GET 值的数据大小      | 2         |           |
| -k    | 连接保持，1=keep alive 0=reconnect         | 1         |           |
| -r    | SET/GET/INCR 使用随机 key, SADD 使用随机值 |           |           |
| -P    | 通过管道传输 `<numreq>` 请求               | 1         |           |
| -q    | 强制退出 redis，仅显示 query/sec 值        |           |           |
| --csv | 以 CSV 格式输出                            |           |           |
| -l    | 生成循环，永久执行测试                     |           |           |
| -t    | 仅运行以逗号分隔的测试命令列表             |           | set,lpush |
| -l    | Idle 模式，仅打开 N 个 idle 连接并等待     |           |           |

### 示例

```shell
$ redis-benchmark -h <host> -p <port> -t set -n 100000 -d 1024 -a <password>
```

