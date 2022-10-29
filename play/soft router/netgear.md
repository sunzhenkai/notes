---
title: netgear
categories: 
	- [play,router]
tags:
	- router
date: 2022/10/16 00:00:00
---

# 回刷官方固件

```shell
1. 下载固件并解压
https://www.netgear.com/support/download/

2. 路由器恢复模式
 - 路由器关机
 - 按住 Reset
 - 开机
 - 等待一二十秒，电源灯白灯闪烁
 
3. 上传固件 
// 不同系统的命令稍有差异
$ tftp 192.168.1.1
tftp> binary
tftp> put R9000-V1.0.5.42.img

4. 等待刷新完成
```

