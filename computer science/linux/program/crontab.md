---
title: linux - crontab
categories:
  - [linux, software]
tags:
  - linux
    - crontab
date: 2022/06/22 00:00:00
update: 2022/06/22 00:00:00
---

# 命令格式

```shell
MIN HOUR DOM MON DOW CMD
# DOM: day of month
# DOW: day of week
```

# 查看

```shell
$ crontab -l
```

# 编辑

```shell
$ crontab -e
```

# 启动时运行

```shell
@reboot /home/ubuntu/app/consul/start.sh
```

# 时间格式

```shell
MIN HOUR DOM MON DOW CMD
 *   *    *   *   *   ...
 
# 特殊符号
*	任意值
,	多值分隔符
-	范围分隔符
/	间隔符 (step values)

# 示例
* * * * *       每分钟
30 08 10 06 *   每年的 6 月 10 号 8 点 30 分
30 * * * *      每小时的 30 分
00 11,16 * * *  每天的 11:00 和 16:00
00 09-18 * * *  每天的 9、10 ... 18 点 00 分
00 09-18 * * 1-5 周一至周五每天的 9、10 ... 18 点 00 分
*/10 * * * *    每十分钟
```

# 设置 PATH

```shell
$ crontab -e # 开头添加如下内容
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/home/ubuntu/.local/bin
```

