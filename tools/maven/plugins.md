---
title: maven plugins
categories:  
	- [工具,maven]
tags:
	- maven
date: 2021/08/23 00:00:00
update: 2021/08/23 00:00:00
---

# maven-shade-plugin

## pom

```xml
<!-- https://mvnrepository.com/artifact/org.apache.maven.plugins/maven-shade-plugin -->
<dependency>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>3.2.4</version>
</dependency>
```

## 使用

### 打包可执行 jar 包

通过设置主类的方式，打包可执行 jar 包。

```xml
<plugin>
    <!-- ... -->
    <executions>
        <execution>
          	<!-- ... -->
            <configuration>
                <transformers>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <mainClass>pub.wii.cook.Main</mainClass>
                    </transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>
```

## 配置示例

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
                    <transformer
                            implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <mainClass>pub.wii.cook.Main</mainClass>
                    </transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>
```

# maven-assembly-plugin

## pom

```xml
<!-- https://mvnrepository.com/artifact/org.apache.maven.plugins/maven-assembly-plugin -->
<dependency>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>3.3.0</version>
</dependency>
```

## 使用

`maven-assembly-plugin` 插件的使用需要打包配置（通常命名为 assembly.xml、release.xml 等，具体内容参考配置示例），插件内置了一部分配置，比如 [`jar-with-dependencies` ](https://github.com/apache/maven-assembly-plugin/blob/master/src/main/resources/assemblies/jar-with-dependencies.xml)，使用如下配置，来启用。

```xml
<plugin>
    <!-- ... -->
    <executions>
        <execution>
            <!-- ... -->
            <configuration>
                <descriptorRefs>
                    <descriptorRef>jar-with-dependencies</descriptorRef>
                </descriptorRefs>
                <!-- ... -->
            </configuration>
        </execution>
    </executions>
</plugin>
```

这里需要注意两点。

- 如果指定了预设配置，那么再指定打包配置文件，会被忽略

  ```xml
  <plugin>
      <!-- ... -->
      <executions>
          <execution>
              <!-- ... -->
              <configuration>
                  <descriptorRefs>
                      <descriptorRef>jar-with-dependencies</descriptorRef>
                  </descriptorRefs>
                
                  <descriptors> <!-- 会被忽略 -->
                      <descriptor>src/assemble/assembly.xml</descriptor>
                  </descriptors>
                  <!-- ... -->
              </configuration>
          </execution>
      </executions>
  </plugin>
  ```

- `jar-with-dependencies` 插件，并不会合并 META-INF 下的内容

  - 如果，我们依赖的多个包里面定义了同样的 SPI 接口，那么只会保留其中一个的内容，这样程序在运行时，可能会抛出异常，比如

    ```shell
    Caused by: java.lang.IllegalStateException: Could not find policy 'grpclb'. Make sure its implementation is either registered to LoadBalancerRegistry or included in META-INF/services/io.grpc.LoadBalancerProvider from your jar files.
    ```

  - 遇到这种情况，需要自定义打包配置文件，参考配置示例

## 非配置文件示例

```xml
<plugin>
    <artifactId>maven-assembly-plugin</artifactId>
    <configuration>
        <archive>
            <manifest>
                <mainClass>pub.wii.cook.scala.main</mainClass>
            </manifest>
        </archive>
        <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
        </descriptorRefs>
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

## 配置示例

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
<!--                            <descriptorRefs>-->
<!--                                <descriptorRef>jar-with-dependencies</descriptorRef>-->
<!--                            </descriptorRefs>-->
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
        <containerDescriptorHandler>
            <handlerName>metaInf-spring</handlerName>
        </containerDescriptorHandler>
        <containerDescriptorHandler>
            <handlerName>plexus</handlerName>
        </containerDescriptorHandler>
        <!-- 示例，其实不需要，metaInf-services handler 会做这件事情 -->
        <containerDescriptorHandler>
            <handlerName>file-aggregator</handlerName>
            <configuration>
                <filePattern>.*/META-INF/services/io.grpc.NameResolverProvider</filePattern>
                <outputPath>META-INF/services/io.grpc.NameResolverProvider</outputPath>
            </configuration>
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