---
title: Thrift
categories: 
  - [架构, rpc, dsl]
tags:
  - Thrift
date: "2021-03-05T00:00:00+08:00"
update: "2021-03-05T00:00:00+08:00"
---

# 示例

## 序列化

```java
TSerializer serializer = new TSerializer(new TBinaryProtocol.Factory());
byte[] serialized = serializer.serialize(obj);
```

## 反序列化

```java
TDeserializer deserializer = new TDeserializer(new TBinaryProtocol.Factory());
deserializer.deserialize(obj, bytes);
```

