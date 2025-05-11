---
title: pve - usage
categories: 
  - [play,pve]
tags:
  - samb
date: "2022-08-21T00:00:00+08:00"
---

# 直通

## 硬盘直通

```shell
# sata 硬盘直通
qm set {vm-id} -sata0 /dev/disk/by-id/{disk-id}
# 示例
qm set 105 -sata0 /dev/disk/by-id/ata-HS-SSD-A260_1024G_30066931838
```

