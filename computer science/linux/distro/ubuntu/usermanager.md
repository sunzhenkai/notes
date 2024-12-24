---
title: ubuntu user manager
categories: 
  - [linux,distro,ubuntu]
tags:
  - distro
date: 2021/09/29 00:00:00
update: 2021/09/29 00:00:00
---

```shell
# 添加 group
$ groupadd {groupname}

# 添加用户
$ useradd -d /home/{username} -m -s /bin/bash -g {username} {groupname}

# 添加 sudo
$ sudo usermod -aG sudo {username}

# 设置密码
$ sudo passwd {username}
```

```shell
groupadd wii
useradd -d /home/wii -m -s /bin/bash -g wii wii
sudo usermod -aG sudo wii
sudo passwd wii
```

