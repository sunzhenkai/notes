---
title: nginx 日志分析
categories: 
  - [linux,software]
tags:
  - linux
  - nginx
date: 2021/09/08 00:00:00
update: 2021/09/08 00:00:00
---

# 日志文件合并

```shell
# 对于 gz 格式日志文件，使用 gzcat
$ gzcat access-*.gz > access-all.log
```

# 分析

## goaccess

### 安装

使用 brew 或[下载](https://goaccess.io/)。

```shell
$ brew install goaccess
```

### 日志格式匹配

nginx 日志格式配置需要转换为 goaccess 可识别的日志格式，下面是示例。

| nginx 配置                                                   | goaccess 格式配置                                            |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for" "$request_body" "$upstream_addr" $upstream_status $upstream_response_time $request_time` | log-format `%h %^ [%d:%t %^] "%r" %s %b "%R" "%u" "%^" "%^" "%^" %^ %^ %T`<br />date-format `%d/%b/%Y`<br/>time-format `%T` |
| `$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_time $upstream_addr $upstream_response_time $pipe` | `%h %^[%d:%t %^] "%r" %s %b "%R" "%u" %T %^`                 |

### 日志格式配置

分析前，需要配置日志格式。日志格式可以在 `~/.goaccessrc` 文件配置，也可以在命令行中指定。

```shell
# ~/.goaccessrc
log-format %h %^[%d:%t %^] "%r" %s %b "%R" "%u" "%^" "%^" "%^" %^ %^ %T
date-format %d/%b/%Y
time-format %T


# 使用命令行指定
goaccess access-all.log --log-format='%h %^[%d:%t %^] "%r" %s %b "%R" "%u" "%^" "%^" "%^" %^ %^ %T' --date-format='%d/%b/%Y' --time-format='%T'
```

### 离线分析

```shell
# 使用 ~/.goaccessrc 文件配置日志格式
$ LANG="en_US.UTF-8" goaccess access-all.log -o report.html

# 使用命令行指定日志格式
$ LANG="en_US.UTF-8" goaccess access-all.log --log-format='%h %^[%d:%t %^] "%r" %s %b "%R" "%u" "%^" "%^" "%^" %^ %^ %T' --date-format='%d/%b/%Y' --time-format='%T' -o report.html
```

> 如果出错，可以尝试去掉 `LANG="en_US.UTF-8"`

