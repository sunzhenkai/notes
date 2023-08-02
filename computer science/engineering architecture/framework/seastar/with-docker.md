---
title: seastar with docker
categories: 
  - [架构,框架,seastar]
tags:
  - seastar
date: 2022/03/11 00:00:00
update: 2022/03/11 00:00:00
---

# 创建容器

```shell
docker run ... --sysctl net.core.somaxconn=10240 ...
```

# 设置

```shell
# 临时修改 aio-max-nr
# 注意 image-name 是镜像的名称，不是 container 的名称
docker run --privileged <image-name> sh -c 'echo 1048576 > /proc/sys/fs/aio-max-nr'

# 或者
docker run --privileged -it zhenkai.sun/external-with-openssh bash
sysctl -w fs.aio-max-nr=1048576

# 验证
cat /proc/sys/fs/aio-max-nr
cat /proc/sys/net/core/somaxconn

docker run --privileged --sysctl net.core.somaxconn=10240 zhenkai.sun/external-with-openssh bash
```

