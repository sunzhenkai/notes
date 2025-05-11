---
title: go usage
categories: 
  - [coding, go]
tags:
  - go
date: "2021-03-24T00:00:00+08:00"
update: "2021-03-24T00:00:00+08:00"
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

go env -w GO111MODULE=on
go env -w GOPROXY=direct
go env -w GOSUMDB=off
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

# GC

## 阶段

| 阶段                     | STW（STOP THE WORLD） |
| ------------------------ | --------------------- |
| STW sweep termination    | YES                   |
| concurrent mark and scan | NO                    |
| STW mark termination     | YES                   |

## gc log

```shell
GODEBUG=gctrace=1 ./<program> <parameters>
# GODEBUG 多值
GODEBUG=gctrace=1,schedtrace=1000./<program> <parameters>

gctrace=1 : 打印 gc 日志
schedtrace=1000 : 每 1000 ms 打印一次调度器的摘要信息
```

### 格式

```html
gctrace: setting gctrace=1 causes the garbage collector to emit a single line to standard
error at each collection, summarizing the amount of memory collected and the
length of the pause. Setting gctrace=2 emits the same summary but also
repeats each collection. The format of this line is subject to change.
Currently, it is:
	gc # @#s #%: #+#+# ms clock, #+#/#/#+# ms cpu, #->#-># MB, # MB goal, # P
where the fields are as follows:
	gc #        the GC number, incremented at each GC
	@#s         time in seconds since program start
	#%          percentage of time spent in GC since program start
	#+...+#     wall-clock/CPU times for the phases of the GC
	#->#-># MB  heap size at GC start, at GC end, and live heap
	# MB goal   goal heap size
	# P         number of processors used
The phases are stop-the-world (STW) sweep termination, concurrent
mark and scan, and STW mark termination. The CPU times
for mark/scan are broken down in to assist time (GC performed in
line with allocation), background GC time, and idle GC time.
If the line ends with "(forced)", this GC was forced by a
runtime.GC() call and all phases are STW.
```

```shell
gc # @#s #%: #+#+# ms clock, #+#/#/#+# ms cpu, #->#-># MB, # MB goal, # P
```

- `gc #` ：编号
- `@#s` ：自程序启动到打印 gc 日志的时间
- `#%`：自程序启动，gc 花费的时间占比
- `#+#+# ms clock`：垃圾回收时间，(sweep)+(mark & scan)+(termination) 
- `#+#/#/#+# ms cpu`：垃圾回收占用的 CPU 时间 (sweep)+(mark & scan (辅助时间/后台gc时间/空闲时间))+(termination) 
- `#->#-># MB`：gc 开始时堆大小、gc 结束时堆大小、存活堆大小
- `#MB goal` ：全局堆大小
- `#P` ：使用的处理器数量

> ms cpu 约等于 cpu_num * ms clock

**示例**

```shell
gc 35 @1130.489s 1%: 0.71+3290+0.12 ms clock, 5.7+5932/26084/4619+1.0 ms cpu, 35956->37042->8445 MB, 37411 MB goal, 32 P

1. 第 35 次 gc，距离程序启动 1130s，自程序启动 gc 时间占比 1%
```

**参考**

- [golang_debug_gctrace](https://zboya.github.io/post/golang_debug_gctrace/)

# Profile

```shell
curl http://127.0.0.1:12067/debug/pprof/profile > profile.dat
go tool pprof -http=:8081 ~/profile.dat

curl http://127.0.0.1:12067/debug/pprof/heap > heap.dat
go tool pprof -alloc_space -http=:8082 ~/heap.at
```

# 类型转换

## String 转数字

```shell
# string -> int32
if tr, err := strconv.ParseInt("9207", 10, 32); err != nil {
	res = int32(tr)
}

# string -> int64
res, err := strconv.ParseInt("9207", 10, 64)
```

# 问题

## `GLIBC_2.32' not found`

```shell
# 错误
./main: /lib64/libc.so.6: version `GLIBC_2.32' not found (required by ./main)

# 解决: 编译的时候 CGO_ENABLED 设置为 0
CGO_ENABLED=0 go build
```

