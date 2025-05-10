---
title: linux lvm
categories: 
  - [computer science, computing, storage]
tags:
  - openstack
date: "2021-11-02T00:00:00+08:00"
update: "2021-11-02T00:00:00+08:00"
---

# LVM

对磁盘创建 lvm。

```shell
# 创建
$ pvcreate /dev/sda
$ vgcreate cinder-volumes /dev/sda

# 删除
## 移除卷
$ lvremove cinder--volumes-cinder--volumes--pool_tmeta
## 删除组
$ vgremove cinder-volumes
## 删除物理卷
$ pvremove /dev/sda
```

如果出现 `pvcreate` 时出现 `execlude by a filter`，检查 `/etc/lvm/lvm.conf ` 下的 `filters`。

```shell
filter = [ "a/sda/", "a/nvme/", "r/.*/" ]
```

如果想要接受一个块设备，使用类似下面的配置。

```shell
"a|.*|"
```

如果想要拒绝一个块设备，使用类似下面的配置。

```shell
"r|/dev/cdrom|"
```