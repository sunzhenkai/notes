---
title: moviepilot
categories: 
  - [play,server]
tags:
  - moviepilot
date: 2024/03/06 00:00:00
update: 2024/03/06 00:00:00
---

# 站点

- 必须配置一个认证站点

## 配置认证站点

以 HDFans 为例。

![image-20240306194634129](usage/image-20240306194634129.png)

需要设置三个环境变量。

```shell
AUTH_SITE=hdfans
HDFANS_UID=...
HDFANS_PASSKEY=...
```

### 获取 UID

UID 是数字的用户 ID，点击用户名，跳转到用户信息页面，有 UID 一行。

![image-20240306194856879](usage/image-20240306194856879.png)

### 获取 PASSKEY

![image-20240306194948521](usage/image-20240306194948521.png)

一般在站点的设置页面的设置首页，这里的 **密钥** 就是 PASSKEY。

# 媒体服务

## 获取 Plex 的 API 密钥

找到一个媒体，点击这里的更多。

![image-20240307102003310](usage/image-20240307102003310.png)

再点击获取信息。

![image-20240307102038095](usage/image-20240307102038095.png)

![image-20240307102122293](usage/image-20240307102122293.png)

再点击 查看 XML。

![image-20240307102705931](usage/image-20240307102705931.png)

在最后有一个 X-Plex-Token，把等号后面的字符串填到 API 密钥那里。

![image-20240307102844578](usage/image-20240307102844578.png)

# 注意

- MoviePilot 使用三方工具下载内容（比如 Transmission），并通过工具的 API 调用，需要注意的是，下载路径是 MoviePilot 制定的下载路径，如果 Transmission 在另外的容器里面，要确保下载路径在 MoviePilot 和 下载工具的映射**是一致的**。

# 辅种

MoviePilot 版本 2.1.9-1。辅种原理是，通过种子的 HASH 数据，确认相同的种子，再从其他站点下载种子，只要 HASH 校验通过即可。

1. 注册 [IYUU](https://iyuu.cn/) 获取 Token（微信关注后发送 Token）。
2. 下载插件 **IYUU 站定绑定**
   1. 下载后，在已安装点击插件
   2. 输入 IYUU Token，点击保存，关闭插件配置
   3. 再次点击插件，选站点，输入密钥、UID，点击保存
   4. 查看日志校验是否成功，如果不成功可尝试绑定其他站点

![截屏2025-01-08 21.31.55](./usage/截屏2025-01-08 21.31.55.png)

3. 下载插件 IYUU 自动辅种
   1. 启用插件
   2. 输入 IYUU Token
   3. 选择下载器
   4. 选择站点
   5. 保存即可

![image-20250108213217556](./usage/image-20250108213217556.png)

