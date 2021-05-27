---
title: go startup
categories: 
	- [coding, go]
tags:
	- go
date: 2020/12/30 12:00:00
update: 2020/12/30 12:00:00
---

# 安装

```shell
# mac
$ brew install go
```

# 编译

```shell
$ go build main.go
$ go build -o output-file-name main.go
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

# 参考

- [Effective Go](https://golang.org/doc/effective_go.html#package-names)
- [Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [菜鸟教程](https://www.runoob.com/go/go-tutorial.html)