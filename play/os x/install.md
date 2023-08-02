---
title: os x
categories: 
  - [play, os x]
tags:
  - os x
date: 2020/12/17 00:00:00
update: 2020/12/17 00:00:00
---

# 分区

```shell
$ diskutil partitionDisk disk4 GPT fat32 Linux 10% ExFat d2 10% ExFat d3 80%
# 对 disk4 进行分区，GPT格式
# 三个分区：
# 	Linux (fat32格式，10%空间)
# 	d2 (ExFat格式，10%空间)
#   d3 (ExFat格式，80%空间)
```

# Write Bootable ISO

目标磁盘尽量格式化为 `Mac OS Extended (Journaled)`，通过 `ls /Volumns` 查看目标磁盘。

## Mac OS

**Big Sur**

```shell
$ sudo /Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia --volume /Volumes/Big\ Sur --nointeraction # "/Volumes/Big\ Sur" 需要定制
# output
Erasing disk: 0%... 10%... 20%... 30%... 100%
Copying to disk: 0%... 10%... 20%... 30%... 100%
Making disk bootable...
Install media now available at "/Volumes/Install macOS Big Sur"

# 如果不显示进度，尝试重启终端 / 在 Disk Utility 中重新挂在卷
```

**Catalina**

```shell
$ sudo /Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia --volume /Volumes/Catalina --nointeraction
```

**参考**

- [Apple](https://support.apple.com/en-us/HT201372)

## Windows

```shell
# 注: 暂时废弃

#### 1. Convert ISO to DMG
$ hdiutil convert -format UDRW -o cn_windows_10_business_editions_version_2004_updated_sep_2020_x64_dvd_7134ba4b.img cn_windows_10_business_editions_version_2004_updated_sep_2020_x64_dvd_7134ba4b.iso
# output 64_dvd_7134ba4b.iso
Reading CPBA_X64FRE_ZH-CN_DV9            (Apple_UDF : 0)…
..............................................................................................................................................................................................
Elapsed Time: 12.059s
Speed: 420.2Mbytes/sec
Savings: 0.0%
created: /Users/wii/Downloads/cn_windows_10_business_editions_version_2004_updated_sep_2020_x64_dvd_7134ba4b.img.dmg

#### 2. Rename
$ mv cn_windows_10_business_editions_version_2004_updated_sep_2020_x64_dvd_7134ba4b.img.dmg cn_windows_10_business_editions_version_2004_updated_sep_2020_x64_dvd_7134ba4b.img

#### 3. 写入
$ sudo dd if=cn_windows_10_business_editions_version_2004_updated_sep_2020_x64_dvd_7134ba4b.img of=/dev/rdisk2s5 bs=1m
```

