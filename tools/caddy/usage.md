---
title: caddy usage
categories: 
  - [工具,caddy]
tags:
  - caddy
date: "2021-08-17T00:00:00+08:00"
update: "2021-08-17T00:00:00+08:00"
---

# 文档

- [首页](https://caddyserver.com/docs/)
- [反向代理配置](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy)

# 示例

```
localhost {
    respond "caddy server"
}

http://git.example.com {
    reverse_proxy 192.168.1.2:8000
}

http://doc.example.com:85 {
    reverse_proxy 192.168.1.3:8000 {
        header_down Location "^(http://doc.example.com)(.*)$" "$1:85$2"
    }
}
```

# 注意

- 如果监听端口是 80 或不设置端口（默认监听 80），那么在处理请求时，看做 http 协议请求
- 如果监听端口是非 80，那么请求被当做 https 协议请求
- 显式指定 http 协议，那么请求看做 http 协议处理

```shell
example.com { ... }            # http 协议
example.com:81 { ... }         # https 协议
http://example.com:81 { ... }  # http 协议
```

# 问题

## 跳转时端口丢失

原因是服务再返回请求设置 header 的 Location 字段时，没有把端口加进去，导致的现象是访问 `http://doc.example.com:85` 服务跳转到 `http://doc.example.com/index`，由于端口丢失，导致无法访问。

从两个思路解决问题。

- 服务端，在返回时设置 header 的 Location 把 port 加上（`http://doc.example.com:85/index`）
- 代理服务器处理，处理方式是替换 response header 的 Location，加上端口

下面是 Caddy 的配置示例。

```shell
header_down Location "^(http://doc.example.com)(.*)$" "$1:85$2"
```

- header_down，修改 response 的 header。相反，header_up 是修改请求 header
- Location，response header 字段
- `"^(http://doc.example.com)(.*)$"`， 匹配域名和 path
- `"$1:85$2"`，在域名和 path 中间加端口