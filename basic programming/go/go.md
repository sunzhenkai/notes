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

## 版本

```shell
# 格式
v<major>.<minor>.<patch>-<pre-release>.<patch>
# 实例
v1.2.23
v1.4.0-beta.2
v2.3.4-alpha.3
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

## 数组 / slice

**声明**

```go
var variable_name [SIZE] variable_type
var variable_name [SIZE1][SIZE2]...[SIZEN] variable_type  // 多维数组
```

**初始化**

```go
var balance = [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
balance := [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
il := []int{1, 2}

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

// 创建空数组
s := make([]int, 0, 10)
// 获取长度
len(s) // 0
// 获取容量
cap(s) // 10
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

### list

底层实现是双向链表。

```shell
# 创建
l := list.New()

# 插入元素
l.PushBack(1)
l.PushFront(2)

# 插入其他列表
l.PushFrontList(ol)
l.PushBackList(ol)

# 移除
l.Remove(1)

# 长度
l.Len()
```

## 集合

```go
var m map[string]string = map[string]string{"France": "Paris", "Italy": "Rome", "Japan": "Tokyo"}
m := make(map[int]int)

// 遍历参考章节 循环
```

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

// list - 顺序
for i := l.Front(); i != nil; i = i.Next() {
    fmt.Println(i.Value)
}
// list - 
for i := l.Back(); i != nil; i = i.Prev() {
		fmt.Println(i.Value)
}

// 数组
for i := 0; i < len(arr); i++ {
    //arr[i]
}
for index, value := range arrHaiCoder{
}
for _, value := range arrHaiCoder{  // 忽略 index
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

# 打印

```shell
# fmt.Printf 占位符
%T	打印变量类型
%p	打印指针
%v	打印值
%s	打印字符串
%d	打印数值
```



# 特性

## 语法糖

## 空指针处理

## 函数式编程

## 接口

```go
// 定义接口
type FileReader interface {
	NextLine() string
	HasNext() bool
	Close()
}

// 定义实现接口实现结构
type FileReaderImpl struct {
	dataPath string
	file     *os.File
	scanner  *bufio.Scanner
	done     bool
	buf      string
}

// 定义接口实现方法
func (impl *FileReaderImpl) NextLine() string {
	t := impl.buf
	impl.done = !impl.scanner.Scan()

	if err := impl.scanner.Err(); err != nil {
		log.Fatal(err)
	} else {
		v := impl.scanner.Text()
		impl.buf = v
	}

	return t
}

func (impl *FileReaderImpl) HasNext() bool {
	return !impl.done
}

func (impl *FileReaderImpl) Close() {
	err := impl.file.Close()
	if err != nil {
		log.Fatal(err)
	}
}

// 定义创建接口方法
func NewFileReader(dp string) FileReader {
	file, err := os.Open(dp)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	sr := &FileReaderImpl{dataPath: dp, file: file, scanner: scanner, done: false}
	// read one line, for HasNext
	sr.NextLine()
	return sr
}
```

> **注意**
>
> NextLine 方法定义由于需要修改 impl 对象内容，必须使用指针。如果使用指针，创建接口时，必须加 & ，比如 `sr := &FileReaderImpl{dataPath: dp, file: file, scanner: scanner, done: false}`。

## 指针

### slice 与指针

```go
func PointArg(l interface{}) {
	fmt.Printf("%p %p\n", l, &l)
}

func main() {
	l := make([]int, 0, 10)
	fmt.Printf("%T %p\n", l, l)
	PointArg(l)
}

// 输出
[]int 0xc0000b8000
0xc0000b8000 0xc000096220

// 分析
1. l 保存的 make 返回的指针
2. 指针传参，直接打印参数值为源参数内存地址；对指针参数 & 操作，返回参数变量的内存地址
```

### struct 与指针

```go
func PointArg(l interface{}) {
	fmt.Printf("%p %p\n", l, &l)
}

type Person struct {
	name string
}

func main() {
	p := Person{name: "wii"}
	fmt.Printf("%T %v %p\n", p, p, &p)
	PointArg(p)
}

// 输出
main.Person {wii} 0xc000010240
%!p(main.Person={wii}) 0xc000010270

// 分析
1. p 不是指针类型
2. 非指针参数传递，会导致内存拷贝
```

# Tips

## Interface{} 

### 作为类型参数

使用 `interface{}` 作为参数类型，来匹配任意类型，注意，不可用 `*interface{}`

### 转换类型

```go
// i 为 interface{} 变量, 实际类型为 map[string]interface{}
for k, v := range i.(map[string]interface{}) {   // 使 i 识别为 map[string]interface{} 类型，并遍历
  ...
}  
```

## 函数变量

```go
// 保存函数
func main() {
    var fns []func()
    fns = append(fns, beeper)
    fns = append(fns, pinger)

    for _, fn := range fns {
        fn()
    }
}

func beeper() {
    fmt.Println("beep-beep")
}

func pinger() {
    fmt.Println("ping-ping")
}

// 另外一个示例
type dispatcher struct {
    listeners []func()
}

func (d *dispatcher) addListener(f func()) {
    d.listeners = append(d.listeners, f)
}

func (d *dispatcher) notify() {
    for _, f := range d.listeners {
        f()
    }
}

func ping() {
    fmt.Println("Ping... ping...")
}

func beep() {
    fmt.Println("Beep... beep...")
}

func main() {
    d := dispatcher{}
    d.addListener(ping)
    d.addListener(beep)
    d.notify()
}
```

## 类型判断

```go
t := map[string]interface{}{}
switch t.(type) {
case map[string]interface{}:
	for tk, tv := range t.(map[string]interface{}) {
		r[tk] = tv
	}
default:
	r[cvt.Name] = t
}
```

# 单测（Unit Tests）

## 单测文件

创建名为 `{code}_test.go` 的文件，即为 `{code}.go` 的单测文件。

## 示例

**echo.go**

```go
package tm

func Echo(s string) string {
	return s
}
```

**echo_tests.go**

```go
package tm

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestEcho(t *testing.T) {
	word := "hello"
	echo := Echo(word)
	assert.Equal(t, word, echo)
}
```



# 参考

- [Go 语言设计与实现](https://draveness.me/golang/)
- [指针](https://stackoverflow.com/questions/4938612/how-do-i-print-the-pointer-value-of-a-go-object-what-does-the-pointer-value-mea)