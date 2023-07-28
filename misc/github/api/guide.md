---
title: API - 规范
categories: 
    - [guide,api]
tags:
    - API
    - 规范
date: 2021/07/15 00:00:00
update: 2021/07/15 00:00:00
---

# 目标

接口设计应以一些目标为导向，这些目标包含且不限于，易读、易懂、易用、清晰（意义明确，不易误用）、易维护、易扩展、功能强大且满足需求。要达到如上目标，在设计 API 时应考虑如下细节。

- 文档
- 控制器和动作命名公约
- 稳定性且一致性
- 灵活性
- 安全性
- 有效性校验
- HTTP 状态码
- 帮助页面
- 日志

从形式来讲，API 不仅有 HTTP/WEB，还有 gRPC、Thrift。

# 视角

对于思考设计良好的接口，可从下面两个视角着手。

- API 实现视角
  - 这个服务需要做什么
  - 这个服务需要提供什么
  - 怎么才能使  API 更通用 （输入、输出、扩展性）
- API 使用者视角
  - 使用者如何继承我们的 API
  - 如何让使用者更灵活地向 API 提供数据并获取输出
  - 如何让使用者花更少的时间获得他们所需要的信息

# 规范

## 分类

### Errors（错误）

Errors 是指客户端向服务发送错误数据，服务正确拒绝该数据。**Errors 不会影响服务可用性**。

### Faults（故障）

Faults 是指服务对合法的请求无法正常返回结果。Faults 会影响服务可用性。

由于限流或配额失败（事先设定）引起的调用失败，不能算作 faults。如果是由于服务自我保护造成的请求失败，算作 faults，比如快速失败策略。

### Latency（延迟）

Latency 是指完成特定 API 调用消耗的时间，尽可能接近客户端计量。对于长操作请求，该指标记为初始请求耗时。

### Time to complete

对于暴露长操作的服务，必须对这些指标跟踪 "Time to complete" 指标。

### Long running API faults

对于长操作，初始请求和检索请求都可能正常，但如果最终操作失败，必须汇总至总体的可用性指标中。

## 客户端规范

### 忽略原则

忽略服务端返回的多余字段。

### 可变顺序规则

忽略服务端返回数据字段的顺序。

## 一致性基础

### URL 结构

URL 应该易读且易构造。

### URL 长度

HTTP 1.1 RFC 7230 并未定义 URL 长度限制，如果服务接收到的请求 URL 长度大于其定义的限制长度，应返回 414 状态码。

所以，对于长度大于 2083 个字符的 URL ，应考虑服务是否可以接受。

## 支持的方法

| 方法    | 描述                                                         | 是否幂等 |
| ------- | ------------------------------------------------------------ | -------- |
| GET     | 返回当前对象值                                               | 是       |
| PUT     | 替换或创建对象                                               | 是       |
| DELETE  | 删除对象                                                     | 是       |
| POST    | 根据提供的数据创建新对象，或提交命令                         | 否       |
| HEAD    | 为 GET 响应返回对象的元数据，资源支持 GET 请求，也应支持 HEAD 请求 | 是       |
| PATCH   | 对对象应用重要的更新                                         | 否       |
| OPTIONS | 获取请求的信息                                               | 是       |

## 自定义 Headers

跟定 API 的基本操作，不能指定自定义 Headers。

## 命名公约

- 请求和返回值参数，不应使用缩写（比如 msg）

## response

返回值数据结构应分级，不应将业务数据放在第一级。

```json
# 异常
{
    "status": 1000,
    "errors": {
        "target": "ContactInfo",
        "message": "Multiple errors in ContactInfo data",
        "details": [
            {
                "code": "NullValue",
                "target": "PhoneNumber",
                "message": "Phone number must not be null"
            },
            {
                "code": "MalformedValue",
                "target": "Address",
                "message": "Address is not valid"
            }
        ]
    }
}

# 正常
{
    "status": 0,
    "data": {
        "contacts": [
            {
                "name": "cmcc",
                "phone": "10086"
            }
        ]
    }
}
```

对于 code，应进行细致的划分，比如。

| 状态码 | 说明                               | HTTP Status Code |
| ------ | ---------------------------------- | ---------------- |
| 0      | 请求正常返回                       | 200              |
| 1000+  | 请求错误（参数、数据不存在等）     | 400              |
| 2000+  | 元数据读取异常（不存在、格式异常） | 200              |
| 3000+  | 处理时异常                         | 500              |
| 4000+  | 数据写入时异常                     | 500              |
| 5000+  | 未知服务异常                       | 500              |

对于  message 格式也应进行统一（避免英文/中文混用，有的 message 为英文，有的为中文），务必保证 code 不为 0 时返回有效 message。

# QA

有一些设计细节，很难判定那种方式实现比较好，这里做下讨论。

## 多个功能使用一个接口 VS 多个接口

对于功能相似的多个接口，是使用一个接口 + 字段标识，还是拆分成多个接口。

# 参考

- https://www.moesif.com/blog/api-guide/getting-started-with-apis/
- https://www.c-sharpcorner.com/article/web-api-design-principles-or-web-api-design-guidelines/
- https://github.com/microsoft/api-guidelines
- https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design