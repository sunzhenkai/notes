---
title: go common
categories: 
	- [coding, go]
tags:
	- go
date: 2021/03/24 00:00:00
update: 2021/03/24 00:00:00
---

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

## 解析请求

```go

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
```

