---
title: spark read s3
categories: 
	- [big data, spark]
tags:
	- spark
date: 2022/06/04 00:00:00
update: 2022/06/04 00:00:00
---

# pyspark

## 安装

```shell
pip3 install pyspark
```

## 读取 s3 数据

```python
# 创建 spark session
from pyspark.sql import SparkSession
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.amazonaws:aws-java-sdk-pom:1.12.153,org.apache.hadoop:hadoop-aws:3.2.2,org.apache.hadoop:hadoop-client:3.2.2 pyspark-shell'
spark = SparkSession.builder.master("local[1]").appName("sample").getOrCreate()

# 从本地读取 aws 认证信息
import configparser
from pathlib import Path
import os
config = configparser.ConfigParser()
config.read(os.path.join(Path.home(), '.aws/credentials'))
access_key_id = config.get('default', 'aws_access_key_id')
secret_access_key = config.get('default', 'aws_secret_access_key')

# 设置 spark context
spark._jsc.hadoopConfiguration().set('fs.s3a.access.key', access_key_id)
spark._jsc.hadoopConfiguration().set('fs.s3a.secret.key', secret_access_key)
spark._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
spark._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
spark._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")

# 读取文件
sample_file = "s3a://<bucket>/path/to/file"
data = spark.read.text(sample_file)

# 解析记录 (pb)
import base64
from google.protobuf.json_format import MessageToJson
import sample_pb2

def decode_pb(row):
    decoded_data = base64.b64decode(row.value)
    tr = sample_pb2.Example()
    tr.ParseFromString(decoded_data)
    return [MessageToJson(tr)]
  
# spark 任务
result = data.rdd.map(decode_pb).toDF(["value"])
result.show(1, False)
```

# scala

```scala
// 创建 Spark Session
val spark: SparkSession = SparkSession.builder()
	.master("local[1]")
	.appName("queue_pb_log")
	.getOrCreate()

// 读取 s3 认证信息
val cf = Paths.get(System.getProperty("user.home"), ".aws/credentials")
val c = new Ini(new File(cf.toUri))
val prefs = new IniPreferences(c)
val awsAccessKeyId = prefs.node("default").get("aws_access_key_id", "no")
val awsSecretAccessKey = prefs.node("default").get("aws_secret_access_key", "no")

// 设置 spark context
spark.sparkContext.hadoopConfiguration.set("fs.s3a.access.key", awsAccessKeyId)
spark.sparkContext.hadoopConfiguration.set("fs.s3a.secret.key", awsSecretAccessKey)
spark.sparkContext.hadoopConfiguration.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
spark.sparkContext.hadoopConfiguration.set("com.amazonaws.services.s3.enableV4", "true")
spark.sparkContext.hadoopConfiguration.set("fs.s3a.aws.credentials.provider",
"com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")

// 读取日志
val sampleFile = "s3a://<bucket>/path/to/file"
val src = spark.sparkContext.textFile(sampleFile)
val result = src.map(record => {
  // 解析 pb 日志
  val parsed = Example.parseFrom(Base64.getDecoder.decode(record))
  JsonFormat.printer().print(parsed)
})

println(result.first())
```

## pom

```xml
<dependency>
  <groupId>org.apache.hadoop</groupId>
  <artifactId>hadoop-common</artifactId>
  <version>2.7.3</version>
</dependency>

<dependency>
  <groupId>org.apache.hadoop</groupId>
  <artifactId>hadoop-aws</artifactId>
  <version>2.7.3</version>
</dependency>
<!-- https://mvnrepository.com/artifact/org.apache.spark/spark-core -->
<dependency>
  <groupId>org.apache.spark</groupId>
  <artifactId>spark-core_2.11</artifactId>
  <version>2.4.8</version>
</dependency>

<!-- https://mvnrepository.com/artifact/org.apache.spark/spark-core -->
<dependency>
	<groupId>org.apache.spark</groupId>
	<artifactId>spark-core_2.11</artifactId>
	<version>2.4.8</version>
</dependency>
<!-- https://mvnrepository.com/artifact/org.apache.spark/spark-sql -->
<dependency>
	<groupId>org.apache.spark</groupId>
	<artifactId>spark-sql_2.11</artifactId>
	<version>2.4.8</version>
  <!-- 本地运行 -->
	<!-- <scope>compile</scope> -->
  <!-- 远程提交 -->
	<!-- <scope>provided</scope> -->
</dependency>
<!-- https://mvnrepository.com/artifact/org.ini4j/ini4j -->
<dependency>
  <groupId>org.ini4j</groupId>
  <artifactId>ini4j</artifactId>
  <version>0.5.4</version>
</dependency>

<!-- 其他 如果版本有冲突可以尝试 -->
<properties>
  <scala.version>2.11.6</scala.version>
  <jackson.version>2.11.4</jackson.version>
</properties>

<dependency>
  <groupId>com.fasterxml.jackson.module</groupId>
  <artifactId>jackson-module-scala_2.11</artifactId>
  <version>${jackson.version}</version>
</dependency>

<!-- https://mvnrepository.com/artifact/com.fasterxml.jackson.module/jackson-module-scala -->
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-core</artifactId>
  <version>${jackson.version}</version>
</dependency>

<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-annotations</artifactId>
  <version>${jackson.version}</version>
</dependency>

<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
  <version>${jackson.version}</version>
</dependency>

<dependency>
  <groupId>org.apache.httpcomponents</groupId>
  <artifactId>httpclient</artifactId>
  <version>4.3.3</version>
</dependency>

<!-- protobuf 相关 -->
<properties>
	<protobuf.version>3.7.1</protobuf.version>
</properties>

<dependency>
  <groupId>com.google.protobuf</groupId>
  <artifactId>protobuf-java</artifactId>
  <version>${protobuf.version}</version>
</dependency>
<dependency>
  <groupId>com.google.protobuf</groupId>
  <artifactId>protobuf-java-util</artifactId>
  <version>${protobuf.version}</version>
</dependency>

<build>
  <extensions>
    <extension>
      <groupId>kr.motd.maven</groupId>
      <artifactId>os-maven-plugin</artifactId>
      <version>1.6.1</version>
    </extension>
  </extensions>
  <plugins>
		<plugin>
      <groupId>org.xolstice.maven.plugins</groupId>
      <artifactId>protobuf-maven-plugin</artifactId>
      <version>0.6.1</version>
      <extensions>true</extensions>
      <configuration>
        <!--                    <protocExecutable>protoc</protocExecutable>-->
        <protocArtifact>com.google.protobuf:protoc:${protobuf.version}:exe:${os.detected.classifier}</protocArtifact>
      </configuration>
      <executions>
        <execution>
          <goals>
            <goal>compile</goal>
            <goal>test-compile</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

