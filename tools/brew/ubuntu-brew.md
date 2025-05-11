---
title: brew - ubuntu
categories: 
  - [工具,brew]
tags:
  - brew
date: "2022-05-08T00:00:00+08:00"
update: "2022-05-08T00:00:00+08:00"
---

# 安装

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 配置
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/ubuntu/.profile
```

# 服务

## consul

```shell
# 安装
brew install consul

# 配置
vim /home/linuxbrew/.linuxbrew/Cellar/consul/1.12.0/homebrew.consul.service
## 修改 ExecStart
ExecStart=/home/linuxbrew/.linuxbrew/opt/consul/bin/consul agent -dev -bind 0.0.0.0 -advertise 127.0.0.1 -client 0.0.0.0

# 手动启动
/home/linuxbrew/.linuxbrew/opt/consul/bin/consul agent -dev -bind 0.0.0.0 -advertise 127.0.0.1 -client 0.0.0.0
```

