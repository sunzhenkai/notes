---
title: pom example
categories:  
  - [工具,maven]
tags:
  - maven
date: "2021-08-23T00:00:00+08:00"
update: "2021-08-23T00:00:00+08:00"
---

# scala

```xml
<!-- properties -->
<properties>
  <scala.version>2.12.7</scala.version>
  <scala.compat.version>2.12</scala.compat.version>
  <encoding>UTF-8</encoding>
</properties>

<!-- dependencies -->
<dependencies>
  <dependency>
    <groupId>org.scala-lang</groupId>
    <artifactId>scala-library</artifactId>
    <version>${scala.version}</version>
  </dependency>
  <dependency>
    <groupId>org.scala-lang.modules</groupId>
    <artifactId>scala-xml_${scala.compat.version}</artifactId>
    <version>1.1.1</version>
  </dependency>
  <dependency>
    <groupId>org.scala-lang.modules</groupId>
    <artifactId>scala-parser-combinators_${scala.compat.version}</artifactId>
    <version>1.1.1</version>
  </dependency>
  <dependency>
    <groupId>org.scala-lang.modules</groupId>
    <artifactId>scala-swing_${scala.compat.version}</artifactId>
    <version>2.0.3</version>
  </dependency>
</dependencies>

<!-- plugins -->
<plugins>
  <plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
      <source>1.8</source>
      <target>1.8</target>
      <fork>true</fork>
      <verbose>true</verbose>
      <encoding>UTF-8</encoding>
      <compilerArguments>
        <sourcepath>
          ${project.basedir}/src/main/java
        </sourcepath>
        <sourcepath>
          ${project.basedir}/src/main/scala
        </sourcepath>
      </compilerArguments>
    </configuration>
  </plugin>
  <plugin>
    <groupId>net.alchim31.maven</groupId>
    <artifactId>scala-maven-plugin</artifactId>
  </plugin>
  <plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>2.4</version>
    <configuration>
      <descriptorRefs>
        <descriptorRef>jar-with-dependencies</descriptorRef>
      </descriptorRefs>
      <archive>
        <manifest>
          <mainClass>com.*.Class</mainClass>
        </manifest>
      </archive>
    </configuration>
    <executions>
      <execution>
        <phase>package</phase>
        <goals>
          <goal>single</goal>
        </goals>
      </execution>
    </executions>
  </plugin>
</plugins>
```

