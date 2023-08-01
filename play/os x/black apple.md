---
title: 黑苹果安装
categories: 
	- [play, os x]
tags:
	- os x
date: 2021/01/25 00:00:00
update: 2021/01/25 00:00:00
---

# 说明

不定期更新装黑苹果的流程和问题处理，提供两个具体的基于 **`OpenCore`** 的 `config.plist`。

# 流程

该流程基于 [OpenCore](https://github.com/acidanthera/OpenCorePkg)，使用 Mac OS，`config.plist` 主要参考 [这里](https://dortania.github.io/OpenCore-Install-Guide/prerequisites.html#prerequisites)，具体流程如下。

**下载镜像**

- 百度搜索 黑果小兵，找下最新的系统镜像

**制作启动盘**

- 如果无需制作多启动优盘，使用 [etcher](https://www.balena.io/etcher/) 写入即可
- 如果需要制作多启动优盘，需要使用命令，参考 [这里](https://support.apple.com/en-us/HT201372) 制作

**配置 OpenCore**

- [下载 OpenCore](https://github.com/acidanthera/OpenCorePkg/releases)，选最新 `OpenCore-*.*.*-RELEASE.zip` 
- 下载 OpenCore Configurator，提供一个地址，[点击访问](https://mackie100projects.altervista.org/opencore-configurator/)
- `TODO`

# 异常

## `whatevergreen: failed to route IsTypeCOnlySystem`

`whatevergreen` 报 `failed to route IsTypeCOnlySystem` 异常，如果是使用集显，需要调整 device-properties。

## DSDT_HPET.aml

Dell Optiplex 7050 使用 OpenCore 0.6.5 安装 Big Sur (11.1) 后，板载声卡无法识别，Lilu.kext + AppleALC.kext 换各种 layout-id 无解。后参考这篇[帖子](https://www.tonymacx86.com/threads/help-mojave-alc-255-dell.274856/)，需要 fix Comment-IRQ，如果使用 Clover 的话，在 ACPI 勾选 `FixHPET`、`FixIPIC` 、 `FixRTC` 、`FixTMR` 即可，使用 OpenCore 的话，略微麻烦。

**首先，获取机器的 DSDT.aml** ，参考[这篇文章](https://dortania.github.io/Getting-Started-With-ACPI/Manual/dump.html#from-opencore) ，我使用 UEFI Shell 方式，需要下载 [acpidump.efi](https://github.com/dortania/OpenCore-Install-Guide/tree/master/extra-files/acpidump.efi.zip) ，和 OpenShell.efi（在下载的 OpenCore 中） 一并放入 `/EFI/OC/Tools` 下面，并在 config.plist 的 `Misc -> Tools` 下面启用，具体参考文章。重启，在引导界面进入 Open Shell，输入如下命令。

```shell
shell> fs0: // 替换为实际分区，进入OpenShell后会有分区提示
fs0:\> dir  // 查看分区文件，确认选的分区是否正确
   Directory of fs0:\
   01/01/01 3:30p EFI
fs0:\> cd EFI\OC\Tools   
fs0:\EFI\OC\Tools> acpidump.efi -b -n DSDT -z  
```

运行完上面命令后，会在EFI分区生成多个 `*.dat` 文件，我们把 `dsdt.dat` 拿出来，重命名为 `DSDT.aml`。

**然后，使用工具生成 `SSDT-HPET.aml` 文件**。下载工具 [SSDTTime](https://github.com/corpnewt/SSDTTime)，双击 [SSDTTime.command](https://github.com/corpnewt/SSDTTime/blob/master/SSDTTime.command) 运行，选择 `FixHPET    - Patch Out IRQ Conflicts` ，把生成好的 `DSDT.aml` 拖入终端，按照提示操作，最后会生成四个文件。

```
patches_Clover.plist
patches_OC.plist
SSDT-HPET.aml
SSDT-HPET.dsl
```

**接下来，需要做的是拷贝文件和Patch**，把 SSDT-HPET.aml 拷贝至 `EFI/OC/ACPI` 文件夹下，并用 OpenCore Configurator 打开 `patches_OC.plist`，把 ACPI 项内的数据复制至我们自己的 config.plist 中。

至此，大功告成。可解决 ALC255/ALC3243 声卡无法识别问题。