---
title: kafka commend line tools
categories: 
    - [架构, mq, kafka]
tags:
    - kafka
date: "2021-09-24T00:00:00+08:00"
update: "2021-09-24T00:00:00+08:00"
---

[toc]

# list consumer groups

```shell
# 列出所有 consumer group
./bin/kafka-consumer-groups.sh --bootstrap-server $bootstrap_servers --list
```

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

# 查看 topic 信息

```shell
$ ./bin/kafka-topics.sh --zookeeper c3cloudsrv.zk.hadoop.srv:11000/kafka/c3cloudsrv-feeds --describe --topic model_diff_update_111
Topic:model_diff_update_111	PartitionCount:1	ReplicationFactor:1	Configs:retention.ms=300000
	Topic: model_diff_update_111	Partition: 0	Leader: 1	Replicas: 1	Isr: 1
```

```shell
$ kafka-topics --zookeeper 127.0.0.1:2181 --describe --topic <topic-name>
```

# 消费

```shell
$ ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic <topic> --from-beginning
$ ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic <topic> # 默认最新消息开始消费

# oom 异常, 设置 KAFKA_HEAP_OPTS="-Xms512m -Xmx1g"
$ env KAFKA_HEAP_OPTS="-Xms512m -Xmx1g" ./bin/kafka-console-consumer.sh --bootstrap-server <bootstrap-servers> --topic <topic> --from-beginning
```

## 指定配置文件

`kafka-auth.properties`

```ini
security.protocol        = "ssl"
ssl.ca.location          = "ca_cert.pem"
ssl.certificate.location = "client_cert.pem"
ssl.key.location         = "client_cert_key.pem"
ssl.key.password         = "password"
```

```shell
# 指定配置文件
## consumer
... --consumer.config kafka-auth.properties
## producer
... --producer.config kafka-auth.properties
```

参考

- [REF 1](https://docs.cloudera.com/HDPDocuments/HDP3/HDP-3.1.0/configuring-wire-encryption/content/configuring_kafka_producer_and_kafka_consumer.html)

## 环境变量指定认证

```shell
CONNECT_CONSUMER_SECURITY_PROTOCOL: SASL_SSL
CONNECT_CONSUMER_SASL_KERBEROS_SERVICE_NAME: "kafka"
CONNECT_CONSUMER_SASL_JAAS_CONFIG: com.sun.security.auth.module.Krb5LoginModule required \
                            useKeyTab=true \
                            storeKey=true \
                            keyTab="/etc/kafka-connect/secrets/kafka-connect.keytab" \
                            principal="<principal>;
CONNECT_CONSUMER_SASL_MECHANISM: GSSAPI
CONNECT_CONSUMER_SSL_TRUSTSTORE_LOCATION: <path_to_truststore.jks>
CONNECT_CONSUMER_SSL_TRUSTSTORE_PASSWORD: <PWD>
```



# 发送消息

```shell
$ /bin/kafka-console-producer.sh --broker-list localhost:9092 --topic <topic>
```

# 删除 topic

```shell
$ ./bin/kafka-topics --delete --zookeeper 127.0.0.1:2181 --topic <topic-name>
```

