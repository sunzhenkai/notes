---
title: rsync
categories:
	- [tools, rsync]
tags:
	- rsync
comments: true
date: 2021/06/01 00:00:00
update: 2021/06/01 00:00:00
---

# 安装

```shell
$ brew install rsync
```

# 参数

```shell
P	等价于 --partial --progress
a	archive 模式
```



# 同步文件夹

```shell
$ rsync -Pav <local> <user@ip:remote-dist>

# 使用特定 id_rsa
$ rsync -Pav -e "ssh -i ~/.ssh/id_rsa_sensors" <local> <user@ip:remote-dist>

```

# 实时同步

使用工具 [fswatch](http://emcrisostomo.github.io/fswatch/usage.html)。

```shell
# 安装依赖
$ brew install fswatch

# watch 文件变动
$ fswatch . | xargs -n1 -I{} <do-something>

# 定义同步方法
function dosyn() {
    if [ ! -e .RSYNCING ]; then
        touch .RSYNCING
        echo "begin to sync"
        rsync -Pav -e "ssh -i ~/.ssh/<secret-id>" <local> <user@ip:remote-dist>   # 修改这里
        echo "rsync done at $(date), sleep 30 seconds"
        sleep 30
        rm .RSYNCING
        echo "sleep done at $(date)"
    else
        echo "syncing OR sleeping ..."
    fi
}
 
[ -e .RSYNCING ] && rm .RSYNCING
export -f dosyn
fswatch -e .RSYNCING -ro . | xargs -P0 -n1 -I{} bash -c 'dosyn'
```

