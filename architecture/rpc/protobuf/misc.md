---
title: protobuf - misc
categories: 
	- [架构, rpc, dsl]
tags:
	- protobuf
date: 2021/05/21 00:00:00
update: 2021/05/21 00:00:00
---

# maven

**打包插件**

```xml
<plugin>
  <groupId>org.xolstice.maven.plugins</groupId>
  <artifactId>protobuf-maven-plugin</artifactId>
  <executions>
    <execution>
      <goals>
        <goal>compile</goal>
        <goal>compile-custom</goal>
        <goal>test-compile</goal>
        <goal>test-compile-custom</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

# IDEA

**引用飘红**

把 proto 所在文件夹标记为 source root。