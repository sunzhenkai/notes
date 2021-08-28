---
title: server
categories: 
	- [play,server]
tags:
	- server
date: 2021/08/24 00:00:00
update: 2021/08/24 00:00:00
---

# BIOS 配置

## 断电恢复后自启动

- 开机长按 `Delete` 进入 BIOS
- `InelRCSetup -> PCH Configuration -> PCH Devices -> Restore AC after Power Loss`
- 设置为 `Power On`

设置断电恢复后启动，目的是设置远程启动。

# 系统

Centos 7。

# 配置

```shell
# 关闭 selinux
$ sudo vim /etc/selinux/config
SELINUX=enforcing -> SELINUX=disabled
$ sudo setenforce 0

# 关闭 swap
$ sudo vim /etc/fstab
注释掉行 /dev/mapper/centos-swap

# 关闭防火墙
$ systemctl stop firewalld
$ systemctl disable firewalld
```

# 程序

## 必备

```shell
sudo yum install git telnet -y
```

## zsh

```shell
$ sudo yum install zsh
# on my zsh
$ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

## docker

```shell
# 一键安装脚本
$ curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

## 参考

- [docker 安装](https://www.runoob.com/docker/ubuntu-docker-install.html)

## vnc

**服务端**

```shell
sudo apt install xfonts-base xfonts-75dpi xfonts-100dpi
sudo apt install tightvncserver

# centos
```

**配置**

```shell
# /etc/systemd/system/vncserver@:1.service
[Unit]
Description=Remote desktop service (VNC)
After=syslog.target network.target

[Service]
#User=wii
#Group=wii
#WorkingDirectory=/home/wii
Type=forking

# Clean any existing files in /tmp/.X11-unix environment
ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'
# ExecStart=/sbin/runuser -l wii -c "/usr/bin/vncserver %i -geometry 1920x1080"
ExecStart=/bin/sh -c "/usr/bin/vncserver %i -geometry 1920x1080"
PIDFile=/home/wii/.vnc/%H%i.pid
ExecStop=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'

[Install]
WantedBy=multi-user.target
```

**客户端**

从[这里](https://www.tightvnc.com/download.php)下载。

**参考**

- https://www.tecmint.com/install-and-configure-vnc-server-in-centos-7/
- https://www.tecmint.com/install-tightvnc-remote-desktop/

## jdk

**手动下载**

```shell
# 从这里 https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html 下载 jdk

# 安装
$ sudo yum install jdk-8u301-linux-x64.rpm
$ sudo alternatives --config java
```

**yum**

```shell
$ yum install -y java-1.8.0-openjdk-devel  # 安装 jdk
$ yum install -y java-1.8.0-openjdk        # 安装 jre
```

## mvn

从 [这里](https://maven.apache.org/) 下载。

```shell
# 修改 conf/settings.xml
# 注释掉如下内容
<mirror>
    <id>maven-default-http-blocker</id>
    <mirrorOf>external:http:*</mirrorOf>
    <name>Pseudo repository to mirror external repositories initially using HTTP.</name>
    <url>http://0.0.0.0/</url>
    <blocked>true</blocked>
</mirror>
```

## npm

```shell
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
$ nvm install v12
# nrm
$ npm install nrm
$ nrm use taobao
```

## mysql / mariadb

```shell
$ yum install mariadb mariadb-server
$ systemctl start mariadb   #启动mariadb
$ systemctl enable mariadb  #设置开机自启动
$ mysql_secure_installation #设置root密码等相关
$ mysql -uroot -p           #测试登录
```

## ~~ambari~~ (using MapR)

**依赖**

- jdk

- mvn

- rpm-build（centos）

- npm

- python-devel

  - `sudo yum install -y python-devel`

- ant

  ```shell
  #!/bin/bash
  set -ex
  ANT_VERSION=1.10.11
  wget http://archive.apache.org/dist/ant/binaries/apache-ant-${ANT_VERSION}-bin.tar.gz
  sudo tar xvfvz apache-ant-${ANT_VERSION}-bin.tar.gz -C /opt
  sudo ln -sfn /opt/apache-ant-${ANT_VERSION} /opt/ant
  sudo sh -c 'echo ANT_HOME=/opt/ant >> /etc/environment'
  sudo ln -sfn /opt/ant/bin/ant /usr/bin/ant
  
  ant -version
  rm apache-ant-${ANT_VERSION}-bin.tar.gz
  ```

- gcc

**下载**

从 [这里](https://github.com/apache/ambari/tree/branch-2.7)下载，或使用 git 克隆，`git clone git@github.com:apache/ambari.git`，切换分支 `git checkout branch-2.7`。

**安装**

参考[这里](https://cwiki.apache.org/confluence/display/AMBARI/Installation+Guide+for+Ambari+2.7.5)。

```shell
# 添加 -Drat.skip=true
$ mvn -B clean install rpm:rpm -DnewVersion=2.7.5.0.0 -DbuildNumber=5895e4ed6b30a2da8a90fee2403b6cab91d19972 -DskipTests -Drat.skip=true -Dpython.ver="python >= 2.6"

# 需要修改所有 https://s3.amazonaws.com/dev.hortonworks.com/ 开头的连接
# 参照这个 mr 修改 https://github.com/apache/ambari/pull/3283/commits/3dca705f831383274a78a8c981ac2b12e2ecce85
```

**异常**

```shell
# 报错
[ERROR] Failed to execute goal com.github.eirslett:frontend-maven-plugin:1.3:npm (npm install) on project ambari-admin: Failed to run task: 'npm install --unsafe-perm' failed. (error code 1) -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
[ERROR]
[ERROR] After correcting the problems, you can resume the build with the command
[ERROR]   mvn <args> -rf :ambari-admin

# 处理
cd ambari-admin/src/main/resources/ui/admin-web
npm install --unsafe-perm

# 继续打包
mvn -B clean install rpm:rpm -DnewVersion=2.7.5.0.0 -DbuildNumber=5895e4ed6b30a2da8a90fee2403b6cab91d19972 -DskipTests -Drat.skip=true -Dpython.ver="python >= 2.6" -rf :ambari-admin
```

**问题集锦**

- https://www.cnblogs.com/barneywill/p/10264135.html

## 配置远程启动

整机无负载功率在 100w 左右，功率大且并不常用，工作的时候可能会用到。远程关闭、启动方案是通过设置 BIOS 的断电恢复后自动启动 + 小米智能插座实现。

