---
title: openstack images
categories: 
	- [computer science, computing, openstack]
tags:
	- openstack
date: 2021/09/02 00:00:00
update: 2021/09/02 00:00:00
---

# 镜像下载

[Openstack 官方镜像文档](https://docs.openstack.org/image-guide/obtain-images.html)。

## ubuntu

对于 ubuntu cloud 的初始化文档参考[这里](https://help.ubuntu.com/community/CloudInit)，对于 cloud init 参考[这里](https://cloud-init.io/) 还有[这里](https://cloudinit.readthedocs.io/en/latest/topics/examples.html)。

**配置账号密码**

```shell
#cloud-config
chpasswd:
  list: |
    ubuntu:ubuntu
    wii:wii
  expire: False
```

