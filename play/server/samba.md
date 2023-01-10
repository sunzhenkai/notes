---
title: samba server
categories: 
	- [play,samb]
tags:
	- samb
date: 2022/08/21 00:00:00
---

# 安装

```shell
# ubuntu
sudo apt update
sudo apt install samba
```

# 配置

```shell
sudo vim /etc/samba/smb.conf
# 在文档最后添加
[sambashare]
    comment = Samba on Ubuntu
    path = /home/username/sambashare
    read only = no
    browsable = yes
```

# 重启服务

```shell
sudo service smbd restart
```

# 添加用户并设置密码

```shell
sudo smbpasswd -a <username>
```

