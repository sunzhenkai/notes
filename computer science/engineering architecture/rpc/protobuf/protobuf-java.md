---
title: protobuf - java
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

# 对比

## StringValue & string

类似的还有 `int32 & Int32Value` 等。

`StringValue` 和 `string` 相比：

- StringValue 可以为 null，在部分语言中，string 类型数据不能为 null，那么对于 string 类型，无法区分 `""` 是代表 null 还是空字符串
- gRPC 调用过程的的参数和返回值不能为基本类型，也就是不能为 string、int32 这种

