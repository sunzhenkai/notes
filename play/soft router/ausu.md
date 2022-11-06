---
title: 华硕路由器
categories: 
	- [play,router]
tags:
	- router
date: 2022/10/16 00:00:00
---

# 通过域名解析内网机器

打开 **高级设置 / 内部网络**，修改路由器网络名称为 `host`。

> 这里选 host 是应为 host 是合法的定级域名，浏览器输入不添加协议头 (`http://` 等) 时不会调用搜索。

![image-20221106215611021](./ausu/image-20221106215611021.png)

**修改机器名称**

在下面的 **手动指定 IP 的 DHCP 列表** 中添加内网机器记录。

![image-20221106224817651](./ausu/image-20221106224817651.png)

**检查 Hosts**

```shell
$ ssh admin@192.168.6.1

$ cat /etc/hosts
127.0.0.1 localhost.localdomain localhost
192.168.6.1 RT-AX88U-BD78.host RT-AX88U-BD78
192.168.6.1 RT-AX88U-BD78.local
192.168.6.1 router.asus.com
192.168.6.1 www.asusnetwork.net
192.168.6.1 www.asusrouter.com
192.168.6.6 unraid.host
...
```

**浏览器访问**

![image-20221106220852396](./ausu/image-20221106220852396.png)