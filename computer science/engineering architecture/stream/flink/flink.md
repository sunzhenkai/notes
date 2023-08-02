---
title: flink
categories: 
  - [架构,stream,flink]
tags:
  - flink
date: 2022/07/07 00:00:00
---

# Protobuf

## 设置自定义序列化

**引入依赖**

```xml
<dependency>
	<groupId>com.twitter</groupId>
	<artifactId>chill-protobuf</artifactId>
	<version>0.10.0</version>
</dependency>
```

**设置自定义序列化类**

```scala
import com.twitter.chill.protobuf.ProtobufSerializer

env.getConfig.registerTypeWithKryoSerializer(classOf[PbMessage], classOf[ProtobufSerializer])
```

# 参数

```shell
-m    address of job manager which to connect
-d    detached mode
-yd   yarn detached mode
-ynm  yarn application name
-yn   number of yarn container to allocate = Number of Task Managers
-ys   Number of slots per TaskManager
-yjm  Memory for JobManager Container with optional unit (default: MB)
-ytm  Memory per TaskManager Container with optional unit (default: MB)
-p    The parallelism with which to run the program.
-c    class to run
```

