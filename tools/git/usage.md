---
title: git 使用
categories: 
	- [工具,git]
tags:
	- git
date: 2020/11/20 00:00:00
update: 2020/11/20 00:00:00
---

# basic

生成公钥

```shell
$ ssh-keygen -t rsa -C "<your email>"              # id_rsa
$ ssh-keygen -t rsa -C "<your another email>"      # id_rsa_work
```

配置全局信息

```shell
$ git config --global user.name "sunzhenkai"
$ git config --global user.email "zhenkai.sun@qq.com"
```

# 多公钥

**适用**

- 一台机器，同一Git仓库，多账号
- 一台机器，多Git仓库，多账号

```shell
# 生成公钥
$ ssh-keygen -t rsa -C "<your email>"              # id_rsa
$ ssh-keygen -t rsa -C "<your another email>"      # id_rsa_work

# 配置 config
$ vim ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa

Host github.com-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_work
    
# 指定账号添加对应公钥
    
# 使用, 克隆或添加remote时使用config定义的Host别名(github.com / github.com-work / 其他)
$ git clone git@github.com:<user-name>/<repo-name>.git
$ git remote add origin git@github.com:<user-name>/<repo-name>.git
```

# stash

用于暂存代码。

```shell
# 暂存
$ git stash save 'message'

# 查看暂存
$ git stash list

# 恢复并删除暂存
$ git stash pop stash@{?}

# 只恢复，不删除暂存
$ git stash apply stash@{?}

# 删除暂存
$ git stash drop stash@{?}

# 删除所有暂存
$ git stash clear
```

# submodule

```shell
# 添加子模块
$ git submodule add <git-address> <localpath>

# 初始化/下载子模块代码
$ git submodule update --init --recursive

# 递归clone
$ git clone ... --recursive
$ git clone --recurse-submodules ...

# 更新子模块至最新提交
$ git submodule update --remote --merge
```

# tags

```shell
$ git tag -s "tag_name" -m "comments"
# push 到远端
$ git push origin <tag_name>	# one
$ git push --tags							# all
$ git push origin --tags			# all
```

