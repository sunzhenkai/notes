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
  expire: False
```

```shell
#cloud-config
groups:
  - ubuntu: [root,sys]
  - cloud-users
users:
  - default
  - name: ubuntu
    gecos: ubuntu
    sudo: ALL=(ALL) NOPASSWD:ALL
    primary_group: ubuntu
    groups: users
    lock_passwd: false
    # ubuntu
    hashed_passwd: $6$rounds=4096$F/colBvEPXvBa$cz4/dBg7R/jGVVPoAzQi/vydQ3H3h.iXIVDJrXczbDfXy/nGIHyaFA14Ee7e0pSJfWJNMlJGvwo4Kpi6NXFf00
```

使用如下命令生成加密密码。

```shell
# mkpasswd --method=SHA-512 --rounds=4096
Password:
$6$rounds=4096$F/colBvEPXvBa$cz4/dBg7R/jGVVPoAzQi/vydQ3H3h.iXIVDJrXczbDfXy/nGIHyaFA14Ee7e0pSJfWJNMlJGvwo4Kpi6NXFf00
```

