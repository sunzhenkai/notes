---
title: Spring注解
categories: 
  - [架构,Java,框架,Spring]
tags:
  - Spring
  - 注解
  - Java
date: 2020/11/20 00:00:00
update: 2020/11/20 00:00:00
---

# 简述

## Spring注解

| 注解                            | 对象       | 说明                                                         |
| ------------------------------- | ---------- | ------------------------------------------------------------ |
| @Controller                     | 类         | DispatcherServlet会自动扫描注解了此注解的类                  |
| @Service                        | 类         | -                                                            |
| @Reponsitory                    | 类         | -                                                            |
| @Component                      | 类         | -                                                            |
| @Autowired                      | 方法、字段 | 依赖注入                                                     |
| @Configuration                  | 类         | 声明类为配置类                                               |
| @ComponentScan                  | 类         | 自动扫描指定包内特定注解并注册Bean，默认扫描@Service、@Component、@Controller、@Repository注解，可自定义规则 |
| @Bean                           | 方法、注解 | 声明返回值为Bean，可定义init、destroy方法，在Bean创建、销毁时调用 |
| @Aspect                         | 类         | 声明切面                                                     |
| **@After**                      | 方法       | 后置建言，原方法前执行                                       |
| **@Before**                     | 方法       | 前置建言，原方法前执行                                       |
| **@Around**                     | 方法       | 环绕建言，在原方法执行前执行，在原方法执行后再执行           |
| @PointCut                       | -          | 声明切点，即定义拦截规则，确定有哪些方法会被切入             |
| @Transactional                  |            | 声明事务                                                     |
| @Cacheable                      |            | 声明数据缓存                                                 |
| @Value                          |            | 值注入，常与Sping EL表达式语言一起使用，注入普通字符，系统属性，表达式运算结果，其他Bean的属性，文件内容，网址请求内容，配置文件属性值等等 |
| @PropertySource                 |            | 指定文件地址，提供了一种方便的、声明性的机制，向Spring的环境添加PropertySource。与@Configuration一起使用 |
| @PostConstruct                  | 方法       | 构造函数执行完成之后执行该方法                               |
| @PreDestroy                     | 方法       | 对象销毁之前执行该方法                                       |
| @Profile                        |            | 根据配置条件注册/激活                                        |
| @EnableAsync                    | 配置类     | 开启异步任务支持                                             |
| @Async                          | 类、方法   | 注解在方法上标示这是一个异步方法，在类上标示这个类所有的方法都是异步方法 |
| @EnableScheduling               | 类         | 开启对计划任务的支持                                         |
| @Scheduled                      | 方法       | 声明该方法是计划任务，支持多种类型的计划任务：cron、fixDelay、fixRate |
| @Conditional                    | 类         | 条件声明                                                     |
| @RunWith                        | 类         | junit注解                                                    |
| @ContextConfiguration           | 类         | 用来加载配置ApplicationContext，其中classes属性用来加载配置类:@ContextConfiguration(classes = {TestConfig.class(自定义的一个配置类)}) |
| @ActiveProfiles                 | 类         | 用来声明活动的profile                                        |
| @EnableWebMvc                   | 配置类     | 开启SpringMvc的Mvc的一些默认配置：如ViewResolver，MessageConverter等。同时在自己定制SpringMvc的相关配置时需要做到两点：1.配置类继承WebMvcConfigurerAdapter类，2.必须使用这个@EnableWebMvc注解 |
| @RequestMapping                 | 类、方法   | 映射web请求（访问路径和参数                                  |
| @ResponseBody                   | 方法、类   | 将返回值放在response体内                                     |
| @RequestBody                    | 参数       | request的参数在request body内，此注解放置在参数前            |
| @PathVariable                   | 参数       | 接受路径参数                                                 |
| @RestController                 | 类         | 组合了@Controller和@ResponseBody，当我们只开发一个和页面交互数据的控制层的时候可以使用此注解 |
| @ControllerAdvice               | 类         | 声明一个控制器建言，它也组合了@Component注解，会自动注册为Spring的Bean |
| @ExceptionHandler               | 方法       | 异常处理                                                     |
| @ModelAttribute                 | 参数、方法 | 将键值对添加到全局，所有注解了@RequestMapping的方法可获得此键值对 |
| @WebAppConfiguration            | 类         | 一般用在测试上，注解在类上，用来声明加载的ApplicationContext是一个WebApplicationContext。他的属性指定的是Web资源的位置，默认为src/main/webapp，我们可以修改为：@WebAppConfiguration("src/main/resources") |
| @EnableAutoConfiguration        | 类         | 此注释自动载入应用程序所需的所有Bean，该注解组合了@Import注解，@Import注解导入了EnableAutoCofigurationImportSelector类，它使用SpringFactoriesLoader.loaderFactoryNames方法来扫描具有META-INF/spring.factories文件的jar包。而spring.factories里声明了有哪些Bean自动配置 |
| @ImportResource                 | 类         | 用来加载额外配置（xml等定义）                                |
| @ConfigurationProperties        | 类         | 将properties属性与一个Bean及其属性相关联，从而实现类型安全的配置 |
| @ConditionalOnBean              | 类         | 条件注解，当容器里有指定Bean的条件下                         |
| @ConditionalOnClass             | 类         | 条件注解，当类路径下有指定的类的条件下                       |
| @ConditionalOnExpression        | 类         | 条件注解，基于SpEL表达式作为判断条件                         |
| @ConditionalOnJava              | 类         | 条件注解，基于JVM版本作为判断条件                            |
| @ConditionalOnJndi              | 类         | 条件注解，在JNDI存在的条件下查找指定的位置                   |
| @ConditionalOnMissingBean       | 类         | 条件注解，当容器里没有指定Bean的情况下                       |
| @ConditionalOnMissingClass      | 类         | 条件注解，当类路径下没有指定的类的情况下                     |
| @ConditionalOnNotWebApplication | 类         | 条件注解，当前项目不是web项目的条件下                        |
| @ConditionalOnResource          | 类         | 条件注解，类路径是否有指定的值                               |
| @ConditionalOnSingleCandidate   | 类         | 条件注解，当指定Bean在容器中只有一个，后者虽然有多个但是指定首选的Bean |
| @ConditionalOnWebApplication    | 类         | 条件注解，当前项目是web项目的情况下                          |
| @EnableConfigurationProperties  | 类         | 声明开启属性注入，使用@Autowired注入，例：@EnableConfigurationProperties(HttpEncodingProperties.class)。 |
| @AutoConfigureAfter             | 类         | 在指定的自动配置类之后再配置，例：@AutoConfigureAfter(WebMvcAutoConfiguration.class) |

## JSR 注解

| 注解      | 说明     | JSR版本 |
| --------- | -------- | ------- |
| @Resource | 依赖注入 | JSR250  |
| @Inject   | 依赖注入 | JSR330  |

# 对比

## Resource & Inject & Autowired

| 注解      | Processor                            | 注入方式                                       |
| --------- | ------------------------------------ | ---------------------------------------------- |
| Resource  | AutowiredAnnotationBeanPostProcessor | 默认字段名(field name)，若失败退化为类型(type) |
| Inject    | AutowiredAnnotationBeanPostProcessor | 默认依据类型注入                               |
| Autowired | CommonAnnotationBeanPostProcessor    | 默认依据类型注入                               |

# 参考

- https://blog.csdn.net/u012734441/article/details/51706504
- https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/ComponentScan.html