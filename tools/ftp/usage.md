---
title: ftp client usage
categories: 
  - [tools,ftp]
tags:
  - ftp
date: 2022/1/10 00:00:00
update: 2022/1/10 00:00:00
---

```shell
Usage: { ftp | pftp } [-46pinegvtd] [hostname]
   -4: use IPv4 addresses only
   -6: use IPv6, nothing else
   -p: enable passive mode (default for pftp)
   -i: turn off prompting during mget
   -n: inhibit auto-login
   -e: disable readline support, if present
   -g: disable filename globbing
   -v: verbose mode
   -t: enable packet tracing [nonfunctional]
   -d: enable debugging
```

# 登录

```shell
$ ftp
ftp> open {ip}
```

