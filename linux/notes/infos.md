---
title: Linux之查看系统信息
categories: 
	- [linux,notes]
tags:
	- Linux
date: 2020/12/05 18:40:00
update: 2020/12/05 18:40:00
---

# 查看版本信息

## 发行版名称及信息

```shell
# lsb_release
$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04.5 LTS
Release:	18.04
Codename:	bionic

# os-release
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="18.04.5 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.5 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic

# hostnamectl
$ hostnamectl
   Static hostname: mvm
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 2d1d6a0bc90a451ab6ed062e9c2153bf
           Boot ID: d8d4f12a272847b0b7d1de1ec2307493
    Virtualization: qemu
  Operating System: Ubuntu 18.04.5 LTS
            Kernel: Linux 4.15.0-126-generic
      Architecture: x86-64
      
# issue
$ cat /etc/issue
Ubuntu 18.04.5 LTS \n \l
```

## 内核版本

```shell
# uname
$ uname -r  # OR -a
4.15.0-126-generic
```

