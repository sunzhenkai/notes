---
title: node - npm
categories: 
  - [前端, node]
tags:
  - npm
date: "2021-05-13T00:00:00+08:00"
update: "2021-05-13T00:00:00+08:00"
---

# install pkg

```shell
$ npm install <pkg-name> # OR npm install <pkg-name>
$ npm install <pkg-name>@<version> -s
```

# Upgrade pkg

```shell
# 检查过时的包
$ npm outdated
$ npm update --save <pkg-name>  # OR --save-dev
```

**使用工具更新所有依赖**

```shell
$ npm i -g npm-check-updates # 安装依赖
$ ncu -u                     # 升级
$ npm install								 # 安装升级后的依赖
```

