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

# df 磁盘用满但 du 显示还有空间

```shell
#lsof | grep delete
COMMAND     PID   TID           USER   FD      TYPE             DEVICE     SIZE/OFF       NODE NAME
intercept 14265                 root    3u      REG              259,1 227432595897   54608901 /data/intercept/access.log (deleted)
```

`/data/intercept/access.log` 日志占用 210G 容量，但是已经被删除。

# 使用不同网关导致配合端口转发失效

- [这里](https://unix.stackexchange.com/questions/664757/port-forwarding-does-not-work-using-different-gateway)

# Shell 登录慢

```shell
# 调试
$ bash --login --verbose
...
export PS1="[\u@${Green}\H${ENDCOLOR}:${Brown}$(ips)${ENDCOLOR} \W]\\$" # 在这个位置卡很久

# 原因
## ips 命令卡住的可能性比较大, 手动执行 ips
## 果然会卡住

$ which ips
ips ()
{
    curl -s http://169.254.169.254/latest/meta-data/public-ipv4
}

# 用的阿里云机器, 修改为下面的命令
$ sudo vim /etc/profile
# 修改 function ips() ... 为如下
function ips() {
    GET http://100.100.100.200/latest/meta-data/eipv4
}
```

