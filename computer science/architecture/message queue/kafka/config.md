---
title: kafka configuration
categories: 
    - [架构, mq, kafka]
tags:
    - kafka
date: 2021/10/12 00:00:00
update: 2021/10/12 00:00:00
---

# Common

| 配置项               | 单位        | 说明                                |
| -------------------- | ----------- | ----------------------------------- |
| bootstrap.servers    | -           | brokers 列表，多个服务器 `,` 分隔   |
| metadata.max.age.ms  | 毫秒        | 本地缓存的 meta 信息最大有效时间    |
| send.buffer.bytes    | 字节(bytes) | TCP 发送缓存大小，-1 使用系统默认值 |
| receive.buffer.bytes | 字节(bytes) | TCP 接受缓存大小，-1 使用系统默认值 |

# Producer

| 配置项                                | 单位        | 说明                                                         |
| ------------------------------------- | ----------- | ------------------------------------------------------------ |
| client.id                             | -           | 向服务端发请求的客户端标识，主要用于 kafka 服务端落日志及 debug |
| reconnect.backoff.ms                  | 毫秒        | 客户端重连 broker 的最小等待时间                             |
| reconnect.backoff.max.ms              | 毫秒        | 每次重连失败会增加等待时间，直到此最大等待时间               |
| retries                               | -           | 消息发送失败重试次数；设置大于 0 的值，会触发客户端遇到错误后重新发送消息；设置 retries 且 max.in.flight.requests.per.connection > 1 可能会导致消息重排序 |
| retry.backoff.ms                      | 毫秒        | 消息重发等待时间                                             |
| connections.max.idle.ms               | 毫秒        | 限制连接最大空闲时间                                         |
| request.timeout.ms                    | 毫秒        | 请求超时时间；应大于 replica.lag.time.max.ms (broker配置) 的值 |
| batch.size                            | 字节(bytes) | 设置批量发送消息时每条消息最大字节数，设置 0 禁用批量发送消息 |
| acks                                  | -           | 设置 kafka 集群 leader 需要多少 ack 才认为消息发送成功；设置 0，producer 不等待确认，消息写入发送缓存，这种情况下不保证服务端接收到消息，retries 配置不生效，offset 返回值总是 -1；设置 1，kafka leader 消息写入日志文件后发送确认消息，不等待 followers 数据写入确认，如果 leader down 掉可能会出现消息丢失；设置 all 或 -1，kafka leader 等待所有 follower 确认写入后，再发送确认消息。 |
| linger.ms                             | 毫秒        | 设置徘徊等待时间，消息到达后不是立即发送给消费者，而是等待一段时间，以便聚合更到消息，批量发送；如果达到 batch.size 的限制，则会忽略该配置立即发送；默认是0，不启用消息徘徊等待 |
| max.request.size                      | 字节(bytes) | 一个请求的最大字节数；服务器可能用不同的方式来计算 batch size |
| max.block.ms                          | 毫秒        | 控制 `KafkaProducer.send()` 和 `KafkaProducer.partitionsFor()` 的阻塞时间，这两个方法可能会因为缓存满或元数据不可用阻塞 |
| buffer.memory                         | 字节(bytes) | producer 用于发送消息缓存的全部字节数，不仅缓存消息，还有处理中的请求、压缩后的消息 |
| compression.type                      | -           | 压缩类型；none、gzip、snappy、lz4                            |
| max.in.flight.requests.per.connection | -           | 每个连接允许的最大正在处理（未收到确认）请求数，超过之后会阻塞；如果设置的值大于 1，那么存在因为消息发送失败及启用 retries 导致的消息重排序的问题（比如 message1 先发送且失败，message2 后发送且成功，message1 会因为重试机制再次发送且后于 message2 确认） |
| key.serializer                        | -           | key 的序列化类，实现 org.apache.kafka.common.serialization.Serializer 接口 |
| value.serializer                      | -           | value 的序列化类，实现 org.apache.kafka.common.serialization.Serializer 接口 |
| partitioner.class                     | -           | 分区类，实现 org.apache.kafka.clients.producer.Partitioner 接口 |
| interceptor.classes                   | -           | 拦截器类，实现 org.apache.kafka.clients.producer.ProducerInterceptor 接口；允许在发送给 cluster 前拦截 producer 的消息；默认没有拦截器 |
| enable.idempotence                    | -           | 幂等性设置；设置 true 会保证消息只被写入一次，前提配置是 enable.idempotence <= 5，retries > 0，acks = all；如果设为 false，则可能会出现一条消息因为重试写入多次 |
| transaction.timeout.ms                | 毫秒        | 事务协作者等待事务状态更新的超时时间                         |
| transactional.id                      | -           | 用于事务投递，如果配置，则必须开启 enable.idempotence，默认是 null，不能使用事务 |

