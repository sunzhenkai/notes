---
title: maven settings
categories:  
  - [工具,maven]
tags:
  - maven
date: 2021/08/23 00:00:00
update: 2021/08/23 00:00:00
---

# Minimal settings.xml

```xml
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
                      http://maven.apache.org/xsd/settings-1.0.0.xsd">
  <localRepository/>
  <interactiveMode/>
  <usePluginRegistry/>
  <offline/>
  <pluginGroups/>
  <servers/>
  <mirrors/>
  <proxies/>
  <profiles/>
  <activeProfiles/>
</settings>
```

# aliyun

```xml

<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
                      http://maven.apache.org/xsd/settings-1.0.0.xsd">
  <localRepository/>
  <interactiveMode/>
  <usePluginRegistry/>
  <offline/>
  <pluginGroups/>
  <servers/>
  <mirrors>
  	<mirror>
    	<id>aliyunmaven</id>
    	<mirrorOf>*</mirrorOf>
    	<name>阿里云公共仓库</name>
  		<url>https://maven.aliyun.com/repository/public</url>
		</mirror>
  </mirrors>
  <proxies/>
  <profiles/>
  <activeProfiles/>
</settings>
```

