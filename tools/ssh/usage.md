---
title: ssh
categories: 
  - [工具,ssh]
tags:
  - ssh
date: "2025-06-06T00:00:00+08:00"
update: "2025-06-06T00:00:00+08:00"
---

# 配置

## ProxyCommand

```shell
Host relay
  HostName 192.168.6.5
  User wii
  IdentityFile ~/.ssh/id_rsa
Host dev
  HostName 192.168.6.2
  User wii
  IdentityFile ~/.ssh/id_rsa
  ProxyCommand ssh relay -W %h:%p
```