# Consumer

| 配置项                        | 单位 | 说明                                                         |
| ----------------------------- | ---- | ------------------------------------------------------------ |
| group.id                      | -    | 消费组                                                       |
| max.poll.records              | -    | 单次调用 `poll()`  返回的最大消息条数                        |
| max.poll.interval.ms          | 毫秒 | 使用消费组管理时，触发`poll()` 的最大间隔时间                |
| session.timeout.ms            | 毫秒 | 消费者存活周期；使用组管理设施时，消费者定期发送心跳延长 broker 保存的存活时间，如果超过该项设置的时间没有收到心跳请求，broker 会移除 consumer 并 rebalance；值必须是 broker 允许的值，在 `group.min.session.timeout.ms` 和 `group.max.session.timeout.ms` （broker 配置）之间 |
| heartbeat.interval.ms         | 毫秒 | 心跳请求发送周期；该值一般不应大于 `session.timeout.ms` 的 1/3 |
| enable.auto.commit            | -    | 如果为 true，消费者的 offset 会在后台定期提交                |
| auto.commit.interval.ms       | 毫秒 | 消费者定期提交 offset 的间隔                                 |
| partition.assignment.strategy | -    | 类名，消费者使用的分区分配策略                               |
| auto.offset.reset             | -    | 没有初始的 offset 信息时消息消费策略；earliest，从最早的 offset 消费；latest，从新的消息开始消费；none，如果没有设置消费组 offset 则抛出异常 |
| fetch.min.bytes               | 字节 | 拉取请求 server 返回的最小字节数；不足则等待足够的消息再返回，默认为1，只要有消息则立即返回 |
| fetch.max.bytes               | 字节 | 拉取请求 server 返回的最大字节数；并不是一个绝对最大值，还受其他配置影响，比如 max.message.bytes，默认 50 MB |
| fetch.max.wait.ms             | 毫秒 | 服务响应拉取请求的最大阻塞时间                               |
| max.partition.fetch.bytes     | 毫秒 | 拉取请求，每个分区返回的最大字节数，默认 1 MB                |
| client.id                     | -    | 向服务端发请求的客户端标识，主要用于 kafka 服务端落日志及 debug |
| check.crcs                    | -    | 开启 CRC32 检查                                              |
| key.deserializer              | -    | key 反序列化类，实现 org.apache.kafka.common.serialization.Deserializer 接口 |
| value.deserializer            | -    | key 反序列化类，实现 org.apache.kafka.common.serialization.Deserializer 接口 |
| default.api.timeout.ms        | 毫秒 | consumer API 的默认超时时间                                  |
| interceptor.classes           | -    | 拦截器类，实现 org.apache.kafka.clients.consumer.ConsumerInterceptor 接口 |
| exclude.internal.topics       | -    | 内部 topic 消息是否暴露给消费者；如果为 true，唯一可以从内部 topic 获取消息的方式是订阅它 |
| internal.leave.group.on.close | -    | consumer 关闭时是否退出消费组；如果为 false，则消费者关闭后不会触发 rebalance，知道 `session.timeout.ms` 过期 |
| isolation.level               | -    | 控制读取事务消息的方式；read_committed，`consumer.poll()` 只返回提交了的事务消息；read_uncommitted，返回所有消息，包括被废弃的事务消息；对于非事务消息，两种方式会无条件返回；默认是 read_uncommitted |

# 其他

## 幂等性

producer 设置 `enable.idempotence` 为 true，kafka 会保证消息按顺序且不重复的送达。

### 原理

每个 producer 被分配一个 PID（producer id），向 broker 发送消息时会带上，且每个消息有一个单调递增的序列号，生产者为主题的每个分区维护一个序列号，broker 同样记录 producer 的最大消息序列号，只接受 +1 的消息。

# 参考

- https://www.cloudkarafka.com/blog/apache-kafka-idempotent-producer-avoiding-message-duplication.html