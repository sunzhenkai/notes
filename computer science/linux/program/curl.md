---
title: curl
categories:
  - [linux, software]
tags:
  - linux
    - curl
date: "2021-09-14T00:00:00+08:00"
update: "2021-09-14T00:00:00+08:00"
---

# 参数

```shell
-X	指定请求方法
-H  添加 Header，添加多个可通过重复指定
```

# 示例

```shell
# 格式
curl [options] [URL...]

# 指定方法
curl -X POST [URL...]

# 添加 Header
curl -H "Content-Type: application/json" [URL...]
```

