---
title: 云原生
categories: 
	- [架构, 概念]
tags:
	- 云原生
date: 2020/11/11 00:00:00
update: 2020/11/11 00:00:00
---

 # 定义

云原生技术有利于各组织在公有云、私有云和混合云等新型**动态环境**中，构建和运行可**弹性扩展**的应用。云原生的代表技术包括容器、服务网格、微服务、不可变基础设施和声明式API。

这些技术能够构建容错性好、易于管理和便于观察的松耦合系统。结合可靠的自动化手段，云原生技术使工程师能够轻松地对系统作出频繁和可预测的重大变更。

# 技术

## 不可变基础设施

在传统可变服务器基础架构中，服务器在创建之后会不断更新和修改，包括软件环境、配置等，在这种架构中存在配置漂移、雪花服务器等问题。**配置漂移** 是指对操作系统的更改不被记录，独特和可变的配置，无法/很难在其他机器复现。**雪花服务器** 存在配置漂移问题的服务器，很难被复制。**凤凰服务器** 对配置进行版本管理，减少或解决配置漂移问题。

在不可变基础架构/设施中，对配置进行版本控制，服务器一但部署，不会再手动更改。如需更新配置、软件环境，通过部署版本化的配置解决，或通过部署打包的公共镜像。这种方式，有更高的一致性、可靠性及可预测的部署过程。

# 参考

- https://jimmysong.io/kubernetes-handbook/cloud-native/cloud-native-definition.html?q=
- https://jimmysong.io/migrating-to-cloud-native-application-architectures/
- https://en.wikipedia.org/wiki/Cloud_native_computing
- https://landscape.cncf.io/
- https://github.com/cncf/toc/blob/master/DEFINITION.md#%E4%B8%AD%E6%96%87%E7%89%88%E6%9C%AC
- https://cloud.tencent.com/developer/news/329406
- https://www.howtoing.com/configuration-drift-phoenix-server-vs-snowflake-server-comic
- https://developer.aliyun.com/article/781563
- https://www.infoq.cn/article/2urzLXGzykx0VmYYVekO