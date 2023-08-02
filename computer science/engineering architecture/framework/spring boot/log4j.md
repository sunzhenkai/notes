---
title: spring boot - log4j
categories: 
  - [架构,框架,spring boot]
tags:
  - log4j
    - spring boot
date: 2021/05/12 00:00:00
update: 2021/05/12 00:00:00
---

# Dependency

```xml
<!-- exclude logback-classic -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
  <exclusions>
    <exclusion>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
    </exclusion>
  </exclusions>
</dependency>

<!-- add slf4j-log4j12 dependency -->
<dependency>
  <groupId>org.slf4j</groupId>
  <artifactId>slf4j-log4j12</artifactId>
  <version>1.7.30</version>
</dependency>
```

# Configuration

```properties
# root logger setup; [level], appenderName...
log4j.rootLogger=INFO, CL, FILE

# appender; consul
log4j.appender.CL=org.apache.log4j.ConsoleAppender
log4j.appender.CL.layout=org.apache.log4j.PatternLayout
log4j.appender.CL.layout.ConversionPattern=%-5p %c %x - %m%n

# appender; file
log4j.appender.FILE=org.apache.log4j.RollingFileAppender
log4j.appender.FILE.File=/tmp/eubalaena.log
log4j.appender.FILE.MaxFileSize=1MB
log4j.appender.FILE.MaxBackupIndex=15
log4j.appender.FILE.layout=org.apache.log4j.PatternLayout
log4j.appender.FILE.layout.ConversionPattern=%-5p %c %x - %m%n

log4j.logger.pub.wii=DEBUG, FILE
log4j.logger.org.springframework=INFO, FILE
log4j.logger.org.mybatis=INFO, FILE
org.mybatis.spring.mapper.ClassPathMapperScanner=OFF
```

