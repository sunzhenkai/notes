---
title: vncserver
categories: 
	- [linux,notes]
tags:
	- Linux
date: 2021/08/25 00:00:00
update: 2021/08/25 00:00:00
---

# centos

```shell
# 安装 vncserver
$ sudo yum install tigervnc-server

# 设置密码
$ vncpasswd

# 拷贝配置
$ sudo cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@:1.service

# 修改配置
$ sudo vim /etc/systemd/system/vncserver@\:1.service
```

**配置**

以用户 wii 为例，需要替换其中的内容。

```shell
[Unit]
Description=Remote desktop service (VNC)
After=syslog.target network.target

[Service]
Type=forking
ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'
ExecStart=/sbin/runuser -l wii -c "/usr/bin/vncserver %i -geometry 1280x1024"
PIDFile=/home/wii/.vnc/%H%i.pid
ExecStop=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'

[Install]
WantedBy=multi-user.target
```

**交由 systemctl 管理**

```shell
$ sudo systemctl daemon-reload         # 重新加载配置
$ sudo systemctl start vncserver@:1    # 启动 vnc server
$ sudo systemctl status vncserver@:1   # 查看状态
$ sudo systemctl enable vncserver@:1   # 开启自启动
```

## 参考

- https://www.tecmint.com/install-and-configure-vnc-server-in-centos-7/
- https://www.tecmint.com/install-tightvnc-remote-desktop/