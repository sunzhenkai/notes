---
title: 认证（Authentication）
categories:
  - 计算机科学
  - 工程架构
  - 安全
tags:
  - 安全
  - 认证
  - OAuth
  - OIDC
date: "2026-08-04T15:16:46+08:00"
update: "2026-08-04T15:16:46+08:00"
---

# 认证（Authentication）

认证（AuthN）用于验证一个主体所声明的身份。主体既可以是人，也可以是服务、设备或自动化任务；认证的结果应是稳定的主体标识和可信的认证上下文，而不只是一个“登录成功”布尔值。

## 认证因素

认证凭据通常分为三类：

| 因素 | 含义 | 示例 |
|------|------|------|
| 知识因素 | 知道的内容 | 密码、PIN |
| 持有因素 | 拥有的物品或密钥 | 硬件安全密钥、Passkey、TOTP 设备、客户端证书 |
| 固有因素 | 身体特征 | 指纹、面容 |

多因素认证（MFA）应组合不同类别的因素。密码加安全问题仍然属于两个知识因素，不能提供真正的多因素保护。位置、设备信誉和行为特征通常更适合作为风险信号，用于触发二次认证，而不是单独作为身份凭据。

## 认证生命周期

一个完整的认证系统不只有登录页面，还需要覆盖：

1. **身份注册与核验**：建立主体和现实身份或组织关系之间的绑定。
2. **凭据签发**：设置密码、注册 Passkey、发放证书或密钥。
3. **凭据验证**：验证凭据，并实施限速、风险检测和抗重放保护。
4. **会话建立**：生成新的会话标识或令牌，记录认证时间、方式和强度。
5. **增强认证**：访问高风险功能前执行 step-up authentication。
6. **恢复与重置**：找回流程的安全强度不能低于正常登录流程。
7. **轮换与撤销**：在泄露、离职、设备丢失或权限变化时使凭据及时失效。

## 常见认证方式

| 方式 | 适用场景 | 优点 | 主要风险与注意事项 |
|------|----------|------|--------------------|
| 密码 | 通用的人类用户登录 | 部署简单、兼容性好 | 弱密码、撞库、钓鱼；需要安全哈希、限速和 MFA |
| Passkey / WebAuthn | Web 和原生应用登录 | 抗钓鱼，不依赖共享秘密 | 需要设计设备同步、丢失与恢复流程 |
| TOTP / 硬件安全密钥 | MFA 或增强认证 | 标准成熟；安全密钥抗钓鱼能力更强 | TOTP 仍可能被实时钓鱼，恢复码必须安全保存 |
| 客户端证书 / mTLS | 服务间、设备认证 | 双向验证、适合工作负载身份 | 证书签发、主体映射、轮换和吊销较复杂 |
| API Key | 项目、脚本或简单服务调用 | 易于使用 | 常只能标识应用而非最终用户；必须限定权限、支持轮换且不得出现在 URL 中 |
| 联邦登录 | 跨系统单点登录 | 统一身份源和登录策略 | 必须正确验证签名、签发者、受众、回调地址和协议状态参数 |

### 密码

- 全链路使用 TLS，密码不得写入日志或分析事件。
- 使用专门的、带盐的自适应密码哈希算法，例如 Argon2id；也可根据平台采用 scrypt、bcrypt 或 PBKDF2。不要使用可逆加密或 MD5、SHA-1、SHA-256 等快速哈希直接保存密码。
- 允许用户使用足够长的密码和密码管理器，不应禁止粘贴；用常见密码和已泄露密码列表做拦截。
- 不要仅因时间流逝强制周期性改密；在疑似泄露、凭据恢复等事件发生时再要求更换。
- 对登录和找回接口做基于账号、来源和风险的限速。响应文案应避免泄露“账号是否存在”，同时防止锁定机制被利用来拒绝服务。

### Passkey 与 WebAuthn

Passkey 基于公钥密码学。服务端保存公钥，私钥保留在用户设备或受保护的同步体系中；认证响应与站点 origin 绑定，因此比密码和普通 OTP 更能抵抗钓鱼。实现时仍需验证 challenge、origin、RP ID、签名计数等数据，并为新增设备和账号恢复建立严格流程。

## 会话与令牌

认证成功后，系统通常通过会话或令牌延续认证状态。

### 服务端会话

浏览器仅持有不可预测的随机会话 ID，身份和状态保存在服务端。

- Cookie 至少设置 `Secure`、`HttpOnly`，并根据业务选择合适的 `SameSite`。
- 登录成功、权限提升或敏感属性变化后轮换会话 ID，防止会话固定攻击。
- 同时设置空闲超时和绝对超时；注销、改密和风险事件发生后使会话失效。
- Cookie 自动随请求发送，因此仍需结合 SameSite、CSRF Token 和来源检查防御 CSRF。

