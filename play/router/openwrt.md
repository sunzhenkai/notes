---
title: openwrt
categories: 
  - [play,soft router]
tags:
  - soft router
date: "2022-10-16T00:00:00+08:00"
---

# 开启 Samba

```shell
# 安装依赖
opkg install shadow-common shadow-useradd

# 添加用户
useradd share
smbpasswd -a share
```

# 扩容 overlay

**已验证的镜像类型**

```shell
openwrt-...-...-generic-squashfs-combined-efi.img
```

**扩容**

```shell
# 扩容镜像
dd if=/dev/zero bs=1G count=30 >> openwrt-22.03.2-x86-64-generic-squashfs-combined-efi.img
# 分区
$ parted openwrt-22.03.2-x86-64-generic-squashfs-combined-efi.img
...
(parted) print
...
Number  Start   End     Size    File system  Name  Flags
128     17.4kB  262kB   245kB                      bios_grub
 1      262kB   17.0MB  16.8MB  fat16              legacy_boot
 2      17.0MB  126MB   109MB

(parted) resizepart 2 100%
(parted) print
...
Number  Start   End     Size    File system  Name  Flags
128     17.4kB  262kB   245kB                      bios_grub
 1      262kB   17.0MB  16.8MB  fat16              legacy_boot
 2      17.0MB  32.3GB  32.3GB

(parted) quit

# [pve] 加载镜像为虚拟机磁盘
qm importdisk 103 openwrt-22.03.2-x86-64-generic-squashfs-combined-efi.img local-lvm
```

# 挂载新的磁盘

```shell
# 格式化磁盘
mkfs.ext4 /dev/sdb

# 安装 block-mount
opkg install block-mount

# 进入网页, 打开 系统 -> 挂载点
挂载点 -> 新增
保存并应用
```

# 预编译固件

- Immortal Wrt
- iStoreOs

# 配置

- [OpenClash 配置](https://www.youtube.com/watch?v=s84CWgKus4U&t=514s)
