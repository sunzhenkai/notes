---
title: spring kafka
categories: 
    - [架构, mq, kafka]
tags:
    - kafka
date: 2021/09/24 00:00:00
update: 2021/09/24 00:00:00
---

# 连接 Kafka

```java
// 连接 kafka
@Bean
public KafkaAdmin admin() {
    Map<String, Object> configs = new HashMap<>();
    configs.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, "127.0.0.1:9092");
    return new KafkaAdmin(configs);
}
```

# 管理 Topic

```java
@Bean
public NewTopic divinerInternalStrategyOperation() {
    return TopicBuilder.name("example-topic")
            .partitions(1)
            .replicas(1)
            .compact()
            .build();
}
```

# 订阅 topic 

```java
@KafkaListener(id = "consumer-group", topics = "diviner_internal_strategy_operation")
public void listen(String in) {
    // ...
}
```

# 发送消息

```java
@Autowired
private KafkaTemplate<Object, Object> template;
 
template.send(key, value);
```

# 参考

- https://docs.spring.io/spring-kafka/reference/html/
- [bean 冲突](https://stackoverflow.com/questions/43142295/problems-adding-multiple-kafkalistenercontainerfactories/43142573)

