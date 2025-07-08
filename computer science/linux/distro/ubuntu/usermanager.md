---
title: ubuntu user manager
categories: 
  - [linux,distro,ubuntu]
tags:
  - distro
date: "2021-09-29T00:00:00+08:00"
update: "2021-09-29T00:00:00+08:00"
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
NEW_USER=wii
sudo groupadd $NEW_USER
sudo useradd -d /data/$NEW_USER -m -s /bin/bash -g $NEW_USER $NEW_USER
sudo usermod -aG sudo $NEW_USER
sudo passwd $NEW_USER
```

