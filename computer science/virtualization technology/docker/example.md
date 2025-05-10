---
title: docker example
categories: 
  - [计算机科学,虚拟化,docker]
tags:
  - docker
date: "2022-07-28T00:00:00+08:00"
---

# 示例

```shell
# 下载镜像
docker pull centos:8

# 创建容器并运行
docker run -it -d --restart=always --privileged --dns=223.5.5.5 --name=cto centos:8 /usr/sbin/init 

# 挂载文件
```

