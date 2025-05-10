---
title: go startup
categories: 
  - [coding, go]
tags:
  - go
date: "2020-12-30T12:00:00+08:00"
update: "2020-12-30T12:00:00+08:00"
---

[TOC]

# 安装

```shell
# mac
$ brew install go
```

# 编译

```shell
$ go build main.go
$ go build -o output-file-name main.go

# 打印 gc 信息
$ go build -gcflags="-m" main.go
```

## 静态编译

不依赖共享库，可以避免 libc 库接口不兼容的问题。

```shell
CGO_ENABLED=0 go build -ldflags="-s -w -extldflags=-static" main.go
```

## 示例

**代码**

```go
package main

import "fmt"

func main() {
  fmt.Println("Hello World!")
}
```

**运行**

```shell
$ go run hello.go
Hello World!
```

**编译**

```shell
$ go build hello.go
```

## 添加依赖库示例

```shell
# main.go
```

# 依赖

使用 `go get` 下载公开库，该命令会把依赖下载至第一个 `GOPATH` 下的 `src` 目录下。

| 参数 | 说明                 |
| ---- | -------------------- |
| -v   | 打印详情日志         |
| -d   | 只下载不安装         |
| -u   | 下载丢失的包，不更新 |

**示例**

```shell
$ go get [dep-name]				# 安装单个依赖
$ go get -d -v ./... 			# 递归地下载当前目录下所有文件的依赖
```

# Package

报名尽量使用单个词。

```go
package http;
```

# 私有库

## terminal prompts disabled

```shell
go: gitlab.company.com/org/pkg@v0.0.1: reading https://goproxy.cn/gitlab.company.com/org/pkg/@v/v0.0.1.mod: 404 Not Found
	server response:
	not found: gitlab.company.com/org/pkg@v0.0.1: invalid version: git fetch -f origin refs/heads/*:refs/heads/* refs/tags/*:refs/tags/* in /tmp/gopath/pkg/mod/cache/vcs/1b2a69e43fbd284ebef999cca485d367b743c300d2970b093def252bae54d3ef: exit status 128:
		fatal: could not read Username for 'http://gitlab.company.com': terminal prompts disabled
```

私有项目，默认走 goproxy，故找不到 pkg。

```shell
# 设置 pkg 路径为私有库
go env -w GOPRIVATE="gitlab.company.com/org"

# get
GIT_TERMINAL_PROMPT=1 go get
```

或者使用 ssh 认证。

```shell
git config --global --add url."git@your-repo.com:".insteadOf "https://your-repo.com/"
```

# Env

```shell
# 查看 go env
$ go env
GO111MODULE=""
GOARCH="amd64"
...

# 设置
$ go env -w GOPROXY="..."

# 取消设置
$ go env -u GOPROXY
```

## Proxy

```shell
# 设置 proxy
$ go env -w GOPROXY="..."

# 不使用 proxy 的仓库
$ go env -w GOPRIVATE "git.a.com,git.b.com,..."
```

# Mod

```shell
# 下载依赖
go mod download

# 整理依赖
go mod tidy

# 清楚缓存（删除所有下载的库，谨慎操作）
go clean -modcache
```

# 参考

- [Effective Go](https://golang.org/doc/effective_go.html#package-names)
- [Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [菜鸟教程](https://www.runoob.com/go/go-tutorial.html)