# example
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>com.neu.cse</groupId>
	<artifactId>PowerCloud</artifactId>
	<packaging>war</packaging>
	<version>0.0.1-SNAPSHOT</version>
	<name>PowerCloud Maven Webapp</name>

	<!-- 集中定义依赖版本号 -->
	<properties>
		<junit.version>4.12</junit.version>
		<spring.version>4.1.3.RELEASE</spring.version>
		<mybatis.version>3.2.8</mybatis.version>
		<mybatis.spring.version>1.2.2</mybatis.spring.version>
		<mybatis.paginator.version>1.2.15</mybatis.paginator.version>
		<mysql.version>5.1.32</mysql.version>
		<slf4j.version>1.6.4</slf4j.version>
		<jackson.version>2.4.2</jackson.version>
		<druid.version>1.0.9</druid.version>
		<httpclient.version>4.3.5</httpclient.version>
		<jstl.version>1.2</jstl.version>
		<servlet-api.version>2.5</servlet-api.version>
		<jsp-api.version>2.0</jsp-api.version>
		<joda-time.version>2.5</joda-time.version>
		<commons-lang3.version>3.3.2</commons-lang3.version>
		<commons-io.version>1.3.2</commons-io.version>
		<commons-net.version>3.3</commons-net.version>
		<pagehelper.version>3.4.2</pagehelper.version>
		<jsqlparser.version>0.9.1</jsqlparser.version>
		<commons-fileupload.version>1.3.1</commons-fileupload.version>
	</properties>

	<dependencies>
		<!-- 时间操作组件 -->
		<dependency>
			<groupId>joda-time</groupId>
			<artifactId>joda-time</artifactId>
			<version>${joda-time.version}</version>
		</dependency>
		<!-- Apache工具组件 -->
		<dependency>
			<groupId>org.apache.commons</groupId>
			<artifactId>commons-lang3</artifactId>
			<version>${commons-lang3.version}</version>
		</dependency>
		<dependency>
			<groupId>org.apache.commons</groupId>
			<artifactId>commons-io</artifactId>
			<version>${commons-io.version}</version>
		</dependency>
		<dependency>
			<groupId>commons-net</groupId>
			<artifactId>commons-net</artifactId>
			<version>${commons-net.version}</version>
		</dependency>
		<!-- Jackson Json处理工具包 -->
		<dependency>
			<groupId>com.fasterxml.jackson.core</groupId>
			<artifactId>jackson-databind</artifactId>
			<version>${jackson.version}</version>
		</dependency>
		<!-- httpclient -->
		<dependency>
			<groupId>org.apache.httpcomponents</groupId>
			<artifactId>httpclient</artifactId>
			<version>${httpclient.version}</version>
		</dependency>
		<!-- 单元测试 -->
		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>${junit.version}</version>
			<scope>test</scope>
		</dependency>
		<!-- 日志处理 -->
		<dependency>
			<groupId>org.slf4j</groupId>
			<artifactId>slf4j-log4j12</artifactId>
			<version>${slf4j.version}</version>
		</dependency>
		<!-- Mybatis -->
		<dependency>
			<groupId>org.mybatis</groupId>
			<artifactId>mybatis</artifactId>
			<version>${mybatis.version}</version>
		</dependency>
		<dependency>
			<groupId>org.mybatis</groupId>
			<artifactId>mybatis-spring</artifactId>
			<version>${mybatis.spring.version}</version>
		</dependency>
		<dependency>
			<groupId>com.github.miemiedev</groupId>
			<artifactId>mybatis-paginator</artifactId>
			<version>${mybatis.paginator.version}</version>
		</dependency>
		
		<!-- Pagehelper -->
		<dependency>
			<groupId>com.github.pagehelper</groupId>
			<artifactId>pagehelper</artifactId>
			<version>${pagehelper.version}</version>
		</dependency>
		
 		<!-- MySql -->
		<dependency>
			<groupId>mysql</groupId>
			<artifactId>mysql-connector-java</artifactId>
			<version>${mysql.version}</version>
		</dependency>
		<!-- 连接池 -->
		<dependency>
			<groupId>com.alibaba</groupId>
			<artifactId>druid</artifactId>
			<version>${druid.version}</version>
		</dependency>
		<!-- Spring -->
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-context</artifactId>
			<version>${spring.version}</version>
		</dependency>
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-beans</artifactId>
			<version>${spring.version}</version>
		</dependency>
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-webmvc</artifactId>
			<version>${spring.version}</version>
		</dependency>
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-jdbc</artifactId>
			<version>${spring.version}</version>
		</dependency>
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-aspects</artifactId>
			<version>${spring.version}</version>
		</dependency>
		<!-- JSP相关 -->
		<dependency>
			<groupId>jstl</groupId>
			<artifactId>jstl</artifactId>
			<version>${jstl.version}</version>
		</dependency>
		<dependency>
			<groupId>javax.servlet</groupId>
			<artifactId>servlet-api</artifactId>
			<version>${servlet-api.version}</version>
			<scope>provided</scope>
		</dependency>
		<dependency>
			<groupId>javax.servlet</groupId>
			<artifactId>jsp-api</artifactId>
			<version>${jsp-api.version}</version>
			<scope>provided</scope>
		</dependency>
		<!-- 文件上传组件 -->
		<dependency>
			<groupId>commons-fileupload</groupId>
			<artifactId>commons-fileupload</artifactId>
			<version>${commons-fileupload.version}</version>
		</dependency>
	</dependencies>
	<build>
		<finalName>${project.artifactId}</finalName>
		<plugins>
			<!-- 资源文件拷贝插件 -->
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-resources-plugin</artifactId>
				<version>2.7</version>
				<configuration>
					<encoding>UTF-8</encoding>
				</configuration>
			</plugin>
			<!-- java编译插件 -->
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-compiler-plugin</artifactId>
				<version>3.2</version>
				<configuration>
					<source>1.7</source>
					<target>1.7</target>
					<encoding>UTF-8</encoding>
				</configuration>
			</plugin>
		</plugins>
		<pluginManagement>
			<plugins>
				<!-- 配置Tomcat插件 -->
				<plugin>
					<groupId>org.apache.tomcat.maven</groupId>
					<artifactId>tomcat7-maven-plugin</artifactId>
					<version>2.2</version>
					<configuration>
					<port>8080</port>
					<path>/</path>
					<url>http://127.0.0.1:8080/manager/text</url>
					<username>tomcat</username>
					<password>tomcat</password>
					</configuration>
				</plugin>
			</plugins>
		</pluginManagement>
		<!-- 如果不添加此节点mybatis的mapper.xml文件都会被漏掉。 -->
		<resources>
			<resource>
				<directory>src/main/java</directory>
				<includes>
					<include>**/*.properties</include>
					<include>**/*.xml</include>
				</includes>
				<filtering>false</filtering>
			</resource>
			<!-- 由于以上修改了resource目录，如果不添加此节点将无法扫描到applicationContext文件都会被漏掉。 -->
			<resource>
                <directory>src/main/resources</directory>
                <includes>
                    <include>**/*.properties</include>
                    <include>**/*.xml</include>
                </includes>
                <filtering>false</filtering>
            </resource>			
		</resources>
	</build>
</project>

```

