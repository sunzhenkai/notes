---
title: 合并依赖包内 META-INF
categories:  
  - [工具,maven]
tags:
  - maven
date: "2021-08-23T00:00:00+08:00"
update: "2021-08-23T00:00:00+08:00"
---

# 打包成单体 jar 包

在很多场景下，需要将程序及依赖打包为单个 jar 包，方便部署、运行。打包成单体 jar 包，有多个插件可选，比如 `maven-shade-plugin`、`maven-assembly-plugin`。


# 合并 META-INF/services

以 gRPC 为例，我们有一个依赖包，里面自定义了 NameResolver。

```shell
# META-INF/services/io.grpc.NameResolverProvider
pub.wii.cook.governance.nameresolver.DynamicNameResolverProvider
```

如果我们恰巧引用了另外一个依赖包（jetcd-core），里面定义了其他的 NameResolver。

```shell
# META-INF/services/io.grpc.NameResolverProvider
io.etcd.jetcd.resolver.DnsSrvResolverProvider
io.etcd.jetcd.resolver.IPResolverProvider
```

那么，在我们打包成单体 jar 时，将两个依赖包内的 `META-INF/services/io.grpc.NameResolverProvider` 合并为一个，这样打包后的程序在运行时才可以通过 SPI 机制，找到所有的扩展。

```shell
# 期望的打包后 META-INF/services/io.grpc.NameResolverProvider
io.etcd.jetcd.resolver.DnsSrvResolverProvider
io.etcd.jetcd.resolver.IPResolverProvider
pub.wii.cook.governance.nameresolver.DynamicNameResolverProvider
```

无论  `maven-shade-plugin` 还是 `maven-assembly-plugin`，默认配置都不支持合并，需要单独配置。

对于 `maven-shade-plugin` ，需要添加 transformer。

```xml
<transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
```

对于 `maven-assembly-plugin` ，需要添加组装描述文件 `assembly.xml`，并启用 handler `metaInf-services`。

```xml
<!-- assembly.xml -->
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
    </containerDescriptorHandlers>
</assembly>
```

# 配置示例

 `maven-shade-plugin` 和 `maven-assembly-plugin` 配置，二选一。

## maven-shade-plugin

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>3.2.4</version>
    <configuration>
        <filters>
            <filter>
                <artifact>*:*</artifact>
                <excludes>
                    <exclude>META-INF/*.SF</exclude>
                    <exclude>META-INF/*.DSA</exclude>
                    <exclude>META-INF/*.RSA</exclude>
                </excludes>
            </filter>
        </filters>
    </configuration>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>shade</goal>
            </goals>
            <configuration>
                <transformers>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <mainClass>pub.wii.cook.Main</mainClass>
                    </transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>
```

## maven-assembly-plugin

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>3.3.0</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>single</goal>
            </goals>
            <configuration>
                <descriptors>
                    <descriptor>src/assemble/assembly.xml</descriptor>
                </descriptors>
                <archive>
                    <manifest>
                        <mainClass>pub.wii.cook.Main</mainClass>
                    </manifest>
                </archive>
            </configuration>
        </execution>
    </executions>
</plugin>
```

**assembly.xml**

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
    </containerDescriptorHandlers>
</assembly>
```

# 参考

- https://stackoverflow.com/questions/47310215/merging-meta-inf-services-files-with-maven-assembly-plugin
- https://segmentfault.com/a/1190000016237395
- https://stackoverflow.com/questions/38548271/difference-between-maven-plugins-assembly-plugins-jar-plugins-shaded-plugi
- https://github.com/apache/maven-assembly-plugin/blob/master/src/main/resources/assemblies/jar-with-dependencies.xml
- https://maven.apache.org/plugins/maven-shade-plugin/examples/executable-jar.html
