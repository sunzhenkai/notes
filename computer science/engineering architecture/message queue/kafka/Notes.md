---
title: kafka notes
categories: 
    - [架构, mq, kafka]
tags:
    - kafka
date: "2021-09-24T00:00:00+08:00"
update: "2021-09-24T00:00:00+08:00"
---

# 基础

- 架构
  - 介绍
    - [Ref](https://blog.csdn.net/lp284558195/article/details/80297208)
  - Rebalance
    - Why
      - 是Kafka集群的一个保护设置，用于剔除掉无法消费或过慢的消费者
      - 负载均衡
    - When
      - new consumer
      - consumer offline / exit / dead / unsubscribe
      - 消费者订阅的topic出现分区数量变化
    - 影响
      - 重复消费
      - Rebalance扩散到整个ConsumerGroup，一个Consumer的退出，导致Group进行Rebalance，影响面大
      - 频繁的Rebalance导致重复消费及Rebalance占用大量时间
      - 数据不能及时消费，会累计lag（消费滞后），在Kafka的TTL之后会丢弃数据
    - improve
      - 关闭 auto commit，手动管理offset和心跳
    - Rebalance Listener
      - [Ref](https://www.learningjournal.guru/courses/kafka/kafka-foundation-training/rebalance-listener/)
    - more
      - [Ref](https://www.cnblogs.com/huxi2b/p/6223228.html)
- 名词

  - Broker
    - 消息中间件处理节点
    - 一个Kafka节点就是一个broker
    - 一个或多个Kafka节点组成Kafka集群
  - Topic
    - Kafka根据Topic对消息进行归类
    - 发布到Kafka集群的每条消息都需要指定一个topic
  - Producer
    - 参数
      - Topic
      - Partition（Optional）
      - Key（Optional）
      - Value
  - Consumer
    - 一个Consumer可以消费一个或多个partition
  - ConsumerGroup
    - 每个Consumer属于一个特定的ConsumerGroup
    - 一条消息可以发送到多个不同的ConsumerGroup
    - 一个ConsumerGroup中的一条消息只被一个Consumer处理
    - 仅是用来对消费者进行分组来消费topic的消息
  - Partition
    - 物理上的概念
    - 一个topic的信息可以划分到多个partition
    - 每个partition内部是有序的
    - 每个partition在存储层面是append log文件
    - 顺序写磁盘，效率非常高，这是Kafka高吞吐量的重要保证
    - partition是broker属性，不影响producer
  - Segment
    - partition细分的物理概念
    - 包括：
      - `.index`文件
      - `.log`文件
    - [Ref](https://blog.csdn.net/lp284558195/article/details/80297208)
  - Offset
    - 发布到partition的消息被追加到log文件的尾部
    - 每条消息在partition文件中的位置成为offset
    - offset是一个整形数字，唯一标记一条消息
  - Leader & Follower
    - 为了提高消息可靠性，Kafka为每个topic的partition设置N个副本
    - N 副本中的一个选举为Leader，其他为Follower
    - Leader处理partition的所有读写请求，follower定期复制leader上的数据
    - 负责维护和跟踪ISR（副本同步队列）中所有follower滞后的状态
    - producer发送一条消息到broker后，leader写入消息并复制到所有follower
- 如何提高可靠性

  - 通过request.required.acks参数设置数据可靠性级别
    - 1：producer接受到leader成功收到数据并得到确认后发送下一条数据
      - 如果leader宕机，消息未同步到follower，可能会造成数据丢失
    - 0：producer无需等待来自broker的确认而继续发送下一条消息，可靠性最低
    - -1：producer等待ISR中所有follower都确认接收到数据才算一次发送成功，可靠性最高
      - 如果设置副本为1，也就是说只有leader，此时和设置`request.required.acks`等效，如果leader宕机，也会发生数据丢失
  - 保证高可靠性
    - topic的配置：replication.factor>=3,即副本数至少是个;2<=min.insync.replicas<=replication.factor
    - broker的配置：leader的选举条件unclean.leader.election.enable=false
    - producer的配置：request.required.acks=-1(all)，producer.type=sync
- 应用
  - 日志收集
  - 业务数据收集
  - page view
  - ...
- Ref
  - [Ref 1](https://sq.163yun.com/blog/article/185482391401111552)
  - [Ref 2](https://blog.csdn.net/lp284558195/article/details/80297208)
  - [Ref 3](http://www.infoq.com/cn/articles/kafka-analysis-part-4)

# 读取消息示例

```scala
val props = new Properties()
props.setProperty("group.id", "-")
props.setProperty("bootstrap.servers", "-")
props.setProperty("auto.offset.reset", "-")
props.put("key.deserializer", classOf[StringDeserializer])
props.put("value.deserializer", classOf[StringDeserializer])
props.put("partition.assignment.strategy", "org.apache.kafka.clients.consumer.RangeAssignor")
val consumer = new KafkaConsumer[String, String](props)
consumer.subscribe(List(topic))
while (true) {
  val results = consumer.poll(2000)
  for (record <- results.iterator()) {
    print(s"${record.key()} - ${record.value()}")
  }
}
```

