---
title: elastic data
categories: 
  - [架构, 搜索引擎]
tags:
  - 架构
  - 搜索引擎
  - es
date: "2021-11-22T00:00:00+08:00"
update: "2021-11-22T00:00:00+08:00"
---

# 修改配置

## 接口修改

```shell
# dev tools
PUT <index>
{
    "settings" : {
        "index" : {
            "<name>" : <value>
        }
    }
}

# curl
curl -X PUT -u <user>:<password> "http://<host>:<port>/<index>" -d
```



# 索引配置

```shell
{
    "settings" : {
        "index" : {
            "number_of_shards" : 5,
            "number_of_replicas" : 5
        }
    }
}
```

