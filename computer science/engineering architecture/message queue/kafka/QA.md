---
title: kafka QA
categories: 
    - [架构, mq, kafka]
tags:
    - kafka
date: "2021-09-24T00:00:00+08:00"
update: "2021-09-24T00:00:00+08:00"
---

- consumer 和 consumer group的关系？
  - 一个用户属于一个 consumer group
- consumer group 和 topic 的关系？
  - consumer group保存自己的offset
  - 不同consumer group消费同一topic时，会消费同样的内容，各个group保存自己的offset
- topic 和 partition 的关系？
  - topic 和 partition 不在一个抽象层次
  - 一个 topic 的消息会被划分到多个partition（如果partion数量被设定 > 1）
- consumer group 和 partition 的关系？
  - 同样，consumer group 和 partition 也不在一个抽象层次
- partition 和 replication 的关系？
  - 没关系
- 怎么指定partition？
  - 不允许使用 producer api 设置partition数量
  - 每个topic的partition数量根据配置文件中的`num.partitioins` 指定

