---
title: python virtualenv
categories: 
  - [python, library]
tags:
  - virtualenv
date: 2020/12/10 19:00:00
---

# 安装

```shell
# ubuntu
$ sudo apt install python3-pip # 安装pip3
## OR
$ sudo apt-get install python-pip python-dev python-virtualenv # for Python 2.7
$ sudo apt-get install python3-pip python3-dev python-virtualenv # for Python 3.n

# pip
$ pip3 install virtualenv
```

## 新建虚拟环境

```shell
$ virtualenv venv	# sample

$ virtualenv --no-site-packages venv     # 不使用外部库; 默认不使用，在virtualenv>=20版本中移除，添加上可能会报错
$ virtualenv --system-site-packages venv # 使用系统库
$ virtualenv -p python3 venv             # 指定Python版本
$ virtualenv --copies venv 							 # 复制Python程序等，而不是链接
```

## 激活新环境

```shell
# 进入环境
$ cd venv 
# 激活
$ source bin/activate

$ source bin/activate # bash, sh, ksh, or zsh
$ source bin/activate.csh  # csh or tcsh
```

## 退出环境

```shell
deactivate
```

## 配合supervisor

### supervisor配置文件

```ini
[program:myproj-uwsgi]
process_name=myproj-uwsgi
command=/home/myuser/.virtualenvs/myproj/bin/uwsgi
    --chdir /home/myuser/projects/myproj
    -w myproj:app
environment=PATH="/home/myuser/.virtualenvs/myproj/bin:%(ENV_PATH)s"
user=myuser
group=myuser
killasgroup=true
startsecs=5
stopwaitsecs=10
```

## 导出环境

```shell
# 导出
$ pip freeze > requirements
# 安装
$ pip install -r requirements
```