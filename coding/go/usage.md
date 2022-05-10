---
title: go usage
categories: 
	- [coding, go]
tags:
	- go
date: 2021/03/24 00:00:00
update: 2021/03/24 00:00:00
---

[TOC]

# 说明

- 如果一个对象的字段使用指针的方式引用了另外一个对象的字段，那么备用的变量会增加引用次数，且从栈迁移至堆，不会出现垃圾回收导致内存非法访问问题

# time.Duration

```go
d := time.Duration(10)
d := 10 * time.Nanosecond
// d := rand.Intn(100) * time.Nanosecond ERROR
d := time.Duration(rand.Intn(100)) * time.Nanosecond
```

# 打印

## 打印数组

```go
fmt.Printf("%v", []float64{0.1, 0.5, 0.99, 0.999})
```

# network

## 发送请求

```go
urlBaiduFanyiSug := "https://fanyi.baidu.com/sug"
data := map[string]string{"kw": "hi"}
js, _ := json.Marshal(data)
res, err := http.Post(urlBaiduFanyiSug, "application/json", bytes.NewBuffer(js))
```

# []byte 和 string

```go
// []byte -> string; bys: []byte
s := string(bys)

// string -> []byte
bys := []byte(s)
```

# 依赖

```shell
$ go mod tidy # 整理依赖, 下载没有下载的, 移除没有的
$ go mod download # 下载依赖
$ go get # 更新依赖

# 添加依赖到 go.mod
$ go get -v -t ./...
```

## git 仓库使用 ssh 认证

```shell
git config --global --add url."git@your-repo.com:".insteadOf "https://your-repo.com/"
# 通过 ~/.gitconfig 查看配置，如果还是有问题可检查下配置
```

## 查看依赖版本

```shell
go list -m -versions git.*.com/org/repo
```

## 添加依赖

```shell
go get git.*.com/org/repo

go mod edit -require git.*.com/org/repo@version
```

