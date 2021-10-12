---
title: kafka commend line tools
categories: 
    - [架构, mq, kafka]
tags:
    - kafka
date: 2021/09/24 00:00:00
update: 2021/09/24 00:00:00
---

# list topic

```shell
$ ./bin/kafka-topics.sh --list --zookeeper server.zk
__consumer_offsets
demo_kafka_topic_1
model_diff_update_111
model_diff_update_156
model_diff_update_785
model_diff_update_802

# 示例
$ ./bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181
```

# 清空 topic

```shell
kafka-configs.sh --zookeeper <zkhost>:2181 --alter --entity-type topics --entity-name <topic name> --add-config retention.ms=1000
```

# 查看 topic 的 partition 信息

```shell
$ ./bin/kafka-topics.sh --zookeeper c3cloudsrv.zk.hadoop.srv:11000/kafka/c3cloudsrv-feeds --describe --topic model_diff_update_111
Topic:model_diff_update_111	PartitionCount:1	ReplicationFactor:1	Configs:retention.ms=300000
	Topic: model_diff_update_111	Partition: 0	Leader: 1	Replicas: 1	Isr: 1
```

# 消费

```shell
$ ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic <topic> --from-beginning
$ ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic <topic> # 默认最新消息开始消费
```

# 删除 topic

```shell
$ ./bin/kafka-topics --delete --zookeeper 127.0.0.1:2181 --topic <topic-name>
```

