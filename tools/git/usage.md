---
title: git 使用
categories: 
  - [工具,git]
tags:
  - git
date: 2020/11/20 00:00:00
update: 2020/11/20 00:00:00
---

[toc]

# basic

生成公钥

```shell
$ ssh-keygen -t rsa -C "<your email>"              # id_rsa
$ ssh-keygen -t rsa -C "<your another email>"      # id_rsa_work

# 新的算法
ssh-keygen -t ed25519 -C "<your email>"
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
git submodule update --init --recursive

# 递归clone
$ git clone ... --recursive
$ git clone --recurse-submodules ...

# pull with submodules
$ git pull --recurse-submodules

# 更新子模块至最新提交
$ git submodule update --remote --merge

# 重置 submodule commit id
git submodule update --init
```

## 清理

```shell
$ rm -rf path/to/submodule
$ rm -rf .git/modules/{module}
$ vim .gitmodules # 移除对应 module
$ vim .git/config # 移除对应 module
```

# tags

```shell
$ git tag -s "tag_name" -m "comments"
# push 到远端
$ git push origin <tag_name>	# one
$ git push --tags							# all
$ git push origin --tags			# all
```

# 删除大文件

```shell
git filter-branch -f --prune-empty --index-filter "git rm -rf --cached --ignore-unmatch recommend/keywords.txt" --tag-name-filter cat -- --all
```

# 修改 commit 用户名

```shell
# 设置用户名、邮箱
git config user.name "New User"
git config user.email "newuser@gmail.com"

git log
git rebase -i <commit-id> # 这个 commit-id 需要修改的前一个
# 把需要修改的 commit 前的 'pick' 改为 'edit', 保存并退出

# 重复下面两步
git commit --amend --reset-author --no-edit
git rebase --continue

# 强制提交
git push --force-with-lease
```

参考[这里](https://stackoverflow.com/questions/3042437/how-to-change-the-commit-author-for-one-specific-commit)。

# 查看某一行修改人

```shell
git blame <file> -L <start-line>,<end-line>
```

# branch

```shell
# 删除分支
git push origin --delete <branch>
```

# 配置

```shell
# 打印配置
git config -l
# 打印全局配置
git config --global -l	# 当前用户的配置
git config --sysmte -l	# 系统配置
```

## 作用域 

```shell
          默认仓库级别
--system  系统
--global  用户目录
```

## 配置项

```shell
git config user.name '...'
git config user.email '...'
```

## 代理

```shell
# 设置
git config --global http.proxy http://user:password@domain:port
git config --global https.proxy http://user:password@domain:port

# 取消设置
git config --global --unset http.proxy
git config --global --unset https.proxy
```

# 中文乱码

[参考](https://gist.github.com/nightire/5069597#file-git-windows-md)

```bash
git config --global core.quotepath false  		# 显示 status 编码
git config --global gui.encoding utf-8			# 图形界面编码
git config --global i18n.commit.encoding utf-8	# 提交信息编码
git config --global i18n.logoutputencoding utf-8	# 输出 log 编码
export LESSCHARSET=utf-8
# 最后一条命令是因为 git log 默认使用 less 分页，所以需要 bash 对 less 命令进行 utf-8 编码
# 命令

```shell
# init
git init

# add, 添加改动
git add file

# commit
git commit -m 'comment' --author='sample@x.com' 
## 修改刚刚 commit 的内容
git commit --amend -m 'comment' ...
```

# git-remote-http libcurl-httpd24.so.4 不存在

**错误信息**

```shell
/opt/rh/rh-git218/root/usr/libexec/git-core/git-remote-http: error while loading shared libraries: libcurl-httpd24.so.4: cannot open shared object file: No such file or directory
```

**解决**

```shell
find / -name 'libcurl-httpd24.so.4'
/opt/rh/httpd24/root/usr/lib64/libcurl-httpd24.so.4

# 修改 LD_LIBRARY_PATH 环境变量
# vim ~/.bashrc
export LD_LIBRARY_PATH=/opt/rh/httpd24/root/usr/lib64:$LD_LIBRARY_PATH

source ~/.bashrc
```

