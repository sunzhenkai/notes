---
title: spring cacheable 
categories: 
  - [架构,Java,框架,spring]
tags:
  - spring
date: "2021-09-19T00:00:00+08:00"
update: "2021-09-19T00:00:00+08:00"
---

# 说明

spring 提供了缓存功能，接下来完成一个示例，然后看下怎么不缓存空结果以及怎么写单测。

# 引入依赖

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-cache</artifactId>
  <version>2.3.3.RELEASE</version>
</dependency>
<dependency>
  <groupId>com.github.ben-manes.caffeine</groupId>
  <artifactId>caffeine</artifactId>
  <version>2.6.2</version>
</dependency>
```

# 编写代码

```shell
├── cache
│   ├── CacheableService.java
│   ├── CustomCacheManager.java
│   └── CustomKeyGenerator.java
├── controller
│   ├── CacheController.java
├── ...
```

## CustomCacheManager.java

```java
package pub.wii.cook.springboot.cache;

import com.github.benmanes.caffeine.cache.Caffeine;
import com.google.common.collect.Lists;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.caffeine.CaffeineCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.TimeUnit;

@EnableCaching
@Configuration
public class CustomCacheManager {
    private static final int CACHE_CAP = 100;
    public static final String CACHE_NAME = "sample";

    @Bean(name = CACHE_NAME)
    CacheManager cacheManager() {
        CaffeineCacheManager cm = new CaffeineCacheManager();
        cm.setCaffeine(Caffeine.newBuilder().expireAfterAccess(1, TimeUnit.MINUTES)
                .recordStats()
                .initialCapacity(CACHE_CAP)
                .maximumSize(CACHE_CAP));
        cm.setCacheNames(Lists.newArrayList(CACHE_NAME));
        return cm;
    }
}
```

## CustomKeyGenerator.java

```java
package pub.wii.cook.springboot.cache;

import org.springframework.cache.interceptor.KeyGenerator;
import org.springframework.stereotype.Component;

import java.lang.reflect.Method;
import java.util.Arrays;

@Component
public class CustomKeyGenerator implements KeyGenerator {
    @SuppressWarnings("NullableProblems")
    @Override
    public Object generate(Object o, Method method, Object... objects) {
        return o.getClass().getSimpleName() + ":" + method.getName() + ":" + Arrays.toString(objects);
    }
}
```

## CacheableService.java

```java
package pub.wii.cook.springboot.cache;

import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.UUID;

import static pub.wii.cook.springboot.cache.CustomCacheManager.CACHE_NAME;

@Service
public class CacheableService {
    private static final Random random = new Random();

    @Cacheable(
            cacheManager = CACHE_NAME,
            cacheNames = CACHE_NAME,
            keyGenerator = "customKeyGenerator"
    )
    public List<Object> cache(String key) {
        List<Object> res = new ArrayList<>();
        int size = random.nextInt(10) + 1;
        for (int i = 0; i < size; ++i) {
            res.add(UUID.randomUUID().toString());
        }
        return res;
    }
}
```

## CacheController.java

```java
package pub.wii.cook.springboot.controller;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pub.wii.cook.springboot.cache.CacheableService;

import javax.annotation.Resource;
import java.util.List;

@RestController
@RequestMapping("cache")
public class CacheController {

    @Resource
    CacheableService cacheableService;

    @RequestMapping(value = "get",
            method = RequestMethod.GET,
            produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public ResponseEntity<List<Object>> get(@RequestParam("key") String key) {
        return ResponseEntity.ok(cacheableService.cache(key));
    }
}
```

# 示例

```shell
$ curl "http://localhost:8080/cache/get?key=wii"
["4b2dee35-781b-42cd-b594-8994025fa36e","6b4432c3-f16f-45c6-b56e-334054588a65","57b7f89a-8dd6-4500-98ab-b14973a88971"]
```

# 不缓存空结果

只需要在 `@Cacheable` 添加 `unless = "#result == null or #result.size() == 0"` 选项即可。

```java
@Service
public class CacheableService {
    private static final Random random = new Random();

