---
title: Go 语言基础
categories: 
	- [coding, go]
tags:
	- go
date: 2021/03/01 00:00:00
update: 2021/03/01 00:00:00
---

[toc]

# 组织

## 文件

## 包

```go
package main
package config
```

# 数据类型

## 类型

### 数字

| 类型       | 说明                               |
| ---------- | ---------------------------------- |
| uint8      | -                                  |
| uint16     | -                                  |
| uint32     | -                                  |
| uint64     | -                                  |
| int8       | -                                  |
| int16      | -                                  |
| int32      | -                                  |
| int64      | -                                  |
| float32    | -                                  |
| float64    | -                                  |
| complex64  | 复数                               |
| complex128 | 复数                               |
| byte       | 类似 uint8                         |
| rune       | 类似 int32                         |
| uint       | 硬件架构相关，32位或64位无符号整型 |
| int        | 硬件架构相关，32位或64位有符号整型 |
| uintptr    | 无符号整型，存放指针               |

**示例**

```go
var i int = 1
var f32 float32 = 1.0
var f64 float64 = 1.0
```

### 字符串

**定义**

```go
var name string = "wii"
```

**操作**

```go
// 拼接
var name string = "name" + " : " + "wii"

// 取长度
len("wii")

// 截断

```

### 布尔

```go
val b bool = true
```

## 限定

## 常量

**字面常量**

```go
var i, s, b = 1, "wii", false
```

**itoa**

特殊常量，可以被编译器修改的常量。

```go
const (
  a = iota   //0
  b          //1
  c          //2
  d = "ha"   //独立值，iota += 1
  e          //"ha"   iota += 1
  f = 100    //iota +=1
  g          //100  iota +=1
  h = iota   //7,恢复计数
  i          //8
)

const (
    i=1<<iota	// 1
    j=3<<iota // 6
    k         // 12
    l         // 24
)
```

## 变量

**声明**

```go
var identifier [type] = v
var id1, id2 [type] = v1, v2  // 如果只声明，不初始化值，必须制定类型；制定初始化值，编译器可自行推断
id3 := value                  // OK := 左侧需要有未被声明过的标识符，有即可
id1 := value                  // ERROR id1 已被声明
id1, id4 := v1, v2            // OK id4 未被声明

var (                         // 因式分解式，一般用于声明全局变量
  id5 type
  id6 type
)
```

**示例**

```go
var a string = "wii"
var b, c int = 1, 2

var e, f = 123, "hello"
g, h := 123, "hello"
```

# 数据结构

## 数组

**声明**

```go
var variable_name [SIZE] variable_type
var variable_name [SIZE1][SIZE2]...[SIZEN] variable_type  // 多维数组
```

**初始化**

```go
var balance = [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
balance := [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}

// ... 代替长度
var balance = [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
balance := [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}

// 通过下表初始化
balance := [5]float32{1:2.0,3:7.0}   // 将索引为 1 和 3 的元素初始化

// 初始化二维数组
a := [3][4]int{  
 {0, 1, 2, 3} ,   /*  第一行索引为 0 */
 {4, 5, 6, 7} ,   /*  第二行索引为 1 */
 {8, 9, 10, 11},   /* 第三行索引为 2 */
}
```

**多维数组示例**

```go
// 先声明后赋值
values := [][]int{}            // 创建数组
row1 := []int{1, 2, 3}
row2 := []int{4, 5, 6}
values = append(values, row1)  // 使用 appped() 函数向空的二维数组添加两行一维数组
values = append(values, row2)

// 维度不一致数组
animals := [][]string{}
row1 := []string{"fish", "shark", "eel"}
row2 := []string{"bird"}
row3 := []string{"lizard", "salamander"}
animals = append(animals, row1)
animals = append(animals, row2)
animals = append(animals, row3)
```

## 列表

## 集合

```go
var m map[string]string = map[string]string{"France": "Paris", "Italy": "Rome", "Japan": "Tokyo"}
```

## 映射

# 语法

## 程序结构

## 注释

```go
// 单行注释

/*
 多行注释
*/
```

## 运算符

## 条件控制

## 循环

```go
// 1. 类似于 for(...; ...; ...)
for init; condition; post { }

// 2. 类似于 while
for condition { }

// 3. 类似于 for (;;)
for { }
```

**range**

```go
// map
for key, value := range oldMap {
    newMap[key] = value
}

strings := []string{"google", "runoob"}
for i, s := range strings {
    fmt.Println(i, s)
}
```

## 函数

**格式**

```go
func function_name( [parameter list] ) [return_types] {
   // 函数体
}
```

**示例**

```go
func swap(x, y string) (string, string) {
   return y, x
}
```

**参数**

```go
// 值传递
func swap(x, y int) int {
   var temp int

   temp = x /* 保存 x 的值 */
   x = y    /* 将 y 值赋给 x */
   y = temp /* 将 temp 值赋给 y*/

   return temp;
}
swap(a, b)

// 引用传递
func swap(x *int, y *int) {
   var temp int
   temp = *x    /* 保持 x 地址上的值 */
   *x = *y      /* 将 y 值赋给 x */
   *y = temp    /* 将 temp 值赋给 y */
}
swap(&a, &b)

// 函数参数
getSquareRoot := func(x float64) float64 {
  return math.Sqrt(x)
}
fmt.Println(getSquareRoot(9))
```

**函数参数**

```go
package main
import "fmt"

// 声明一个函数类型
type cb func(int) int

func main() {
    testCallBack(1, callBack)
    testCallBack(2, func(x int) int {
        fmt.Printf("我是回调，x：%d\n", x)
        return x
    })
}

func testCallBack(x int, f cb) {
    f(x)
}

func callBack(x int) int {
    fmt.Printf("我是回调，x：%d\n", x)
    return x
}
```

**匿名函数**

```go
func getSequence() func() int {
   i:=0
   return func() int {
      i+=1
     return i  
   }
}
```

**方法**

Go 同时有函数和方法，一个方法就是一个包含了接受者的函数，接受者可以是命名类型或者结构体类型的一个值或者是一个指针。所有给定类型的方法属于该类型的方法集，格式如下。

```go
func (variable_name variable_data_type) function_name() [return_type]{
   /* 方法体 */
}
```

下面定义一个结构体，及该类型的一个方法。

```go
package main

import (
   "fmt"  
)

/* 定义结构体 */
type Circle struct {
  radius float64
}

func main() {
  var c1 Circle
  c1.radius = 10.00
  fmt.Println("圆的面积 = ", c1.getArea())
}

//该 method 属于 Circle 类型对象中的方法
func (c Circle) getArea() float64 {
  //c.radius 即为 Circle 类型对象中的属性
  return 3.14 * c.radius * c.radius
}
```

## 结构体

```go
// 定义
type struct_variable_type struct {
   member definition
   member definition
   ...
   member definition
}

// 声明
variable_name := structure_variable_type {value1, value2...valuen}
variable_name := structure_variable_type { key1: value1, key2: value2..., keyn: valuen}
```

**示例**

```go
type Data struct {
  s    string
	sl   []string
	ll   [][]string
}

data := Data {s: "yes"}
```

# 特性

## 语法糖

## 空指针处理

## 函数式编程

## 泛型编程

# 参考

- [Go 语言设计与实现](https://draveness.me/golang/)