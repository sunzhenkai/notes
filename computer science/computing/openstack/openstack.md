---
title: openstack
categories: 
  - [computer science, computing, openstack]
tags:
  - openstack
date: "2021-08-29T00:00:00+08:00"
update: "2021-08-29T00:00:00+08:00"
---

# 安装

安装教程仅供个人学习用，请谨慎用于生产环境。对于 Ubuntu 安装 openstack，推荐按照[官网指引](https://docs.openstack.org/install-guide/)操作，[这里](https://www.server-world.info/en/note?os=Ubuntu_20.04&p=openstack_wallaby&f=1) 是一个不错的辅助。

## 环境检查

打开[安装指引](https://docs.openstack.org/install-guide/)，在 [Environment](https://docs.openstack.org/install-guide/environment.html#) 章节下方，有 [OpenStack packages](https://docs.openstack.org/install-guide/environment-packages.html) 连接，在下方有不同 linux 发行版的 package 说明，比如 [centos](https://docs.openstack.org/install-guide/environment-packages-rdo.html)，里面有对发行版版本的要求说明，[这里](https://releases.openstack.org/index.html) 有所有的 openstack 版本。比如，centos 7  只能安装 Ussuri 之前的版本，即 Train 及之前。

此外其他配置也要进行，比如 mariadb、rabbitmq、memcached、etcd。

## 环境准备

以 centos 7 + openstack train 为例。[这里](https://releases.openstack.org/train/index.html) 是 train 的发布页，[这里](https://docs.openstack.org/install-guide/openstack-services.html) 是安装引导页面，里面有 train 的安装指引连接 [Minimal deployment for Train](https://docs.openstack.org/install-guide/openstack-services.html#minimal-deployment-for-train)，以最小安装为例，先安装 [Identity Service](https://docs.openstack.org/keystone/train/install/) 服务，点击去之后会有常用发行版的安装教程，点击 centos 的 [Install and configure](https://docs.openstack.org/keystone/stein/install/keystone-install-rdo.html)，在上方会有 note，提示先进行 [Openstack Install Guide](https://docs.openstack.org/install-guide/environment-packages-rdo.html#finalize-the-installation) 的先决条件安装步骤。

```shell
# 不要忘了安装 openstack client
$ yum install python-openstackclient

# 使用 pip 安装 openstack client
$ yum install python-devel python-pip
$ pip install python-openstackclient
```

## 安装仓库

如果我们直接使用命令安装，会报错。

```shell
$ yum install openstack-keystone -y
Loaded plugins: fastestmirror, langpacks
Loading mirror speeds from cached hostfile
 * base: mirrors.bupt.edu.cn
 * epel: mirrors.bfsu.edu.cn
 * extras: mirrors.bupt.edu.cn
 * updates: mirrors.bupt.edu.cn
No package openstack-keystone available.
Error: Nothing to do
```

搜下仓库。

```shell
$ yum search openstack
Loaded plugins: fastestmirror, langpacks
Loading mirror speeds from cached hostfile
 * base: mirrors.bupt.edu.cn
 * epel: mirrors.tuna.tsinghua.edu.cn
 * extras: mirrors.bupt.edu.cn
 * updates: mirrors.bupt.edu.cn
============================================ N/S matched: openstack ============================================
ansible-openstack-modules.noarch : Unofficial Ansible modules for managing Openstack
centos-release-openstack-queens.noarch : OpenStack from the CentOS Cloud SIG repo configs
centos-release-openstack-rocky.noarch : OpenStack from the CentOS Cloud SIG repo configs
centos-release-openstack-stein.noarch : OpenStack from the CentOS Cloud SIG repo configs
centos-release-openstack-train.noarch : OpenStack from the CentOS Cloud SIG repo configs
diskimage-builder.noarch : Image building tools for OpenStack
golang-github-rackspace-gophercloud-devel.noarch : The Go SDK for Openstack http://gophercloud.io
php-opencloud.noarch : PHP SDK for OpenStack/Rackspace APIs
php-opencloud-doc.noarch : Documentation for PHP SDK for OpenStack/Rackspace APIs
python2-oslo-sphinx.noarch : OpenStack Sphinx Extensions and Theme for Python 2

  Name and summary matches only, use "search all" for everything.
```

我们安装 train 对应的 noarch。

```shell
$ yum install centos-release-openstack-train.noarch
```

继续下面的流程。

## 安装 keystone

```shell
# 先创建用户 keystone
$ useradd -g keystone keystone

# 安装 glance 之前，创建 domain、project
# 创建 domain
$ openstack domain create --description "Default Domain" default
# 创建 project
$ openstack project create --domain default --description "Service Project" service
```

按教程安装到最后，会有如下内容。

```shell
export OS_USERNAME=admin
export OS_PASSWORD=ADMIN_PASS
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://controller:5000/v3
export OS_IDENTITY_API_VERSION=3
```

修改 `ADMIN_PASS` 之后，保存到文件 `admin-openrc`，后面会用到。

安装指引有创建 domain、project、user、role 的教程，后续安装尽量不要使用新创建的项目，使用默认即可。

| 项目               | 值      |
| ------------------ | ------- |
| domain / domain_id | default |
| domain_name        | Default |
| project            | service |

## 安装 glance

```shell
 # 第二步有个 source admin-openrc，即为安装 keystone 时最后给出的内容
```

## 安装 placement

### 验证

验证时如果出现 `Expecting value： line 1 column 1 (char 0)` ，可以参考[这篇文章](https://www.jianshu.com/p/50e5bacc43dd)。

## 安装 horizon

如果访问 `http://controller/dashboard` 提示 404，在配置 local_settings 时添加如下内容。

```python
WEBROOT = '/dashboard'
```

# 创建实例

## 先决条件

- 创建镜像
- 创建实例类型
- 创建网络
  - 选 vxlan

# LVM

对磁盘创建 lvm。

```shell
# 创建
$ pvcreate /dev/sda
$ vgcreate cinder-volumes /dev/sda

# 删除
## 移除卷
$ lvremove cinder--volumes-cinder--volumes--pool_tmeta
## 删除组
$ vgremove cinder-volumes
## 删除物理卷
$ pvremove /dev/sda
```

如果出现 `pvcreate` 时出现 `execlude by a filter`，检查 `/etc/lvm/lvm.conf ` 下的 `filters`。

```shell
filter = [ "a/sda/", "a/nvme/", "r/.*/" ]
```

如果想要接受一个块设备，使用类似下面的配置。

```shell
"a|.*|"
```

如果想要拒绝一个块设备，使用类似下面的配置。

```shell
"r|/dev/cdrom|"
```

# Ubuntu 安装

参考[安装指南](https://docs.openstack.org/install-guide/)，下面是在单机安装，IP 为 `192.168.6.55`。

## 版本信息

| 软件/系统 | 版本     |
| --------- | -------- |
| Ubuntu    | 22.04.2  |
| Openstack | antelope |

## **安装依赖**

```shell
# apt install apache2 libapache2-mod-uwsgi tgt 
```

## 环境配置

## Hosts

```shell
# vim /etc/hosts
## 添加如下内容, 注意替换 ip
192.168.6.55 controller
```

### 安装仓库

参考[这里](https://docs.openstack.org/install-guide/environment-packages-ubuntu.html)，选择一个版本即可，比如。

```shell
# add-apt-repository cloud-archive:antelope
# apt install nova-compute
# apt install python3-openstackclient
```

### SQL Database

```shell
# apt install mariadb-server python3-pymysql
```

**配置**

```shell
# vim /etc/mysql/mariadb.conf.d/99-openstack.cnf
## 添加如下内容
[mysqld]
bind-address = 192.168.6.55

default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
```

> bind-address 为 Controller Node 的 ip

**重启服务**

```shell
# service mysql restart
```

**初始化 mariadb**

```shell
# mysql_secure_installation
```

## Message Queue

> **注意**
>
> - 替换掉命令中的 RABBIT_PASS

```shell
# apt install rabbitmq-server
# rabbitmqctl add_user openstack RABBIT_PASS
# rabbitmqctl set_permissions openstack ".*" ".*" ".*"
```

## Memcached

```shell
# apt install memcached python3-memcache
# vim /etc/memcached.conf
## 将 -l 127.0.0.1 替换为 Controller 的 ip
-l 192.168.6.55
```

## Etcd

```shell
# apt install etcd
# vim /etc/default/etcd
## 参考如下内容修改
ETCD_NAME="controller"
ETCD_DATA_DIR="/var/lib/etcd"
ETCD_INITIAL_CLUSTER_STATE="new"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster-01"
ETCD_INITIAL_CLUSTER="controller=http://192.168.6.55:2380"
ETCD_INITIAL_ADVERTISE_PEER_URLS="http://192.168.6.55:2380"
ETCD_ADVERTISE_CLIENT_URLS="http://192.168.6.55:2379"
ETCD_LISTEN_PEER_URLS="http://0.0.0.0:2380"
ETCD_LISTEN_CLIENT_URLS="http://192.168.6.55:2379"
# systemctl enable etcd
# systemctl restart etcd
```

## 安装 Openstack 服务

参考[这里](https://docs.openstack.org/install-guide/openstack-services.html#minimal-deployment-for-yoga)，我们选择最小部署。

### Identity service

```shell
# mysql
MariaDB [(none)]> CREATE DATABASE keystone;
## 注意替换掉下面的 KEYSTONE_DBPASS
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' \
IDENTIFIED BY 'KEYSTONE_DBPASS';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' \
IDENTIFIED BY 'KEYSTONE_DBPASS';
MariaDB [(none)]> exit

# apt install keystone
# vim /etc/keystone/keystone.conf
## 修改如下内容, 注意替换 KEYSTONE_DBPASS
[database]
# ...
connection = mysql+pymysql://keystone:KEYSTONE_DBPASS@controller/keystone
[token]
# ...
provider = fernet

# su -s /bin/sh -c "keystone-manage db_sync" keystone
# keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
# keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
# keystone-manage bootstrap --bootstrap-password ADMIN_PASS \
  --bootstrap-admin-url http://controller:5000/v3/ \
  --bootstrap-internal-url http://controller:5000/v3/ \
  --bootstrap-public-url http://controller:5000/v3/ \
  --bootstrap-region-id RegionOne
# vim /etc/apache2/apache2.conf
## 添加如下内容
ServerName controller

## 环境变量中添加如下内容
$ export OS_USERNAME=admin, 注意替换 ADMIN_PASS
$ export OS_PASSWORD=ADMIN_PASS
$ export OS_PROJECT_NAME=admin
$ export OS_USER_DOMAIN_NAME=Default
$ export OS_PROJECT_DOMAIN_NAME=Default
$ export OS_AUTH_URL=http://controller:5000/v3
$ export OS_IDENTITY_API_VERSION=3
```

### Glance

```shell
# mysql
## 注意修改 GLANCE_DBPASS
MariaDB [(none)]> CREATE DATABASE glance;
MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' \
  IDENTIFIED BY 'GLANCE_DBPASS';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' \
  IDENTIFIED BY 'GLANCE_DBPASS';
MariaDB [(none)]> exit
## 注意保持上面设置的环境变量
$ openstack user create --domain default --password-prompt glance
$ openstack role add --project service --user glance admin
$ openstack service create --name glance \
  --description "OpenStack Image" image
$ openstack endpoint create --region RegionOne \
  image public http://controller:9292
# apt install glance
```

### Placement

### Compute

> **注意**
>
> - `nova.conf` 中 `auth_url` 填写 `http://controller:5000/v3`

### Networking

### Dashboard

### Block Storage

## 其他配置

#### **tgt 配置**

```shell
$ vim /etc/tgt/targets.conf
# 添加如下内容
include /var/lib/cinder/volumes/*
```

