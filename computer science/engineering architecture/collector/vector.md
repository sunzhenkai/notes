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

