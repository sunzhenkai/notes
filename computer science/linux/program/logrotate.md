---
title: logrotate
categories:
  - [linux, software]
tags:
  - linux
    - logrotate
date: "2022-03-31T00:00:00+08:00"
update: "2022-03-31T00:00:00+08:00"
---

# 配置

## 示例

`rotate.conf`。

```shell
/home/wii/www/logs/*.log {
    daily
    rotate 30
    missingok
    nocompress
    copytruncate
    notifempty
    dateext
}
```

# Rotate

**触发 rotate**

```shell
logrotate [options] [config-file]

logrotate -v -s /home/wii/www/logs/rotate-status rotate.conf

-v: 打印具体信息
-s: 指定 status 保存路径; 默认在 /var/lib/logrotate/ 下，可能没有权限
```

> **注意**
>
> - logrotate 根据 status 文件判断是否需要 rotate，第一次执行可能只创建 status 文件，并不会创建 rotate 日志文件。如果想要触发，修改 status 文件记录的最后一次 rotate 时间，以触发 rotate