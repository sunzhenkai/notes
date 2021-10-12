---
title: kafka configuration
categories: 
    - [架构, mq, kafka]
tags:
    - kafka
date: 2021/10/12 00:00:00
update: 2021/10/12 00:00:00
---

# Producer

| 配置项                   | 单位        | 说明                                                         |
| ------------------------ | ----------- | ------------------------------------------------------------ |
| metadata.max.age.ms      | 毫秒        | 本地缓存的 meta 信息最大有效时间                             |
| send.buffer.bytes        | 字节(bytes) | TCP 发送缓存大小，-1 使用系统默认值                          |
| receive.buffer.bytes     | 字节(bytes) | TCP 接受缓存大小，-1 使用系统默认值                          |
| client.id                | -           | 向服务端发请求的客户端标识，主要用于 kafka 服务端落日志及 debug |
| reconnect.backoff.ms     | 毫秒        | 客户端重连 broker 的最小等待时间                             |
| reconnect.backoff.max.ms | 毫秒        | 每次重连失败会增加等待时间，直到此最大等待时间               |
| retries                  | -           | 消息发送失败重试次数                                         |
| retry.backoff.ms         | 毫秒        | 消息重发等待时间                                             |
| connections.max.idle.ms  | 毫秒        | 限制连接最大空闲时间                                         |
| request.timeout.ms       | 毫秒        | 请求超时时间                                                 |
| batch.size               | 字节(bytes) | 设置批量发送消息时每条消息最大字节数，设置 0 禁用批量发送消息 |
| acks                     | -           | 设置 kafka 集群 leader 需要多少 ack 才认为消息发送成功，设置 0 标识 |

