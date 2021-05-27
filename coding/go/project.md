---
title: go 工程
categories: 
	- [coding, go]
tags:
	- go
date: 2020/12/30 12:00:00
update: 2020/12/30 12:00:00
---

# Layout

```shell
.
├── api           # 符合 OpenAPI/Swagger 规范的服务接口
├── assets        # 项目中使用的其他资源，如媒体资源等
├── build         # 打包和持续集成; 将容器、包(deb、rpm、pkg)、脚本等放在 build/package; ci 放在 build/ci
├── cmd           # 项目主要应用程序; 如, cmd/app/main.go & cmd/tool/main.go
├── configs       # 配置文件
├── deployments   # Iaas，Paas，系统和容器编排部署配置和模板
├── docs          # 设计和用户文档
├── examples      # 样例
├── init          # 系统初始化(systemd、upstart、sysv) 及进程管理(runit、supervisord)配置
├── internal      # 内部代码，不希望被他人导入的代码
├── pkg           # 外部应用程序可以使用的库代码
├── scripts       # 用于执行构建、安装等操作的脚本
├── test          # 外部测试应用程序和测试数据
├── third_party   # 外部辅助工具
├── tools         # 此项目支持的工具
├── vendor        # 应用程序依赖关系
├── web           # Web 应用程序的特定组件, 静态资源、前端模板等
├── website       # github pages / 网站数据
├── Makefile      # 打包
├── go.mod        # 模块信息
├── LICENSE.md
└── README.md
```

# Start

```shell
$ go mod init github.com/sunzhenkai/go-hello-world
```

# Reference

- [Project Layout](https://github.com/golang-standards/project-layout)
- [Starting a go project](https://www.wolfe.id.au/2020/03/10/starting-a-go-project/)
- [Create your first golang app](https://hackersandslackers.com/create-your-first-golang-app/)

