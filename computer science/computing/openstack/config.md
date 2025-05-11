---
title: openstack config
categories: 
  - [computer science, computing, openstack]
tags:
  - openstack
date: "2021-10-29T00:00:00+08:00"
update: "2021-10-29T00:00:00+08:00"
---

# 模块

## 启停

```shell
# 命令
sudo service <service> restart

# nova-scheduler
sudo service nova-scheduler restart
```

## 状态

```shell
sudo systemctl status <service>
```

# 超分

```shell
sudo vim /etc/nova/nova.conf
```

