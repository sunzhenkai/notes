---
title: redis usage
categories: 
  - [架构, 存储, redis]
tags:
  - 架构
  - 存储
date: 2022/02/23 00:00:00
update: 2022/02/23 00:00:00
---

# 登录

```shell
$ redis-cli -h <host> -p <port>
```

# 查询

## 集群信息

```shell
# 集群信息
> cluster info
# 节点信息
> cluster nodes 
# 内存信息
> info memory
```

# 导出数据

## redis-cli

- https://redis.io/topics/rediscli#remote-backups-of-rdb-files

## redis-shake

- https://github.com/alibaba/RedisShake

```shell
./redis-shake.linux -type=dump -conf=redis-shake.conf

```

> redis-shake.conf 配置参考[这里](https://github.com/alibaba/RedisShake/wiki/%E7%AC%AC%E4%B8%80%E6%AC%A1%E4%BD%BF%E7%94%A8%EF%BC%8C%E5%A6%82%E4%BD%95%E8%BF%9B%E8%A1%8C%E9%85%8D%E7%BD%AE%EF%BC%9F)。

# 搭建集群

```shell
nohup redis-server --cluster-enabled yes --port 6379 --cluster-config-file nodes1.conf &
nohup redis-server --cluster-enabled yes --port 6378 --cluster-config-file nodes2.conf &
nohup redis-server --cluster-enabled yes --port 6377 --cluster-config-file nodes3.conf &

sleep 3 # 等服务节点起来
redis-cli --cluster create 127.0.0.1:6379 127.0.0.1:6378 127.0.0.1:6377
```

> nodes1.conf、nodes1.conf、nodes1.conf 可以不存在，运行后 redis 自动创建。不同的 redis 实例，需要绑定不同的配置文件，默认为 node.conf。