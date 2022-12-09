---
title: linux usage
categories: 
	- [linux,notes]
tags:
	- Linux
date: 2020/12/21 9:40:00
update: 2020/12/21 9:40:00
---

[toc]

# 文件及目录

## 按大小排序打印文件

```shell
$ ls -lSh   # -S: 按大小排序; -h: human readable
$ ls -lShr  # -r: 倒序
$ ls -lShrR # -R: 递归列出子文件夹
```

## 在特定文件内查找内容

**grep**

```shell
$ grep -inr --include pom.xml apollo . # i: 忽略大小写; r: 递归; n: 行号
```

**vim**

```shell
:vimgrep /apollo/g **/pom.xml 
```

## 递归查找特定文件[夹]

```shell
# command
find <search-pa>

# 示例
$ find . -name '\.idea'
```

**删除**

```shell
$ find . -name '\.idea' | xargs rm  -r
```

## 目录栈

`dirs` : 查看当前目录栈

- `-v` : 列出目录及其序号
- `-l` : 列出目录全名
- `-c` : 清空目录栈

`pushd` ：改变目录并将原目录压入栈

`popd` : 修改当前目录为栈顶目录并将栈顶目录出栈

```shell
$  ~ dirs
~
$  ~ pushd Downloads 
~/Downloads ~
$  Downloads dirs
~/Downloads ~
$  Downloads popd           
~
$  ~ dirs
~
```

## 递归查看从根至某个路径的权限

```shell
$ namei -om /path/to/check

# 示例
$ namei -om /home/wii/share/
f: /home/wii/share/
 dr-xr-xr-x root root /
 drwxr-xr-x root root home
 drwx------ wii  wii  wii
 drwxrwxrwx wii  wii  share
```

如果一个用户需要访问一个目录，应该有访问其父路径的权限。

## 获取脚本路径

### 脚本所在文件夹

支持使用 source 引用脚本。

```shell
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
```

## 查看软连文件大小

```shell
# -L 
ls -lhL
```

# 用户

## 创建用户

```shell
$ useradd -d <home-dir> -s <login-shell> -g <GROUP> username

# 示例
$ useradd -d /home/wii -s /bin/bash -g wheel wii

# 添加到 sudoers 组
$ usermod -aG wheel <user-name>
```

## 免密登录

```shell
# 以配置 主机A 免密登录 主机B 为例
# [A] 生成密钥文件(~/.ssh/id_rsa, ~/.ssh/id_rsa.pub), 如果已生成可略过
$ ssh-keygen -t rsa -C <email>

# [A] 拷贝密钥
$ ssh-copy-id -i ~/.ssh/id_rsa.pub <user@remote-host>

# [B] 修改目录权限
$ chmod 700 ./.ssh 
$ chmod 600 ~/.ssh/authorized_keys

# [A] 登录
$ ssh <remote-host>
```

## 切换至 root 用户

```shell
# sudo -i / sudo -s / sudo bash / sudo su

Summary of the differences found   
                                               corrupted by user's 
                HOME=/root      uses root's PATH     env vars
sudo -i         Y               Y[2]                 N
sudo -s         N               Y[2]                 Y
sudo bash       N               Y[2]                 Y
sudo su         Y               N[1]                 Y
```

## root 权限无需密码

```shell
# 修改权限
sudo chmod u+w /etc/sudoers

# 修改 /etc/sudoers，添加下面内容
<username>    ALL=(ALL) NOPASSWD: ALL
```

## ssh 无需确认添加指纹信息

```shell
ssh -o StrictHostKeyChecking=no

# 比如
The authenticity of host '192.168.6.10 (<no hostip for proxy command>)' can't be established.
ECDSA key fingerprint is SHA256:Zag81PG/YLKsybs3QAdsea4Sd4gJvwaa+c49X6ts3buM.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

## 切换用户

```shell
su <user>
```

# 进程

## 批量杀死进程

```shell
# 按进程名称
$ ps aux | grep <process-name> | awk '{print $2}' | xargs kill -9
# 按端口
$ lsof -i:8200 | awk '{print $2}' | xargs kill -9
```

## 滚动日志

```shell
kill -USR1 <pid>
```

## 排查进程无故 killed

```shell
$ dmesg -T| grep -E -i -B100 'killed process'
```

# 磁盘读写

```shell
$ iotop -o 
```

**参数**

```shell
-o 仅显示有速度的进程
```

# tail 多个远程文件

```shell
# 在一台机器执行
ssh -n user@host1 'tail -f /path/to/file' &
ssh -n user@host2 'tail -f /path/to/file' &
ssh -n user@host3 'tail -f /path/to/file' &
```

# 日期

```shell
# 当前年月日
$ date '+%Y-%m-%d'
2021-11-06
$ date '+%Y%m%d-%H%M%S'
20220916-110256
```

- **`%D`** – Display date as mm/dd/yy
- **`%Y`** – Year (e.g., 2020)
- **`%m`** – Month (01-12)
- **`%B`** – Long month name (e.g., November)
- **`%b`** – Short month name (e.g., Nov)
- **`%d`** – Day of month (e.g., 01)
- **`%j`** – Day of year (001-366)
- **`%u`** – Day of week (1-7)
- **`%A`** – Full weekday name (e.g., Friday)
- **`%a`** – Short weekday name (e.g., Fri)
- **`%H`** – Hour (00-23)
- **`%I`** – Hour (01-12)
- **`%M`** – Minute (00-59)
- **`%S`** – Second (00-60)

# Tips

## 打印保存在变量内的变量值

```shell
# ${!ref}
$ real="hello"
$ ref=real
$ echo ${!ref}
hello

