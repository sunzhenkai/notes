---
title: soft router
categories: 
	- [play,soft router]
tags:
	- soft router
date: 2022/10/16 00:00:00
---

# 镜像

- [lede](https://github.com/coolsnowwolf/lede)

# 主题

- https://github.com/jerrykuku/luci-theme-argon

# LEDE

## 更新源配置

**腾讯**

```shell
src/gz openwrt_core https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/targets/x86/64/packages
src/gz openwrt_base https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/packages/x86_64/base
src/gz openwrt_luci https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/packages/x86_64/luci
src/gz openwrt_packages https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/packages/x86_64/packages
src/gz openwrt_routing https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/packages/x86_64/routing
src/gz openwrt_telephony https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/telephony
```

**清华源**

```shell
src/gz openwrt_core https://mirrors.cloud.tencent.com/lede/snapshots/targets/x86/64/packages
src/gz openwrt_base https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/base
src/gz openwrt_helloworld https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/helloworld
src/gz openwrt_kenzo https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/kenzo
src/gz openwrt_luci https://mirrors.cloud.tencent.com/lede/releases/18.06.9/packages/x86_64/luci
src/gz openwrt_packages https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/packages
src/gz openwrt_routing https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/routing
src/gz openwrt_small https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/small
src/gz openwrt_telephony https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/telephony
```

# PVE

## 查看 debian 版本

```shell
# 1. 查看文件 release 文件
$ cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
NAME="Debian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"

# 2. 通过 lsb-release 命令
$ apt update
$ apt install lsb-release
$ lsb_release -a
No LSB modules are available.
Distributor ID:	Debian
Description:	Debian GNU/Linux 11 (bullseye)
Release:	11
Codename:	bullseye
```

## 修改 debian 更新源

参考[这里](https://mirrors.tuna.tsinghua.edu.cn/help/debian/)。

```shell
# 安装依赖
apt update
apt install apt-transport-https ca-certificates -y

# 修改源文件
$ mv /etc/apt/sources.list /etc/apt/sources.list.back
$ vi /etc/apt/sources.list
## 输入如下内容 (注意版本, 下面是 bullseye)
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
```

**更新**

```shell
apt update
apt upgrade -y
```

## 修改更新源

参考[这里](https://mirrors.tuna.tsinghua.edu.cn/help/proxmox/)。

**proxmox 更新**

```shell
# 添加源文件
vi /etc/apt/sources.list.d/pve-no-subscription.list
# 输入 (注意 debian 版本)
deb https://mirrors.tuna.tsinghua.edu.cn/proxmox/debian bullseye pve-no-subscription 
```

**CT 模板加速**

```shell
cp /usr/share/perl5/PVE/APLInfo.pm /usr/share/perl5/PVE/APLInfo.pm_back
sed -i 's|http://download.proxmox.com|https://mirrors.tuna.tsinghua.edu.cn/proxmox|g' /usr/share/perl5/PVE/APLInfo.pm
```

> 重启生效。

## 从 qcow2 启动 openwrt

**1. 拷贝镜像至 pve**

```shell
scp openwrt-x86-64-generic-squashfs-combined-efi.qcow2 root@192.168.6.60:
```

**2. 创建虚拟机**

不用添加硬盘盒配置 CD/DVD 驱动器。

**3. 挂载镜像为磁盘**

```shell
qm importdisk 100 openwrt-x86-64-generic-squashfs-combined-efi.qcow2 local-lvm
```

> 这里的 100 是虚拟机 ID
>
> local-lvm 是存储池名称

![image-20221105161004992](./soft-router/image-20221105161004992.png)

**4. 为虚拟机添加硬盘**

![image-20221105160819628](./soft-router/image-20221105160819628.png)

选中未使用的磁盘，并点击编辑。

![image-20221105160840881](./soft-router/image-20221105160840881.png)

类型选择 IDE。

**5. 修改引导**

![image-20221105161029736](./soft-router/image-20221105161029736.png)

![image-20221105161048645](./soft-router/image-20221105161048645.png)

启用新添加的硬盘，并把优先级设为最高（拖动序号前的三条横杠）。

**6. 启动虚拟机**

保存上述更改，启动虚拟机即可。

## 硬盘直通

```shell
$ vi /etc/default/grub
# 修改 GRUB_CMDLINE_LINUX_DEFAULT 为如下
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on"

# 更新 grub
$ update-grub
```