### Access Token

Access Token 是客户端访问资源服务器的凭据，应只发送给其 `audience` 对应的 API。Opaque Token 由授权服务器保存状态，资源服务器通过自省或网关查询；JWT 可由资源服务器本地验证，减少查询，但撤销和声明变更更困难。

验证 JWT 时至少要：

1. 固定允许的签名算法，不接受令牌自行选择的不安全算法；
2. 验证签名，并安全获取、缓存和轮换验证密钥；
3. 验证 `iss`、`aud`、`exp`、`nbf` 等声明；
4. 根据业务验证主体、授权范围和令牌类型，必要时使用 `jti` 防重放；
5. 拒绝缺失关键声明或类型不符的令牌。

JWT 默认只是签名编码，并未加密；任何拿到令牌的人通常都能读取 Payload。因此不要放入密码、私钥或不必要的个人信息。Bearer Token 一旦泄露即可被持有者使用，应保持短期有效并避免写入日志、URL、错误信息或不可信存储。

### Refresh Token

Refresh Token 只用于向授权服务器换取新的 Access Token，不应发送给业务 API。应限制客户端和授权范围，采用轮换与重复使用检测，并在注销、异常使用和安全事件后撤销。浏览器应用可优先考虑 Backend for Frontend（BFF）等模式，避免让长期令牌暴露给页面 JavaScript。

## OAuth 2.0、OpenID Connect 与 SAML

这些协议解决的问题不同：

| 协议 | 主要用途 | 关键结果 |
|------|----------|----------|
| OAuth 2.0 | 委托授权 | Access Token；本身不是用户认证协议 |
| OpenID Connect（OIDC） | 在 OAuth 2.0 之上提供身份认证 | ID Token 和标准化用户信息 |
| SAML 2.0 | 企业身份联合与单点登录 | 由身份提供方签发的 SAML Assertion |

OIDC 中的 ID Token 是客户端验证登录结果的凭据，Access Token 才用于调用资源 API。不要把 ID Token 当成 Access Token 发送给业务 API，也不要仅解析 Token 而跳过签名、签发者、受众和时效验证。

### 常用流程

- **Authorization Code + PKCE**：Web、单页应用和原生应用的首选交互式登录流程。严格匹配预注册的重定向 URI，并校验 `state`、PKCE；OIDC 还应校验 `nonce`。
- **Client Credentials**：没有最终用户参与的服务到服务调用。权限绑定到工作负载身份，不能冒充用户流程。
- **Device Authorization Grant**：输入能力受限的电视、命令行等设备。

避免使用 Resource Owner Password Credentials 模式；新系统也不应采用 Implicit Flow。原生应用应使用系统浏览器，而不是嵌入式 WebView 收集用户凭据。

## 认证上下文

认证系统传递给授权层的信息应最小且明确，例如：

```json
{
  "subject_id": "user-123",
  "tenant_id": "tenant-a",
  "auth_time": 1785834000,
  "auth_methods": ["passkey"],
  "assurance_level": "high",
  "session_id": "session-456"
}
```

`tenant_id`、角色等安全属性必须来自可信身份源或服务端查询，不能直接相信请求参数。授权层还应考虑认证新鲜度：转账、修改 MFA、导出敏感数据等操作可以要求近期完成高强度认证。

## HTTP 状态码

- 缺少、失效或无法接受的认证凭据通常返回 `401 Unauthorized`，并按协议提供 `WWW-Authenticate`。
- 身份已经确认但无权执行操作通常返回 `403 Forbidden`。
- 为避免暴露资源是否存在，可以在策略一致的前提下对部分越权访问返回 `404 Not Found`。

## 检查清单

- [ ] 所有认证流量都使用 TLS，秘密不会进入 URL、日志和前端埋点。
- [ ] 密码、密钥、恢复码和 Token 使用适合各自威胁模型的存储方式。
- [ ] 登录、注册、MFA、找回、改密和注销均有滥用防护与审计。
- [ ] 会话在登录、提权和安全事件后正确轮换或撤销。
- [ ] Token 严格验证算法、签名、签发者、受众、时效和类型。
- [ ] 关键操作支持增强认证，恢复流程不会绕过 MFA。
- [ ] 服务账号和 API Key 具有负责人、用途、到期时间、最小权限及轮换机制。

## 参考

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 7636: Proof Key for Code Exchange](https://www.rfc-editor.org/rfc/rfc7636)
- [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700)