# 环境变量可以也可以使用 printenv
$ export real="hello"
$ ref=real
$ printenv $ref
hello
```

# ssh

## 端口转发

```shell
ssh -i <secret> -L <port-local>:<ip>:<port-remote> <user>@<host>

# 实例
ssh -i ~/.ssh/id_rsa -L 8000:192.168.0.10:8000 wii@relay.company.com

# 多端口后台转发
ssh -i <secret> <user>@<host> -fCqTnN -L <port-local>:<ip>:<port-remote> -L <port-local>:<ip>:<port-remote> ...

-f -N: 仅后台转发端口
-C: 压缩数据d
-q: 安静模式
-T: 禁止远程分配终端
-n: 关闭标准输入
-N: 不执行远程命令
```

## 代理

```shell
# socks5 代理
ssh -D <localhost>:<local-port> <remote-host>
```

## pem 文件登录

**命令方式**

```shell
ssh -i key.pem user@host
```

**配置方式**

```shell
Host <host>
   User <user>
   IdentityFile /path/to/key.pem
   IdentitiesOnly yes
```

## 配置密码登录

```shell
sudo vim /etc/ssh/sshd_config
# 设置
PasswordAuthentication yes

# 重启 ssh 服务
sudo service sshd restart
```

## 远程执行命令

```shell
$ ssh -i /path/to/secret-key-file user@host "command"
```

**示例**

```shell
# 从 172.31.0.1 同步 consul 数据到本机
C="/usr/local/consul/consul kv export abtest-platform > /tmp/abtest-consul-data.json"
ssh mobdev@172.31.0.1 "$C"
scp mobdev@172.31.0.1:/tmp/abtest-consul-data.json /tmp/
/home/ubuntu/app/consul/consul kv import @/tmp/abtest-consul-data.json
```

## 免密登录

```shell
# 拷贝密钥, 免密登录
ssh-copy-id <user>@<host> -p <port>

# 手动拷贝 *.pub 内容添加至目标机 ~/.ssh/authorized_keys
```

### 无法免密登录

```shell
# 目标机
## 检查 authorized_keys 读写权限
chmod 0600 ~/.ssh/authorized_keys
## 检查 authorized_keys owner+group
chown <user> ~/.ssh/authorized_keys
chgrp <group> ~/.ssh/authorized_keys
```

# 网络

## 端口

### 查看进程监听的端口

```shell
# 查看进程在监听的端口
lsof -iTCP -sTCP:LISTEN | grep <pid/pname>
```

### 查看所有监听的端口

```shell
sudo netstat -tunlp
```

## 网络速度

- iftop
- nload
- cbm
- ifstat

```shell
sudo iftop

# 安装
sudo apt install iftop
```

# 自启动

```shell
crontab -e
# 添加如下内容
@reboot /path/to/program
```

# 查看系统信息

```shell
# lsb_release
$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04.5 LTS
Release:	18.04
Codename:	bionic

# os-release
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="18.04.5 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.5 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic

# hostnamectl
$ hostnamectl
   Static hostname: mvm
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 2d1d6a0bc90a451ab6ed062e9c2153bf
           Boot ID: d8d4f12a272847b0b7d1de1ec2307493
    Virtualization: qemu
  Operating System: Ubuntu 18.04.5 LTS
            Kernel: Linux 4.15.0-126-generic
      Architecture: x86-64
      
# issue
$ cat /etc/issue
Ubuntu 18.04.5 LTS \n \l
```

## 查看发行版信息

```shell
# uname
$ uname -r  # OR -a
4.15.0-126-generic
```

# systemctl

## 查看日志

```shell
journalctl -u <service> -f
```

# 需求

## 同步文件夹

```shell
async -auz <path-to-local> user@host:/path/to/remote
```

# 节点间测速

```shell
# 安装 iperf
apt install iperf3

# node A
iperf3 -s

# node B
iperf3 -c <node-b>
```

# 磁盘测速

