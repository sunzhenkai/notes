---
title: nc
categories: 
  - [linux,程序]
tags:
  - sed
date: "2021-01-11T00:00:00+08:00"
update: "2021-01-11T00:00:00+08:00"
---

# 传送文件

```shell
# receiver
$ nc -l -p {port} > something.tar.gz < /dev/null
# sender
$ cat something.tar.gz | nc {server-ip} {port}

# example
nc -l -p 12345 > something.tar.gz < /dev/null
cat something.zip | nc 127.0.0.1 12345
```

