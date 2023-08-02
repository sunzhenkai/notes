---
title: ubuntu - vnc
categories: 
  - [linux,distro,ubuntu]
tags:
  - distro
date: 2021/09/29 00:00:00
update: 2021/09/29 00:00:00
---

# 安装 Desktop

```shell
sudo apt update && sudo apt upgrade 
sudo apt install tasksel -y 
sudo tasksel	# 选择安装 ubuntu-desktop
sudo systemctl set-default graphical.target 
# 重启电脑
sudo reboot
```

# 安装 TigerVNCServer

```shell
sudo apt install tigervnc-standalone-server tigervnc-common

# 设置 vnc 密码
vncpasswd

# 设置 vnc server
sudo vi  ~/.vnc/xstartup
# 内容如下
#!/bin/sh
xrdb $HOME/.Xresources
vncconfig -iconic &
dbus-launch --exit-with-session gnome-session &

# 启动 vnc server
vncserver -localhost no
```

**操作**

```shell
# 列出启动的 session
vncserver -list 

# kill session
vncserver -kill :<session-no>  # 比如 :2
```

# 参考

- https://techviewleo.com/install-and-configure-vnc-server-on-ubuntu/