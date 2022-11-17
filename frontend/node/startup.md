---
title: node startup
categories: 
	- [前端, node]
tags:
	- usage
date: 2020/12/30 00:00:00
update: 2020/12/30 00:00:00
---

# 安装

```shell
# nvm
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash    # curl
$ wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash   # nvm

# ls-remote
$ nvm ls-remote
$ nvm ls-remote --lts  # 仅列长期支持版本

# install
$ nvm install v12.20.0
$ nvm install 16  # 安装最新的 16 主版本的最新稳定版

# use
$ nvm use v12.20.0

# set default
$ nvm alias default v12.20.0

# check
$ npm -v
$ node -v
```

**常用工具**

```shell
$ npm install nrm -g
```

# 初始化项目

```shell
$ npm init
```

**安装依赖**

```shell
$ npm install <pkg-name> -s
```

**引入依赖**

```javascript
const name = require('pkg-name');
```

