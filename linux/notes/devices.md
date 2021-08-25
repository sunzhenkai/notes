---
title: Linux之查看设备
categories: 
	- [linux,notes]
tags:
	- Linux
date: 2020/12/05 18:40:00
update: 2020/12/05 18:40:00
---

# CPU

```shell
$ lscpu
```

# PCI 设备

```shell
$ lspci
```

# 块设备信息

```shell
$ lsblk
```

**参数**

- `-f` 显示文件系统信息
- `-a` 显示所有设备

# 硬盘

## 列出设备及分区信息

```shell
$ sudo parted -l
```

## 格式化

```shell
$ mkfs [options] [-t type fs-options] device [size]
```

**示例**

```shell
$ sudo mkfs -t ext4 /dev/sda
```

**类型**

- ext4
- FAT32
- NTFS

## 创建分区表

### 打开存储盘

```shell
$ sudo parted /dev/sda
GNU Parted 3.1
Using /dev/sda
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) select /dev/sdb       # 切换至 /dev/sdb
Using /dev/sdb
```

### 创建分区表

```shell
(parted) mklabel [partition_table_type]
```

**分区表类型**

- aix
- amiga
- bsd
- dvh
- gpt
- mac
- ms-dos
- pc98
- sun
- loop

**示例**

```shell
(parted) mklabel gpt
```

### 检查

```shell
(parted) print
```

### 创建分区表

```shell
(parted) mkpart primary [start] [end]
```

**示例**

```shell
(parted) mkpart primary 0.00B 100GB   # 按容量 
(parted) mkpart primary 0 100%        # 按比例
```

## 格式化分区表

```shell
$ sudo mkfs.ext4 /dev/sda1
```

## 自动挂载分区表

```shell
$ sudo mkdir data
$ sudo mount auto /dev/sda1 /data
```

### 示例

```shell
sudo parted /dev/sda
GNU Parted 3.1
Using /dev/sda
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print
Model: ATA Hitachi HUS72404 (scsi)
Disk /dev/sda: 4001GB
Sector size (logical/physical): 512B/4096B
Partition Table: loop
Disk Flags:

Number  Start  End     Size    File system  Flags
 1      0.00B  4001GB  4001GB  ext4

(parted) mklabel gpt
Warning: The existing disk label on /dev/sda will be destroyed and all data on this disk will be lost. Do you want to continue?
Yes/No? yes
(parted) print
Model: ATA Hitachi HUS72404 (scsi)
Disk /dev/sda: 4001GB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start  End  Size  File system  Name  Flags
(parted) mkpart primary 4096s 100%       # 创建分区表
(parted) print
Model: ATA Hitachi HUS72404 (scsi)
Disk /dev/sda: 4001GB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name     Flags
 1      2097kB  4001GB  4001GB               primary
$ sudo mkfs.ext4 /dev/sda1
...
$ sudo mount -t auto /dev/sda1 /data
$ df -h
Filesystem               Size  Used Avail Use% Mounted on
devtmpfs                  32G     0   32G   0% /dev
tmpfs                     32G     0   32G   0% /dev/shm
tmpfs                     32G  2.0G   30G   7% /run
tmpfs                     32G     0   32G   0% /sys/fs/cgroup
/dev/mapper/centos-root   50G  4.2G   46G   9% /
/dev/nvme0n1p2          1014M  233M  782M  23% /boot
/dev/nvme0n1p1           200M   12M  189M   6% /boot/efi
/dev/mapper/centos-home  395G  332M  394G   1% /home
tmpfs                    6.3G   12K  6.3G   1% /run/user/42
tmpfs                    6.3G     0  6.3G   0% /run/user/1000
/dev/sda1                3.6T   89M  3.4T   1% /data
```

**注** 创建分区表时 `4096s` 的取值，可以参考 [这里](https://blog.51cto.com/402753795/1754636) 和 [这里](https://blog.51cto.com/xiaosu/1590212)。

# 参考

- https://phoenixnap.com/kb/linux-create-partition
- https://phoenixnap.com/kb/linux-format-disk
