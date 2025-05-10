---
title: spring boot maven
categories: 
  - [架构,java,框架,spring boot]
tags:
  - spring boot
date: "2021-09-06T00:00:00+08:00"
update: "2021-09-06T00:00:00+08:00"
---

# 单个可执行 jar 包

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>3.3.0</version>
    <configuration>
        <archive>
            <manifest>
                <mainClass>pub.wii.cook.springboot.CookSpringBootApplication</mainClass>
            </manifest>
        </archive>
        <descriptors> <!-- 会被忽略 -->
            <descriptor>src/assemble/assembly.xml</descriptor>
        </descriptors>
    </configuration>
    <executions>
        <execution>
            <id>make-assembly</id> <!-- this is used for inheritance merges -->
            <phase>package</phase> <!-- bind to the packaging phase -->
            <goals>
                <goal>single</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

**assemble.xml**

```xml
<assembly xmlns="http://maven.apache.org/ASSEMBLY/2.1.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/ASSEMBLY/2.1.0
            http://maven.apache.org/xsd/assembly-2.1.0.xsd">
    <id>jar-with-dependencies</id>
    <formats>
        <format>jar</format>
    </formats>

    <includeBaseDirectory>false</includeBaseDirectory>
    <dependencySets>
        <dependencySet>
            <outputDirectory>/</outputDirectory>
            <useProjectArtifact>true</useProjectArtifact>
            <unpack>true</unpack>
            <scope>runtime</scope>
        </dependencySet>
    </dependencySets>

    <containerDescriptorHandlers>
        <containerDescriptorHandler>
            <handlerName>metaInf-services</handlerName>
        </containerDescriptorHandler>
        <containerDescriptorHandler>
            <handlerName>metaInf-spring</handlerName>
        </containerDescriptorHandler>
        <containerDescriptorHandler>
            <handlerName>plexus</handlerName>
        </containerDescriptorHandler>
    </containerDescriptorHandlers>
</assembly>
```
