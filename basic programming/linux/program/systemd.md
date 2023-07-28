---
title: systemd使用
categories: 
	- [linux,software]
tags:
	- linux
	- systemd
date: 2020/11/13 22:30:00
update: 2020/11/13 22:30:00
---

# 添加服务

- 创建可执行服务程序
- 创建 Unit File
- 复制 Unit File 至 `/etc/systemd/system`
- 服务启 / 停

# 示例

```shell
# [required] 1. 创建可执行服务程序
## File: test_service.sh
DATE=`date '+%Y-%m-%d %H:%M:%S'`
echo "Example service started at ${DATE}" | systemd-cat -p info

while :
do
  echo "Looping...";
  sleep 30;
done

# [optional] 2. 复制程序至 /usr/bin
$ sudo cp test_service.sh /usr/bin/test_service.sh
$ sudo chmod +x /usr/bin/test_service.sh

# [required] 3. 创建 Unit File
## File: myservice.service
[Unit]
Description=Example systemd service.

[Service]
Type=simple
ExecStart=/bin/bash /usr/bin/test_service.sh

[Install]
WantedBy=multi-user.target

# [required] 4. 复制 Unit File 至 /etc/systemd/system
$ sudo cp myservice.service /etc/systemd/system/myservice.service
$ sudo chmod 644 /etc/systemd/system/myservice.service
```

# 服务启停

```shell
# 启动 
$ sudo systemctl start myservice

# 查看状态
$ sudo systemctl status myservice

# 停止
$ sudo systemctl stop myservice

# 重启
$ sudo systemctl restart myservice

# 开机启动
$ sudo systemctl enable myservice
```

