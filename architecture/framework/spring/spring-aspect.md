---
title: spring aspect 
categories: 
	- [架构,Java,框架,spring]
tags:
	- spring
date: 2021/04/12 00:00:00
update: 2021/04/12 00:00:00
---

# new Bean 问题

在一些场景下，我们需要通过 new 来创建 spring bean，而不是借助 spring 框架，这时会遇到 `@Autowired` 注解的字段没有初始化的问题（null）。 此时，可以借助 aspect 来解决，具体步骤可以分为三步。

- 引入依赖
- 配置 `context:spring-configed`
- 命令行添加参数 `-javaagent:/path/to/aspectjweaver-{version}.jar`

对于 spring boot，启用 `context:spring-configed` 可以在 Application 类上使用注解 `@EnableSpringConfigured` 来实现，可能还需要 `@EnableAspectJAutoProxy` 注解。对于xml配置，可以添加如下代码。

```xml
<aop:aspectj-autoproxy/>
<context:spring-configured/
```

## 参考

- https://david-kerwick.github.io/2012-08-09-spring-autowired-and-new-operator/