---
title: 安装 Arch Linux 
categories: 
  - [linux,distro,centos]
tags:
  - distro
date: "2021-09-04T00:00:00+08:00"
update: "2021-09-04T00:00:00+08:00"
---

# 创建并挂载分区

1. 查看硬盘

```shell
$ fdisk -l
```

2. 使用 fdisk 创建分区表

```shell
$ fdisk /dev/sda
(fdisk) p # 打印分区信息
(fdisk) g # 创建 GPT 分区表
```

2.1 创建分区

创建 /boot 分区

```shell
(fdisk) n  # 创建分区
(fdisk) Partition number...: # 回车
(fdisk) First section...:    # 回车
(fdisk) Last section...: +1G
```

创建 / 分区

```shell
(fdisk) n  # 创建分区
(fdisk) Partition number...: # 回车, 默认值
(fdisk) First section...:    # 回车
(fdisk) Last section...: 		 # 回车, 使用最大 section number
```

确认

```shell
(fdisk) p   # 重新打印分区，有新创建的两个分区
```

保存

```shell
(fdisk) w
```

3. 格式化分区

```shell
$ mkfs.fat -F32 /dev/sda1   # 格式化 /boot 分区（假设为 /dev/sda1）
$ mkfs.ext4 /dev/sda2       # 格式化 / 分区（假设为 /dev/sda2）
```

4. 挂载

```shell
$ mount /dev/sda2 /mnt       # 挂载根分区
$ mkdir /mnt/boot            # 创建 boot 挂载点
$ mount /dev/sda1 /mnt/boot  # 挂载 /boot 分区
```

# 安装

```shell
$ pacstrap -K /mnt base linux linux-firmware
```

# 配置

```shell
# fstab
$ genfstab -U /mnt >> /mnt/etc/fstab

# Chroot
$ arch-chroot /mnt

# Time
$ ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
$ hwclock --systohc

# root passwd
$ passwd

# 安装 vim
$ pacman -S vim

# Localization
$ vim /etc/locale.conf # 写入如下内容
LANG=en_US.UTF-8

# hostname
$ vim /etc/hostname
```

Boot loader

```shell
# GRUB
$ pacman -S grub efibootmgr
$ grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ArchLinux

## 配置 GRUB
$ grub-mkconfig -o /boot/grub/grub.cfg
```

重启

```shell
$ exit
```

