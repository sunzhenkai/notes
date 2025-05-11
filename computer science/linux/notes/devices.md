---
title: Linux之查看设备
categories: 
  - [linux,notes]
tags:
  - Linux
date: "2020-12-05T18:40:00+08:00"
update: "2020-12-05T18:40:00+08:00"
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

# 查看挂载的节点和对应的分区 UUID
$ ls -lha /dev/disk/by-uuid

# 查看块设备的信息，包含 UUID
$ blkid /dev/sda1
```

**参数**

- `-f` 显示文件系统信息
- `-a` 显示所有设备

# 硬盘

## 初始化步骤

- 创建分区表
- 创建分区
- 格式化分区
- 挂载分区
- 配置启动时挂载

## 列出设备及分区信息

```shell
$ parted -l
# 或
$ fdisk -l
```

## 初始化设备

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

**使用中无法格式化**

```shell
$ dmsetup status
$ dmsetup remove <>
$ dmsetup remove_all # 清楚所有, 谨慎使用, 最好挨个删除
```

## 创建主分区

### 打开存储盘

```shell
$ sudo parted -a optimal /dev/sda
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

### 创建分区

```shell
# 主分区
(parted) print free
(parted) mkpart primary [start] [end]  # 主分区模式

# lvm 分区
(parted) unit s
(parted) mkpart LVM ext4 0% 100%
```

**示例**

```shell
(parted) mkpart primary 0.00B 100GB   # 按容量 
(parted) mkpart primary 0 100%        # 按比例
```

### 格式化分区

```shell
$ sudo mkfs.ext4 /dev/sda1
```

### 自动挂载分区

```shell
$ sudo mkdir data
$ sudo mount -t auto /dev/sda1 /data
```

### 示例

```shell
$ sudo parted /dev/sda
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

### 脚本创建分区 & 格式化

```shell
# 分区
parted --script /dev/vdb \
	mklabel gpt \
	mkpart primary 4096s 100% 
	
# 格式化
mkfs.ext4 /dev/vdb1

# 挂载
mount -t auto /dev/vdb1 /data

# 写入 /etc/fstab, root 用户运行
echo -e "UUID=$(blkid -o value -s UUID /dev/vdb1)\t/data\text4\tdefaults\t0 0" >> /etc/fstab


echo -e "UUID=$(blkid -o value -s UUID /dev/sdb1)\t/downloads\text4\tdefaults\t0 0" >> /etc/fstab
```

## 创建 LVM 分区

### 概念

- 物理卷（Physical Volumes）
- 卷组（Volume Groups）
- 逻辑卷（Logical Volumes）

### 查看信息

**查看所有 LVM 可以管理的块设备**

```shell
sudo lvmdiskscan
```

**查看物理卷信息**

```shell
sudo lvmdiskscan -l
# 或
sudo pvscan

# 如果需要展示更多信息
sudo pvs
# 或
sudo pvdisplay
sudo pvdisplay -m # 查看映射到每个卷的逻辑扩展名
```

**查看 Volumn Group 的信息**

```shell
sudo vgscan
```

**查看 Logical Volumn 信息**

```shell
sudo lvscan
# 或
sudo lvs
```

### 创建 LVM 卷

**从 Raw Storage Device 创建 Physical Volumes**

```shell
# 列出所有可用的设备
sudo lvmdiskscan
```

如果没有列出目标设备，可能是设备使用了不支持的分区表。重新设置设备的分区表为兼容的 BIOS 表。

```shell
sudo parted /dev/sda
(parted) mktable msdos
(parted) quit
```

标记存储设备为 LVM 物理卷。

```shell
sudo pvcreate /dev/sda
# 多个设备
sudo pvcreate /dev/sda /dev/sdb 
```

**从 Physical Volumes 创建 Volume Group**

```shell
sudo vgcreate lvm-storage /dev/sda
# 多个设备
sudo vgcreate lvm-storage /dev/sda /dev/sdb 
```

**从 Volume Group 创建 Logical Volume**

```shell
# 创建指定 size
sudo lvcreate -L 500G -n lvm-storage-hadoop lvm-storage

# 使用所有剩余空间
sudo lvcreate -l 100%FREE -n lvm-storage-hadoop lvm-storage
```

**格式化分区**

```shell
sudo mkfs.ext4 /dev/<lvm-vg-name>/<lvm-lv-name> 
```

**挂载 LV**

```shell
sudo mount /dev/<lvm-vg-name>/<lvm-lv-name> /path/to/destination
```

**自动挂载**

```shell
# 查看 logical volume 的 uuid
sudo blkid
/dev/mapper/<lvm-lv-name>: UUID="0192e4be-db57-4dc9-9f07-cb7bd673811b" BLOCK_SIZE="4096" TYPE="ext4"
# 添加自动挂载
sudo vim /etc/fstab
# 新增如下内容
UUID=0192e4be-db57-4dc9-9f07-cb7bd673811b       /storage/hadoop    ext4    defaults        0       2
```

### 更多操作

#### 向 Volume Group 添加 Physical Volume

```shell
sudo vgextend <volume-group-name> /dev/sdb
```

#### 增加 Logical Volume 的空间

**Solution 1**

```shell
sudo lvresize -L +5G --resizefs <lvm-vg-name>/<lvm-lv-name>  # 调整 lvm size
sudo lvresize -l +100%FREE /dev/<lvm-vg-name>/<lvm-lv-name>  # 使用所有剩余空间
# sudo lvdisplay; 找到 Logical Volume 的 LV Path
sudo resize2fs <lv-path>	# 生效
```

> 注意: lvresize 之后通过 df -h 查看空间，并不会生效，需要再运行 resize2fs 

**Solution 2**

为 Ubuntu 的 lv 分区扩容

```shell
$ sudo vgdisplay  # 查看 vg 信息
$ sudo lvdisplay  # 查看 lv 信息
$ sudo lvextend -l +100%FREE -r /dev/ubuntu-vg/ubuntu-lv
```

#### 删除 Logical Volume 

```shell
sudo umount /dev/<lvm-vg-name>/<lvm-lv-name>
sudo lvremove <lvm-vg-name>/<lvm-lv-name>
```

#### 删除 Volume Group

```shell
sudo umount /dev/<lvm-vg-name>/* # unmount vg 下所有 lv
sudo vgremove <lvm-vg-name>
```

#### 删除 Physical Volume

```shell
sudo pvremove /dev/sda
```

# 查看接口

```shell
sudo dmidecode --type connector
# 可以查看 USB、SATA、M.2 接口
```

# 参考

- https://phoenixnap.com/kb/linux-create-partition
- https://phoenixnap.com/kb/linux-format-disk
- https://unix.stackexchange.com/questions/200582/scripteable-gpt-partitions-using-parted
