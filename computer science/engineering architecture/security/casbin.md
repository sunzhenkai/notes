---
title: Casbin 入门：从 Model 到实际授权
categories:
  - 计算机科学
  - 工程架构
  - 安全
tags:
  - 安全
  - 授权
  - Casbin
date: "2026-08-04T16:31:01+08:00"
update: "2026-08-05T10:30:00+08:00"
---

# Casbin 入门：从 Model 到实际授权

[Casbin](https://casbin.apache.org/) 是一个开源授权库。它不负责登录、密码、Token 签发等认证工作，而是在身份已经确认后回答一个问题：**这个主体能否对这个资源执行这个动作？**

本文面向第一次接触 Casbin 的读者。读完后应该能够：

- 区分认证与授权，理解 Casbin 的职责边界；
- 看懂 Model、Policy 和 `Enforce()`；
- 从 ACL 过渡到 RBAC、ABAC、ReBAC 等模型；
- 在 [Casbin Policy Editor](https://editor.casbin.org/) 中调试授权规则；
- 使用 Go 和 Casbin v3 实现一个多租户文档 API 的授权样例。

## 1. Casbin 解决什么问题

没有授权框架时，权限判断很容易散落在业务代码里：

```go
if user.ID == document.OwnerID || user.Role == "admin" {
    // allow
}
```

系统规模扩大后，这种方式会带来几个问题：

- 相同规则在多个接口重复出现，修改时容易遗漏；
- 角色、租户、资源所有权和例外规则交织在一起；
- 很难回答“某人为什么有这个权限”；
- 很难统一测试、审计和动态更新权限；
- 业务代码与权限模型高度耦合。

Casbin 把授权拆成两部分：

| 部分 | 回答的问题 | 典型内容 |
|------|------------|----------|
| Model | 权限规则如何表达和计算？ | 请求字段、策略字段、角色关系、匹配器、策略效果 |
| Policy | 当前有哪些具体权限关系？ | 用户、角色、租户、资源、动作、允许或拒绝规则 |

可以把 Model 理解为“规则模板”，把 Policy 理解为“按照模板填写的数据”。应用只需要在访问资源前调用 Enforcer：

```text
认证上下文 + 资源 + 动作
          ↓
Enforcer.Enforce(...)
          ↓
       true / false
```

### Casbin 不负责什么

Casbin 是授权组件，不是完整的身份系统。以下工作通常由其他组件完成：

- 用户注册、密码校验、MFA；
- OAuth 2.0 / OIDC 登录；
- Session、JWT、Access Token 的签发与验证；
- 用户和组织的主数据管理。

应用应先验证身份，再把可信的用户 ID、租户等信息交给 Casbin。不要把客户端自行提交的 `user_id`、`role` 或 `tenant_id` 直接当作授权依据。

## 2. 建立最小心智模型

一次最基本的授权请求包含三个元素：

```text
Subject 对 Resource 执行 Action
alice   对 document-1 执行 read
```

| 概念 | Casbin 常用名称 | 含义 | 示例 |
|------|-----------------|------|------|
| 主体（Subject） | `sub` | 发起访问的人、服务或设备 | `alice`、`order-service` |
| 资源（Resource / Object） | `obj` | 被保护的数据、功能或服务 | `document-1`、`/orders/123` |
| 动作（Action） | `act` | 主体希望执行的操作 | `read`、`write`、`DELETE` |
| 域（Domain） | `dom` | 角色或策略生效的边界 | 租户、项目、组织 |
| 策略（Policy） | `p` | 具体的权限数据 | `p, alice, data1, read` |
| 角色关系（Grouping） | `g`、`g2` | 用户角色、资源角色或层级关系 | `g, alice, admin` |
| 策略效果（Effect） | `eft` / `e` | 多条策略匹配时如何合并 | allow、deny、priority |

### Resource 为什么在 Casbin 中叫 Object

Resource 是授权系统保护的目标，Casbin 文档习惯称其为 Object，并使用 `obj` 作为字段名。两者表达的是同一个概念，`obj` 也不是必须使用的固定名称；只要 Model 内引用一致，可以改成 `res`。

Resource 可以按不同粒度建模：

| 粒度 | 示例 | 说明 |
|------|------|------|
| 资源类型 | `document` | 判断某类功能权限 |
| 资源实例 | `document:123` | 执行对象级授权 |
| 层级资源 | `project/1/document/123` | 表达父子资源关系 |
| API 路径 | `/documents/:id` | 使用 KeyMatch 匹配路由 |
| 字段或子资源 | `user:123/email` | 字段级或细粒度授权 |

资源通常还带有 `tenant_id`、`owner_id`、标签、安全级别和业务状态等属性，可用于 ABAC 或 ReBAC。资源 ID 来自请求时仍是不可信输入，不能因为 ID 难以猜测就跳过对象级授权。

### 四个最常见的组件

| 组件 | 作用 | 初学时如何理解 |
|------|------|----------------|
| Model | 定义授权逻辑 | `model.conf` |
| Policy | 保存权限数据 | `policy.csv`，生产环境通常来自数据库 |
| Enforcer | 加载 Model/Policy 并执行决策 | 调用 `Enforce()` 的核心对象 |
| Adapter | 在数据库等存储与 Enforcer 之间加载、保存 Policy | 入门阶段可以先不使用 |

分布式部署中还会遇到 Watcher、Dispatcher、Role Manager 等组件，先掌握 Model、Policy 和 Enforcer 即可。

## 3. 跑通第一个 ACL 示例

先用最简单的 ACL 完成一次从配置到决策的全过程。本例使用 Go，当前官方主版本为 Casbin v3。

### 3.1 创建项目

```bash
mkdir casbin-quickstart
cd casbin-quickstart

go mod init example.com/casbin-quickstart
go get github.com/casbin/casbin/v3
```

项目最终只有三个核心文件：

```text
casbin-quickstart/
├── main.go
├── model.conf
└── policy.csv
```

### 3.2 编写 Model

创建 `model.conf`：

```ini
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = r.sub == p.sub && r.obj == p.obj && r.act == p.act
```

这份 Model 表示：请求和 Policy 的主体、资源、动作全部相等时，该 Policy 匹配；只要至少一条匹配策略允许，请求就被允许。

### 3.3 编写 Policy

创建 `policy.csv`：

```csv
p, alice, data1, read
p, bob, data2, write
```

它表示：

- `alice` 可以读取 `data1`；
- `bob` 可以写入 `data2`；
- 其他未明确允许的请求默认拒绝。

### 3.4 调用 Enforce

创建 `main.go`：

```go
package main

import (
    "fmt"
    "log"

    "github.com/casbin/casbin/v3"
)

func main() {
    e, err := casbin.NewEnforcer("model.conf", "policy.csv")
    if err != nil {
        log.Fatal(err)
    }

    requests := [][]string{
        {"alice", "data1", "read"},
        {"alice", "data1", "write"},
        {"bob", "data2", "write"},
    }

    for _, r := range requests {
        allowed, err := e.Enforce(r[0], r[1], r[2])
        if err != nil {
            log.Fatal(err)
        }
        fmt.Printf("%s %s %s -> %t\n", r[0], r[2], r[1], allowed)
    }
}
```

运行：

```bash
go run .
```

预期输出：

```text
alice read data1 -> true
alice write data1 -> false
bob write data2 -> true
```

### 3.5 Enforce 内部发生了什么

调用：

```go
e.Enforce("alice", "data1", "read")
```

Casbin 会依次执行：

1. 按 `[request_definition]` 把参数映射成 `r.sub`、`r.obj`、`r.act`；
2. 逐条读取 `p` Policy；
3. 使用 `[matchers]` 判断请求和 Policy 是否匹配；
4. 使用 `[policy_effect]` 合并所有匹配结果；
5. 返回 `true` 或 `false`。

`Enforce()` 参数的数量与顺序必须和 `r` 完全一致，这是初学者最常见的错误之一。

## 4. 看懂 Model 的五个部分

Casbin Model 通常包含以下配置段：

| 配置段 | 常用标识 | 作用 |
|--------|----------|------|
| `[request_definition]` | `r` | 定义一次授权请求有哪些字段 |
| `[policy_definition]` | `p` | 定义一条 Policy 有哪些字段 |
| `[role_definition]` | `g`、`g2` | 定义角色或资源关系，可省略 |
| `[policy_effect]` | `e` | 定义多个匹配结果如何合并 |
| `[matchers]` | `m` | 定义请求与 Policy 如何匹配 |

### Request Definition

```ini
[request_definition]
r = sub, obj, act
```

它相当于函数签名：

```text
Enforce(sub, obj, act)
```

多租户系统可以增加域：

```ini
r = sub, dom, obj, act
```

此时调用必须变成：

```text
Enforce(sub, dom, obj, act)
```

### Policy Definition

```ini
[policy_definition]
p = sub, obj, act
```

它定义 CSV 中每条 `p` 记录的字段顺序。字段名可以自定义，但 Model、Policy 和 `Enforce()` 必须保持一致。

### Role Definition

```ini
[role_definition]
g = _, _
```

两个占位符表示一个二元关系：左侧继承右侧。常见 Policy 是：

```csv
g, alice, editor
```

即 `alice` 拥有 `editor` 角色。三元关系通常用于域或租户：

```ini
g = _, _, _
```

```csv
g, alice, admin, tenant-a
```

即 `alice` 只在 `tenant-a` 中拥有 `admin` 角色。

### Policy Effect

最常见的允许覆盖写法：

```ini
e = some(where (p.eft == allow))
```

只要存在一条允许策略就允许。需要显式拒绝优先时，可以使用：

```ini
e = some(where (p.eft == allow)) && !some(where (p.eft == deny))
```

还可以使用 Priority 按策略顺序或优先级决定结果。初学阶段建议从默认拒绝、显式允许开始，不要过早组合复杂效果。

### Matchers

Matcher 是真正的决策表达式：

```ini
m = r.sub == p.sub && r.obj == p.obj && r.act == p.act
```

它可以调用角色关系、内置函数和自定义函数：

```ini
m = g(r.sub, p.sub) && keyMatch2(r.obj, p.obj) && regexMatch(r.act, p.act)
```

阅读 Model 时，先看 `r` 和 `p` 的字段，再看 `m` 如何比较，最后看 `e` 如何合并结果。

## 5. 从 ACL 过渡到 RBAC

ACL 直接把权限授予用户：

```csv
p, alice, data1, read
p, bob, data1, read
p, carol, data1, read
```

用户增多后，可以把权限授予角色，再把用户加入角色。

### RBAC Model

```ini
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
```

### RBAC Policy

```csv
p, reader, data1, read
p, editor, data1, write

g, alice, reader
g, alice, editor
g, bob, reader
```

这里要区分两种记录：

- `p`：角色拥有什么权限；
- `g`：用户拥有什么角色。

因此 `alice` 可以读写 `data1`，`bob` 只能读取。应用可以通过 Casbin Management API 动态添加或删除 Policy 和角色关系；生产环境通常再配合 Adapter 持久化到数据库。

## 6. 常见访问控制模型

| 模型 | 核心关系 | 优点 | 主要代价 | 典型场景 |
|------|----------|------|----------|----------|
| ACL | 主体直接绑定资源权限 | 简单、直观 | 规则数量容易膨胀 | 文件共享、少量对象授权 |
| RBAC | 主体 → 角色 → 权限 | 易批量管理，适合组织职责 | 角色爆炸，动态条件较弱 | 企业后台、岗位权限 |
| ABAC | 根据主体、资源和环境属性决策 | 动态、细粒度 | 属性和策略治理复杂 | 多租户、所有者、合规规则 |
| ReBAC | 根据主体与资源的关系图决策 | 自然表达对象关系 | 图查询和一致性复杂 | 协作文档、组织图、社交关系 |
| PBAC | 由可配置策略组合多个维度 | 表达力强、可集中治理 | 调试、冲突检测要求高 | 跨系统策略平台 |
| BLP | 比较机密性级别 | 防止机密信息向低级别流动 | 约束严格 | 多级机密系统 |
| BIBA | 比较完整性级别 | 防止低可信数据污染高完整性资源 | 约束严格 | 高完整性系统 |
| LBAC | 使用格或偏序比较安全标签 | 支持复杂安全级别 | 建模和运维成本高 | 强制访问控制系统 |

### 如何选择

- 权限规模很小、规则直接：从 ACL 开始；
- 以岗位或用户组管理权限：优先 RBAC；
- 同一角色还要判断租户、所有者、时间或安全级别：RBAC 与 ABAC 组合；
- 权限依赖“成员、协作者、父子组织”等关系：考虑 ReBAC；
- 有严格机密性或完整性分级：考虑 BLP、BIBA 或 LBAC。

这些模型不是互斥的。生产系统常先用 RBAC 判断功能权限，再用 ABAC 校验租户和环境，用 ReBAC 校验对象关系，并以 ACL 表达少量例外共享规则。

### 理论模型与 Casbin 示例的区别

Casbin Editor 中的每个 Model 是一份可运行配置模板，不一定代表一种独立理论：

- Domains、resource roles、time constraints、tags 是 RBAC 的扩展维度；
- KeyMatch 与 IP Match 是 Matcher 使用的匹配函数；
- deny-override 与 Priority 是多条策略的效果合并方式。

选择 Model 时应先明确权限关系，再选择匹配函数和策略效果。

## 7. 三个常用扩展

### 7.1 RESTful 路径匹配

Casbin 内置多种 Matcher 函数：

| 函数 | Pattern 示例 | 特点 |
|------|--------------|------|
| `keyMatch` | `/documents/*` | `*` 通配符 |
| `keyMatch2` | `/documents/:id` | `:id` 路径参数 |
| `keyMatch3` | `/documents/{id}` | `{id}` 路径参数 |
| `keyMatch4` | `/parent/{id}/child/{id}` | 同名参数必须相等 |
| `keyMatch5` | `/documents/{id}/*` | 支持查询参数场景 |
| `regexMatch` | `(GET)\|(POST)` | 正则匹配动作或其他字符串 |
| `ipMatch` | `192.168.1.0/24` | 单个 IP 或 CIDR |

例如：

```ini
m = keyMatch2(r.obj, p.obj) && regexMatch(r.act, p.act)
```

```csv
p, alice, /documents/:id, (GET)|(PUT)
```

即可允许 `alice` 对任意文档路径执行 GET 或 PUT。

### 7.2 Domain / Tenant

普通 RBAC 中，`alice` 一旦是 `admin`，可能在所有空间都拥有管理员权限。Domain 把角色关系限制在某个边界：

```csv
g, alice, admin, tenant-a
g, alice, viewer, tenant-b
```

同一个用户可以在不同租户拥有不同角色。租户信息必须来自可信认证上下文，不能只相信 URL 或请求体中的租户参数。

### 7.3 Policy Effect

当多条 Policy 同时匹配时，需要明确如何合并：

- **allow-override**：任一允许即可允许；
- **deny-override**：任一拒绝即可拒绝；
- **priority**：优先采用顺序更靠前或优先级更高的策略；
- **subject priority**：按主体或角色层级决定策略优先级。

复杂 Effect 会增加理解和调试成本。除非业务确实需要显式拒绝或策略优先级，否则优先使用“默认拒绝 + 显式允许”。

## 8. 使用在线 Editor 学习和调试

[Casbin Policy Editor](https://editor.casbin.org/) 可以直接编辑 Model、Policy 和 Request，不需要先写代码。

建议按以下顺序使用：

1. 在 Model 下拉框选择 `ACL` 或 `RBAC`；
2. 阅读 `[request_definition]`，确认 Request 的参数顺序；
3. 阅读 `[policy_definition]` 和 Policy 数据；
4. 从 Matcher 左到右代入一条 Request；
5. 运行测试，观察允许或拒绝结果；
6. 修改一条 Policy 或 Matcher，再次运行并比较结果；
7. 理解基础模型后再尝试 domains、KeyMatch、deny-override 和 Priority。

### Editor 中的全部 30 个预置 Model

截至 2026 年 8 月 4 日，首页 Model 下拉框包含以下示例。

#### ACL（4 个）

| # | Model key | 页面显示名 | 说明 |
|---|-----------|------------|------|
| 1 | `basic` | ACL | 直接匹配主体、资源和动作 |
| 2 | `basic_with_root` | ACL with superuser | 增加 `root` 超级用户 |
| 3 | `basic_without_resources` | ACL without resources | 只按主体和动作授权 |
| 4 | `basic_without_users` | ACL without users | 只按资源和动作授权 |

#### RBAC（12 个）

| # | Model key | 页面显示名 | 说明 |
|---|-----------|------------|------|
| 5 | `rbac` | RBAC | 基础角色访问控制 |
| 6 | `rbac_with_multiple_roles` | RBAC with multiple roles | 一个用户拥有多个角色 |
| 7 | `rbac_with_resource_roles` | RBAC with resource roles | 用户角色与资源角色 |
| 8 | `rbac_with_domains` | RBAC with domains/tenants | 域或租户内角色 |
| 9 | `rbac_with_pattern` | RBAC with pattern | 对角色主体使用模式匹配 |
| 10 | `rbac_with_all_pattern` | RBAC with all pattern | 对主体和域使用模式匹配 |
| 11 | `rbac_with_deny` | RBAC with deny-override | 显式拒绝覆盖允许 |
| 12 | `rbac_with_domains_and_resources` | RBAC with domains and resource hierarchy | 域与资源层级 |
| 13 | `rbac_with_time` | RBAC with time constraints | 时间范围约束 |
| 14 | `rbac_with_tags` | RBAC with tags | 资源标签或资源组 |
| 15 | `rbac_with_resource_filter` | RBAC with resource filter | 资源路径过滤 |
| 16 | `rbac_with_resource_roles_and_deny` | RBAC with resource roles and deny rules | 资源角色与拒绝规则 |

#### ABAC、ReBAC 与 PBAC（4 个）

| # | Model key | 页面显示名 | 说明 |
|---|-----------|------------|------|
| 17 | `abac` | ABAC | 根据请求中的属性决策 |
| 18 | `abac_with_policy_rule` | ABAC with policy rule | 通过 `eval()` 执行 Policy 属性表达式 |
| 19 | `rebac` | ReBAC | 根据主体与资源的关系决策 |
| 20 | `pbac` | PBAC | 执行主体规则和资源规则 |

#### 多级安全模型（3 个）

| # | Model key | 页面显示名 | 说明 |
|---|-----------|------------|------|
| 21 | `blp` | BLP | Bell-LaPadula 机密性模型 |
| 22 | `biba` | BIBA | Biba 完整性模型 |
| 23 | `lbac` | LBAC | 基于格的访问控制 |

#### RESTful、网络与策略效果（7 个）

| # | Model key | 页面显示名 | 说明 |
|---|-----------|------------|------|
| 24 | `keymatch` | RESTful (KeyMatch) | `*` 路径通配 |
| 25 | `keymatch2` | RESTful (KeyMatch2) | `:id` 路径参数 |
| 26 | `keymatch3` | RESTful (KeyMatch3) | `{id}` 路径参数 |
| 27 | `keymatch4` | RESTful (KeyMatch4) | 同名路径参数一致性 |
| 28 | `keymatch5` | RESTful (KeyMatch5) | 路径与查询参数匹配 |
| 29 | `ipmatch` | IP match | IP 或 CIDR 匹配 |
| 30 | `priority` | Priority | 策略优先级 |

Model Gallery 当前只展示 26 张卡片；`KeyMatch2`～`KeyMatch5` 仍存在于首页下拉框，只是没有独立 Gallery 卡片。

## 9. 接入业务前要知道的事情

### Policy 如何更新

不要直接在业务代码中维护大量 CSV 字符串。生产环境通常采用：

- Management API 添加、删除 Policy 和角色关系；
- Adapter 把 Policy 持久化到数据库；
- Watcher 或 Dispatcher 通知其他实例刷新策略；
- 管理后台处理申请、审批、发布和回收；
- 审计日志记录谁在何时修改了什么权限。

### 授权应该放在哪里

- 前端隐藏按钮只能改善用户体验，不能代替服务端授权；
- 网关适合做粗粒度接口校验，业务服务仍要做对象级授权；
- 列表查询需要按授权条件过滤，不能先返回全部数据再由前端隐藏；
- 修改、删除、批量和导出接口都必须覆盖；
- 授权依赖不可用时，敏感操作通常应失败关闭。

### 常见错误

| 错误 | 后果 | 建议 |
|------|------|------|
| `Enforce()` 参数顺序和 `r` 不一致 | 规则始终不匹配或错误放行 | 把调用封装为固定函数并写测试 |
| 把用户名、角色或租户直接取自请求参数 | 可伪造身份或跨租户 | 从可信认证上下文读取 |
| 只判断接口权限，不判断具体资源 | 产生 BOLA / IDOR | 加载资源的租户、所有者等属性 |
| 把所有规则塞进一个复杂 Matcher | 难以理解和回归 | 从简单模型开始，拆分策略职责 |
| Policy 修改后各实例缓存不同步 | 权限撤销不能及时生效 | 使用 Watcher/Dispatcher 和版本机制 |
| 只测试允许路径 | 越权缺陷未被发现 | 增加横向、纵向、跨租户反例 |

## 10. 实际样例：多租户文档 API

下面把前面的知识组合成一个可运行示例。

### 10.1 需求

系统有多个租户，每个租户包含文档资源：

- `admin`：可以创建、读取、修改和删除文档；
- `editor`：可以创建、读取和修改文档，不能删除；
- `viewer`：只能读取；
- 用户在不同租户可以拥有不同角色；
- API 路径使用 `/documents` 和 `/documents/:id`；
- 未明确允许的请求默认拒绝。

用户关系如下：

| 用户 | tenant-a | tenant-b |
|------|----------|----------|
| alice | admin | viewer |
| bob | editor | - |
| carol | viewer | - |
| dave | - | admin |

### 10.2 Model

创建 `model.conf`：

```ini
[request_definition]
r = sub, dom, obj, act

[policy_definition]
p = sub, dom, obj, act

[role_definition]
g = _, _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub, r.dom) && r.dom == p.dom && keyMatch2(r.obj, p.obj) && regexMatch(r.act, p.act)
```

逐段理解：

- `r` 增加 `dom`，因此每次请求都携带租户；
- `g = _, _, _` 表示“用户、角色、租户”的三元关系；
- `g(r.sub, p.sub, r.dom)` 检查用户在当前租户是否拥有 Policy 中的角色；
- `r.dom == p.dom` 确保 Policy 属于当前租户；
- `keyMatch2` 用于匹配 `/documents/:id`；
- `regexMatch` 让一条 Policy 表示多个 HTTP Method。

### 10.3 Policy

创建 `policy.csv`：

```csv
p, admin, tenant-a, /documents, (GET)|(POST)
p, admin, tenant-a, /documents/:id, (GET)|(PUT)|(DELETE)
p, editor, tenant-a, /documents, (GET)|(POST)
p, editor, tenant-a, /documents/:id, (GET)|(PUT)
p, viewer, tenant-a, /documents, GET
p, viewer, tenant-a, /documents/:id, GET

p, admin, tenant-b, /documents, (GET)|(POST)
p, admin, tenant-b, /documents/:id, (GET)|(PUT)|(DELETE)
p, viewer, tenant-b, /documents, GET
p, viewer, tenant-b, /documents/:id, GET

g, alice, admin, tenant-a
g, alice, viewer, tenant-b
g, bob, editor, tenant-a
g, carol, viewer, tenant-a
g, dave, admin, tenant-b
```

### 10.4 Go 程序

创建 `main.go`：

```go
package main

import (
    "fmt"
    "log"

    "github.com/casbin/casbin/v3"
)

type request struct {
    sub, dom, obj, act string
}

func main() {
    e, err := casbin.NewEnforcer("model.conf", "policy.csv")
    if err != nil {
        log.Fatal(err)
    }

    requests := []request{
        {"alice", "tenant-a", "/documents/42", "DELETE"},
        {"bob", "tenant-a", "/documents/42", "PUT"},
        {"bob", "tenant-a", "/documents/42", "DELETE"},
        {"carol", "tenant-a", "/documents/42", "GET"},
        {"carol", "tenant-a", "/documents", "POST"},
        {"alice", "tenant-b", "/documents/42", "GET"},
        {"alice", "tenant-b", "/documents/42", "DELETE"},
        {"alice", "tenant-c", "/documents/42", "GET"},
    }

    for _, r := range requests {
        allowed, err := e.Enforce(r.sub, r.dom, r.obj, r.act)
        if err != nil {
            log.Fatal(err)
        }
        fmt.Printf("%-5s %-8s %-14s %-6s -> %t\n", r.sub, r.dom, r.obj, r.act, allowed)
    }
}
```

安装依赖并运行：

```bash
go mod init example.com/casbin-demo
go get github.com/casbin/casbin/v3
go run .
```

输出：

```text
alice tenant-a /documents/42  DELETE -> true
bob   tenant-a /documents/42  PUT    -> true
bob   tenant-a /documents/42  DELETE -> false
carol tenant-a /documents/42  GET    -> true
carol tenant-a /documents     POST   -> false
alice tenant-b /documents/42  GET    -> true
alice tenant-b /documents/42  DELETE -> false
alice tenant-c /documents/42  GET    -> false
```

结果体现了三件事：

1. `alice` 在 `tenant-a` 是管理员，但在 `tenant-b` 只是只读用户；
2. `bob` 的 editor 角色允许修改但不允许删除；
3. `tenant-c` 没有角色和 Policy，因此默认拒绝。

### 10.5 接入真实 HTTP 服务

真实服务中的授权调用通常位于中间件或业务方法入口：

```text
sub = 已验证 Token 中的用户 ID
dom = 服务端确认的当前租户
obj = 规范化后的请求路径或具体资源标识
act = HTTP Method 或业务动作

allowed = Enforce(sub, dom, obj, act)
```

还要注意：

- 从认证上下文获取 `sub` 和 `dom`，不要信任客户端伪造值；
- 对 `/documents/42` 完成路径级授权后，仍应加载文档并校验其真实 `tenant_id`；
- 如果要限制“只能修改自己创建的文档”，应再加入资源所有权属性或 ReBAC 关系；
- 把 Policy 迁移到数据库 Adapter，并为多实例配置策略同步；
- 为上述 8 个请求保留自动化测试，新增角色或接口时同步扩展拒绝用例。

## 11. 策略加载方式对比

在多 DP（Digital Product）或多租户场景下，Casbin Policy 来自哪里、何时装入内存、跨实例如何同步，直接决定了授权服务的内存占用、实现成本和一致性模型。常见做法有三种：

| 维度 | A. Adapter 直连（全量） | B. Decision 组装（按域惰性） | C. Filtered Adapter（折中） |
|------|------------------------|------------------------------|------------------------------|
| 数据来源 | Casbin 的 `casbin_rule` 表，存 p/g 行 | 领域表（Role / Permission / Binding）直接查 | 同 A，但按 dom 过滤加载 |
| 加载时机 | 启动时全量载入内存 | 首次访问某域时构造，缓存该域 enforcer | 启动或首次访问时按域加载 |
| 领域模型 | 被 `casbin_rule` 行格式绑架，需与业务表双写或建视图 | 完全自主，管理 API 与审计自然 | 同 A |
| 内存占用 | 全部 DP 的策略常驻 | 只驻留活跃域 | 只驻留已加载域 |
| 多实例同步 | 需要 Watcher（Redis/etcd）广播变更 | 复用已有版本号机制，版本变则丢弃该域 | 需要 Watcher |
| 实现成本 | 最低，社区标准做法 | 中，需自写加载与缓存 | 中低 |

关键差异在规模：中心化 AuthZ 承载所有 DP，g 行数约等于全平台绑定总数，p 行数约等于角色乘权限点。全量常驻在 DP 数量增长后会变成负担，而单次判定只需要一个域的策略。

另一个差异是双写。方式 A 要求策略以 Casbin 的行格式落库，但管理面需要的是 Role、Permission、Binding、AccountNode 这些领域实体，两边得同步，审计也要基于领域表而非 `casbin_rule`。

推荐方式 B：按 `dom` 惰性构造 enforcer，用已有的 `INCR authz:{app_id}:ver` 版本号做失效，不额外引入 Watcher。代价是要自己写加载逻辑——从领域表查角色绑定和角色权限、拼成 p/g 数组喂给内存 Model。若后续觉得自写成本高，可平滑退到 C。

## 参考

- [Apache Casbin：Get Started](https://casbin.apache.org/docs/get-started)
- [Apache Casbin：How It Works](https://casbin.apache.org/docs/how-it-works)
- [Apache Casbin：Model Syntax](https://casbin.apache.org/docs/syntax-for-models)
- [Apache Casbin：Supported Models](https://casbin.apache.org/docs/supported-models)
- [Apache Casbin：Functions in Matchers](https://casbin.apache.org/docs/function)
- [Casbin Policy Editor](https://editor.casbin.org/)
- [Casbin Editor：全部示例源码](https://github.com/apache/casbin-editor/blob/master/app/components/editor/casbin-mode/example.ts)
- [Casbin Editor：Gallery 元数据](https://github.com/apache/casbin-editor/blob/master/app/config/modelMetadata.ts)
