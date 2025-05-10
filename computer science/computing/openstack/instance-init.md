---
title: instance init
categories: 
  - [computer science, computing, instance]
tags:
  - openstack
date: "2022-06-02T00:00:00+08:00"
update: "2022-06-02T00:00:00+08:00"
---

# 挂载卷

```shell
# 创建文件系统
$ sudo mkfs -t ext4 /dev/vdb
# 分区
$ sudo parted -a optimal /dev/vdb 
(parted) mklabel gpt
(parted) mkpart primary 0% 100%
# 格式化
$ sudo mkfs.ext4 /dev/vdb1
# 挂载
$ sudo mkdir /data
$ sudo mount -t auto /dev/vdb1 /data
```

