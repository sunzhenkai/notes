---
title: vector
categories: 
  - [架构]
tags:
  - 架构
date: 2023/05/30 00:00:00
update: 2023/05/30 00:00:00
---

# 配置

## source

### file

```shell
[sources.test]
type = "file"
include = [ "/tmp/test.log" ]
line_delimiter = "$$\n"

# unicode
line_delimiter = "\u0003\u0004\n"
```

**line_delimiter**

```toml
\b         - backspace       (U+0008)
\t         - tab             (U+0009)
\n         - linefeed        (U+000A)
\f         - form feed       (U+000C)
\r         - carriage return (U+000D)
\"         - quote           (U+0022)
\\         - backslash       (U+005C)
\uXXXX     - unicode         (U+XXXX)
\UXXXXXXXX - unicode         (U+XXXXXXXX)
```

## example

```shell
[api]
enabled = true
address = "0.0.0.0:8686"

[sources.test]
type = "file"
include = [ "/tmp/test.log" ]
line_delimiter = "$$\n"

[sinks.console]
inputs = ["test"]
target = "stdout"
type = "console"
encoding.codec = "text"
```

# 安装

## docker

[文档](https://vector.dev/docs/setup/installation/platforms/docker/)。

```shell
# pull image
$ docker pull timberio/vector:0.30.0-debian
# create container
$ docker run \
  -d \
  -v $PWD/vector.toml:/etc/vector/vector.toml:ro \
  -v /tmp/test.log:/tmp/test.log \
  --name vector \
  -p 8686:8686 \
  timberio/vector:0.30.0-debian
```

# trouble shooting
## 日志滚动后无法更新
### 可能原因
vector 在日志文件轮转之后，默认会计算日志文件的前n个字节的 check sum, 如果值一直，则不会监听新的文件。如果日志文件有固定的前缀，那么每次日志轮转，check sum 会保持一致，那么会无法切换至新的文件。
比如，vector 一开始监听 `debug.log` 文件，文件到达一定条件后做轮转操作，移动 `debug.log` 为 `debug.log.1`，创建新的 `debug.log` 文件。如果 `debug.log` 和 `debug.log.1` 有相同的 check sum 值，那么 vector 不会监听新的文件。

### 解决方案
修改 fingerprinter 的计算策略为 `device_and_inode`。
```yaml
[sources.debug-log]
  type         = "file"
  include      = ["/app/name/debug.log"]
  max_line_bytes = 409600 # optional, default, bytes
  ignore_older = 10 #10s
  line_delimiter = "\u001e\u001f\n"
  [sources.debug-log.fingerprinting]
    strategy = "device_and_inode"
```

### 相关 issues
- [The problem with fingerprinters](https://github.com/vectordotdev/vector/issues/2701)