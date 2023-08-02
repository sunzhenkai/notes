---
title: ubuntu setup
categories: 
  - [linux,distro,ubuntu]
tags:
  - distro
date: 2022/08/28 00:00:00
---

# 设置时区

**timedatectl**

```shell
# 查看当前时区信息
$ timedatectl
               Local time: 一 2023-06-26 16:21:01 CST
           Universal time: 一 2023-06-26 08:21:01 UTC
                 RTC time: 一 2023-06-26 08:21:01
                Time zone: Asia/Shanghai (CST, +0800)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
# 查看所有可配置的时区名称
$ timedatectl list-timezones
Africa/Abidjan
Africa/Accra
Africa/Addis_Ababa
Africa/Algiers
Africa/Asmara
Africa/Asmera
Africa/Bamako
Africa/Bangui
Africa/Banjul
Africa/Bissau
...
# 设置时区
$ sudo timedatectl set-timezone Asia/Shanghai
```

**tzselect**

临时需改时区，重启后失效。

```shell
$ tzselect
```

