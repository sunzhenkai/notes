---
title: openstack
categories: 
	- [computer science, computing, openstack]
tags:
	- openstack
date: 2021/08/29 00:00:00
update: 2021/08/29 00:00:00
---

# 安装

安装教程仅供个人学习用，请谨慎用于生产环境。

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

### 创建网络

#### 网络类型

- local
- flat
- vlan
- vxlan
- gre
- geneve

# LVM

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

# Ubuntu 安装

**prepare**

```shell
$ apt install apache2 libapache2-mod-wsgi tgt
```