    @Cacheable(
            cacheManager = CACHE_NAME,
            cacheNames = CACHE_NAME,
            keyGenerator = "customKeyGenerator",
            unless = "#result == null or #result.size() == 0"
    )
    public List<Object> cache(String key) {
        List<Object> res = new ArrayList<>();
        int size = random.nextInt(10) + 1;
        for (int i = 0; i < size; ++i) {
            res.add(UUID.randomUUID().toString());
        }
        return res;
    }
}
```

# 单测

相较于其他单测方式，直接测 Cache 内有没有缓存数据更直接。

## CacheableServiceTest.java

```java
package pub.wii.cook.springboot.cache;

import com.google.common.collect.Lists;
import lombok.SneakyThrows;
import org.junit.jupiter.api.Test;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.interceptor.KeyGenerator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;
import pub.wii.cook.springboot.config.CookSpringBootConfiguration;

import javax.annotation.Resource;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static pub.wii.cook.springboot.cache.CustomCacheManager.CACHE_NAME;

@ContextConfiguration(classes = CookSpringBootConfiguration.class)
@SpringJUnitConfig(classes = CookSpringBootConfiguration.class)
class CacheableServiceTest {

    interface ICache {
        List<Integer> cacheWithEmpty(List<Integer> echo);

        List<Integer> cacheWithoutEmpty(List<Integer> echo);
    }

    @Configuration
    @EnableCaching
    static class Config {
        static class ICacheImpl implements ICache {

            @Cacheable(
                    cacheManager = CACHE_NAME,
                    cacheNames = CACHE_NAME,
                    keyGenerator = "customKeyGenerator"
            )
            @Override
            public List<Integer> cacheWithEmpty(List<Integer> echo) {
                return echo;
            }

            @Cacheable(
                    cacheManager = CACHE_NAME,
                    cacheNames = CACHE_NAME,
                    keyGenerator = "customKeyGenerator",
                    unless = "#result == null or #result.size() == 0"
            )
            @Override
            public List<Integer> cacheWithoutEmpty(List<Integer> echo) {
                return echo;
            }
        }

        @Bean
        ICache iCache() {
            return new ICacheImpl();
        }
    }

    @Resource(name = CACHE_NAME)
    CacheManager cacheManager;

    @Resource
    ICache iCache;

    @SuppressWarnings("ConstantConditions")
    @SneakyThrows
    @Test
    void cache() {
        List<Integer> nonEmpty = Lists.newArrayList(1, 2, 3);
        List<Integer> empty = new ArrayList<>();
        List<Integer> nil = null;
        Cache cache = cacheManager.getCache(CACHE_NAME);
        KeyGenerator kg = new CustomKeyGenerator();
        assertNotNull(cache);

        iCache.cacheWithEmpty(nonEmpty);
        iCache.cacheWithEmpty(empty);
        iCache.cacheWithEmpty(nil);
        iCache.cacheWithoutEmpty(nonEmpty);
        iCache.cacheWithoutEmpty(empty);
        iCache.cacheWithoutEmpty(nil);

        assertEquals(cache.get(genKeyWithEmpty(kg, nonEmpty)).get(), nonEmpty);
        assertEquals(cache.get(genKeyWithEmpty(kg, empty)).get(), empty);
        assertEquals(cache.get(genKeyWithEmpty(kg, nil)).get(), nil);
        assertEquals(cache.get(genKeyWithoutEmpty(kg, nonEmpty)).get(), nonEmpty);
        assertEquals(cache.get(genKeyWithoutEmpty(kg, empty)), nil);
        assertEquals(cache.get(genKeyWithoutEmpty(kg, nil)), nil);
    }

    @SneakyThrows
    Object genKeyWithEmpty(KeyGenerator kg, List<Integer> arg) {
        // 第一个参数不要用 iCache, iCache 是通过反射机制设置的对象, 有可能是一个 Proxy
        // 获取 class name 的时候可能会得到奇怪的值, 导致 key 匹配不上
        return kg.generate(new Config.ICacheImpl(),
                ICache.class.getMethod("cacheWithEmpty", List.class), arg);
    }

    @SneakyThrows
    Object genKeyWithoutEmpty(KeyGenerator kg, List<Integer> arg) {
        // 第一个参数不要用 iCache, iCache 是通过反射机制设置的对象, 有可能是一个 Proxy
        // 获取 class name 的时候可能会得到奇怪的值, 导致 key 匹配不上
        return kg.generate(new Config.ICacheImpl(),
                ICache.class.getMethod("cacheWithoutEmpty", List.class), arg);
    }
}
```

## CookSpringBootConfiguration.java

```java
package pub.wii.cook.springboot.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.context.annotation.aspectj.EnableSpringConfigured;

@EnableSpringConfigured
@EnableAspectJAutoProxy
@ComponentScan(basePackages = {"pub.wii.cook"}, lazyInit = true)
public class CookSpringBootConfiguration {
}
```

