---
title: maven 使用
categories:  
  - [工具,maven]
tags:
  - maven
date: "2021-01-29T00:00:00+08:00"
update: "2021-01-29T00:00:00+08:00"
---

[toc]

# 命令

```shell
# 清理
$ mvn clean

# 打包
$ mvn package

# 依赖树
$ mvn dependency:tree

# 指定 pom
$ mvn --settings YourOwnSettings.xml package
# OR
$ mvn -s YourOwnSettings.xml package
```


# 创建项目

```shell
$ mvn archetype:generate
```

# 打包

```shell
$ mvn package
```

## 指定模块

```shell
$ mvn clean package -pl <group-id>:<artifact-id> -am
```

## 指定 pom 文件

```shell
$ mvn package -f /path/to/pom.xml
```

# 可执行jar

```xml
<build>
  <resources>
    <resource>
      <directory>
        ${project.basedir}/src/main/resources
      </directory>
      <filtering>true</filtering>
    </resource>
  </resources>

  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-assembly-plugin</artifactId>
      <executions>
        <execution>
          <goals>
            <goal>attached</goal>
          </goals>
          <phase>package</phase>
          <configuration>
            <descriptorRefs>
              <descriptorRef>jar-with-dependencies</descriptorRef>
            </descriptorRefs>
            <archive>
              <manifest>
                <mainClass>top.szhkai.mitest.TestZKFacade</mainClass>
              </manifest>
            </archive>
          </configuration>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

# 搜索依赖包

```shell
 $ mvn dependency:tree | grep recommend-service-common
```

# 指定编译版本

```xml
<plugins>  
	  <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.5.1</version>
        <configuration>
            <source>1.8</source>
            <target>1.8</target>
        </configuration>
    </plugin>
	  ...
</plugins>
```

# 配置多源文件

## resources

```xml
   <resources>
        <resource>
            <directory>src/main/java</directory>
            <includes>
                <include>**/*.java</include>
                <include>**/*.properties</include>
                <include>**/*.xml</include>
            </includes>
        </resource>

        <resource>
            <directory>src/main/resources</directory>
            <includes>
                <include>**/*.java</include>
                <include>**/*.properties</include>
                <include>**/*.xml</include>
            </includes>
        </resource>

        <resource>
            <directory>src/main/generated</directory>
            <includes>
                <include>**/*.java</include>
                <include>**/*.properties</include>
                <include>**/*.xml</include>
            </includes>
        </resource>
    </resources>
```

## sourceDirectory

```xm
<generatedSourcesDirectory>src/main/generated</generatedSourcesDirectory>
```

## maven-compiler-plugin

```xml
<build>
    <sourceDirectory>.</sourceDirectory>
    <plugins>
        <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <configuration>
        <includes>
            <include>src/main/java/**/*.java</include>
            <include>src/main/scala/**/*.scala</include>
        </includes>
        </configuration>
        </plugin>
    </plugins>
</build>
```

## build-helper-maven-plugin

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>build-helper-maven-plugin</artifactId>
            <executions>
                <execution>
                    <phase>generate-sources</phase>
                    <goals>
                        <goal>add-source</goal>
                    </goals>
                    <configuration>
                        <sources>
                            <source>src/main/generated</source>
                        </sources>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

# 添加本地依赖

如果有需要添加一个 jar 包到工程，且没有可用的如 nexus 的包管理服务，可以参考[这里](https://stackoverflow.com/questions/2229757/maven-add-a-dependency-to-a-jar-by-relative-path/2230464#2230464)。

首先在工程创建一个目录 `libs`。

```shell
$ mkdir libs
```

然后，安装 jar 包到 `libs` 。

```shell
$ mvn org.apache.maven.plugins:maven-install-plugin:2.5.2:install-file \
  -Dfile=<path-to-jar> \
  -DgroupId=<group-id> \
  -DartifactId=<artifact-id> \
  -Dversion=<version> \
  -Dpackaging=jar \
  -DlocalRepositoryPath=libs
```

然后，修改 pom。

```xml
<repositories>
  <repository>
    <id>project-repo</id>
    <url>file://${project.basedir}/libs</url>
  </repository>
</repositories>

<dependencies>
   <dependency>
        <groupId>org.apache.bahir</groupId>
        <artifactId>flink-connector-kudu_${scala.version}</artifactId>
        <version>1.2-SNAPSHORT</version>
    </dependency>
</dependencies>
```

