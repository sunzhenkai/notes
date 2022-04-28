---
title: linux problems
categories: 
	- [linux,notes]
tags:
	- Linux
date: 2021/12/01 00:00:00
update: 2021/12/01 00:00:00
---

[toc]

# 挂载磁盘导致无法进入系统

拔出新加的磁盘，修改 `/etc/fstab` ，使用 UUID 区分盘符，示例如下。

# 使用 sudo 命令反应慢

- `/etc/hosts` 中没有 hostname 的记录，在 `/etc/hosts` 中添加 `127.0.0.1 <hostname>`

# ssh key 免密登录失败

**生成公钥和密钥**

```shell
ssh-keygen -t ras -C your@email.com

# ~/.ssh/id_rsa & ~/.ssh/id_rsa.pub
```

**配置**

将生成的 `~/.ssh/id_rsa.pub` 内容附加到需要登录机器的 `~/.ssh/authorized_keys` 文件后面。

**登录**

```shell
ssh remote-host
```

**登录失败**

```shell
# Permission denied (publickey).
## 查看远程机器文件权限
chmod 700 /home/$OS_USER/.ssh
chmod 600 /home/$OS_USER/.ssh/authorized_keys
chmod 600 /home/$OS_USER/.ssh/config
chmod 600 /home/$OS_USER/.ssh/id_rsa
```

# 设置语言和地区

在 `~/.bash_profile` 或 `~/.zshrc` 中添加如下内容，具体文件视使用的 shell 而定。

```shell
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
```
