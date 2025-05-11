---
title: vs code server
categories: 
  - [工具]
tags:
  - 工具
date: "2021-05-10T00:00:00+08:00"
update: "2021-05-10T00:00:00+08:00"
---

# 安装

```shell
curl -fsSL https://code-server.dev/install.sh | sh
```

更多参考[这里](https://github.com/coder/code-server)。

# 配置

详细文档参考[这里](https://coder.com/docs/code-server/latest/guide)。默认配置文件路径是 `~/.config/code-server/config.yaml`，也可以通过 `--bind-addr` 参数指定。

配置文件示例。

```yaml
bind-addr: 0.0.0.0:9025
auth: password
password: 67da2351225608a4384150e8
cert: false # 如果使用 https, cert 改为 true
```

## 配置 https 自认证

```shell
# 命令行启动
code-server --cert # 默认证书文件在 ~/.local/share/code-server

# 基于配置启动，修改配置文件
cert: true # 设置为 true 会自动创建 self-signed 证书
```

# 运行

```shell
code-server --config /path/to/config --bind-addr ip:port
```

# 服务管理

```shell
# 配置自启动
sudo systemctl enable code-server@{user}
# 手动启动
sudo systemctl start code-server@{user}
# 手动停止
sudo systemctl stop code-server@{user}
```

