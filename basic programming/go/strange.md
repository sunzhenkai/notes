---
title: go - strange
categories: 
  - [coding, go]
tags:
  - go
date: 2021/05/13 00:00:00
update: 2021/05/13 00:00:00
---

# 三目元算符

go 没有三目运算符，可以通过定义方法，实现类似的功能。这里要**注意参数拷贝传递**的问题，避免造成性能损失和逻辑错误。首先，不使用指针。

```go
package main

import "reflect"

type Person struct {
	Age int
	Name string
}

func IF(condition bool, tv, fv interface{}) interface{} {
	if condition {
		return tv
	} else {
		return fv
	}
}

func main() {
	a := 1
	b := 2
	c := IF(a > b, a, b)
	println(reflect.TypeOf(c).Name())
	println(c.(int))

	pa := Person{Age: 18, Name: "wii"}
	pb := Person{Age: 16, Name: "bvz"}
	pc := IF(pa.Age > pb.Age, pa, pb)
	println(&pa, &pb, &pc)

	pd := IF(pa.Age > pb.Age, &pa, &pb).(*Person)
	println(&pa, &pb, pd)
}
```

输出。

```shel
int
2
0xc00006ef30 0xc00006ef18 0xc00006eef8
0xc00006ef30 0xc00006ef18 0xc00006ef30
```

从输出可以看出，`pc := IF(pa.Age > pb.Age, pa, pb)` 的返回值的内存地址，既不是 pa，也不是 pb。

# interface{}

```go
package main

type Dt struct {
	content string
}

func Ifc(ifc interface{})  {
	println("Ifc, &ifc:", &ifc)
}

func IfcPtr(ifc interface{})  {
	println("IfcPtr, ifc:", ifc.(*Dt))
}

func main() {
	dt := Dt{"wii"}
	println("main, &dt:", &dt)
	Ifc(dt)
	IfcPtr(&dt)
}
```

输出

```shell
main, &dt: 0xc000044758
Ifc, &ifc: 0xc000044748
IfcPtr, ifc: 0xc000044758
```

可以看出，interface{} 类型参数传递时，并不会把变量隐式转换为指针。

# 结构 & 成员函数

go 与其他语言定义结构（类）的方式不同。

```go
// 定义结构
type Data struct {
	name string   // 定义成员变量
}

// 定义成员函数
func (p *Data) Ptr() {
	println("ptr: ", p.name)
}

func (p Data) Cp() {
	println("cp: ", p.name)
}

// 使用
dt := Data{name: "wii"} // OR dt := Data{"wii"}
dt.Ptr()
```

# 接口

go 与其他语言定义接口的方式也不同。

```go
package main

import "fmt"

// Bird 定义接口
type Bird interface {
	Name() string
	Fly() bool
	Chirp() string
}

// Duck 定义接口实现
type Duck struct {
	nm string
	CanFly bool
	Sound string
}

// NewDuck 创建 Duck; go 中的类型，没有构造函数的概念，这里定义一个函数，用户创建对象并初始化
func NewDuck() *Duck {
	return &Duck{CanFly: false, Sound: "quack", nm: "Duck"}
}

// Name 定义接口函数实现
func (duck *Duck) Name() string  {
	return duck.nm
}

func (duck *Duck) Fly() bool {
	return duck.CanFly
}

func (duck *Duck) Chirp() string {
	return duck.Sound
}

// IF go 中没有三目运算符, 这个函数实现简单的三目运算
func IF(condition bool, tv interface{}, fv interface{}) interface{} {
	if condition {
		return tv
	} else {
		return fv
	}
}

func main() {
	var bird Bird = NewDuck()
	fmt.Printf("%v\n", IF(bird.Fly(), bird.Name() + " is flying!", bird.Name() + " cannot fly!"))
	println(bird.Name() + " is chirping:", bird.Chirp(), bird.Chirp(), "...")
}
```

可以看出，在接口是实现上，只要一个类定义了接口的所有方法，那么就可以把该对象的实例赋值给接口类型变量。

# 拷贝传递 & 指针传递

和 C++ 类似，go 也有拷贝传递和指针传递。首先来看一个示例。

```go
package main

type Data struct {
	name string
}

func (p *Data) Ptr() {
	println("ptr, p: ", p)
	println("ptr: ", p.name)
}

func (p Data) Cp() {
	println("cp, &p: ", &p)
	println("cp: ", p.name)
}

func Ptr(p *Data) {
	println("ptr, p: ", p)
	println("ptr: ", p.name)
}

func Cp(p Data) {
	println("cp, &p: ", &p)
	println("cp: ", p.name)
}

func main() {
	da := Data{name: "wii"}
	println("main, &da: ", &da)
  
	da.Ptr()
	(&da).Ptr()
	da.Cp()
	(&da).Cp()

	println("-----")

	Ptr(&da)
	// Ptr(da) // ERROR: Cannot use 'da' (type Data) as the type *Data
	Cp(da)
  // Cp(&da)    // ERROR: Cannot use '&da' (type *Data) as the type Data
}
```

输出。

```shell
main, &da:  0xc000044768
ptr, p:  0xc000044768
ptr:  wii
ptr, p:  0xc000044768
ptr:  wii
cp, &p:  0xc000044748
cp:  wii
cp, &p:  0xc000044738
cp:  wii
-----
ptr, p:  0xc000044768
ptr:  wii
cp, &p:  0xc000044758
cp:  wii
```

关注下面两个点

- 参数类型（指针和非指针）
- 成员函数和普通函数

首先，定义 Data 变量 da，内存地址为 `0xc000044768`。紧接着是四次调用，2（调用对象指针、非指针） * 2（参数指针、非指针）的组合；从这四次调用可以可以发现；对于**结构的成员函数**，调用对象的形式和参数形式无需匹配，实际效果以参数形式为准。如果成员函数参数为指针，则得到的是调用对象的指针形式（无论调用对象是否是指针形式）；同样的，如果成员函数参数为非指针形式，则得到的是调用对象的非指针形式（无论调用对象是否是非指针形式）；且，两种方式都可以编译通过。

其次，对于普通函数调用，严格区分参数是否为指针形式。比如，`Cp(&da)` 和 `Ptr(da)` 两种调用方式都无法通过编译。

最后，从变量的内存地址可以看出，拷贝传递会创建新的内存区域保存传递的参数。

接下来，再来看一个实例。

```go
// file: st.go; mod: "evaluate-go/pkg/st"
package st

type Cart struct {
	Price float64
	Count int
	Promo float64
}

func (r Cart) TotalPrice() float64 {
	return r.Price * float64(r.Count) * r.Promo
}

func (r *Cart) TotalPricePtr() float64 {
	return r.Price * float64(r.Count) * r.Promo
}

func (r Cart) Promotion(p float64) float64 {
	println("Promotion, &r: ", &r)
	r.Promo *= p
	return r.TotalPrice()
}

func (r *Cart) PromotionPtr(p float64) float64 {
	println("PromotionPtr, &r: ", r)
	r.Promo *= p
	return r.TotalPricePtr()
}
```

```go
// file: st.go; mod: "evaluate-go/cmd/st"
package main

import (
	"evaluate-go/pkg/st"
	"fmt"
)

func main() {
	ra := st.Cart{Price: 4, Count: 5, Promo: 1}
	fmt.Printf("%v\n", ra.TotalPrice())
	fmt.Printf("%v\n", ra.TotalPricePtr())
	fmt.Printf("%v\n", (&ra).TotalPricePtr())

	println("-----")
	fmt.Printf("%v\n", ra.Promotion(0.9))
	fmt.Printf("%v\n", ra.TotalPrice())
	fmt.Printf("%v\n", ra.TotalPricePtr())

	println("-----")
	rb := st.Cart{Price: 4, Count: 5, Promo: 1}
	fmt.Printf("%v\n", rb.PromotionPtr(0.9))
	fmt.Printf("%v\n", rb.TotalPrice())
	fmt.Printf("%v\n", rb.TotalPricePtr())
}
```

输出。

```shell
main, &ra:  0xc000092eb8
20
20
20
-----
Promotion, &r:  0xc000092ed0
18
20
20
-----
PromotionPtr, &r:  0xc000092ea0
18
18
18
```

这里需要注意的是，`ra.Promotion(0.9)` 这个调用，由于是拷贝传递，修改的 Promo 值，是临时变量的，而不是`ra` 的；这里可能会感到比较奇怪的是，调用了`ra.Promotion(0.9)` 来设置促销信息（Promo），但是计算总价时，设置的促销信息并未生效（`ra.TotalPrice()` 返回值仍是 20）；调用 `rb.PromotionPtr(0.9)` 设置促销信息之后，则符合预期。

# 整形 * 浮点

整形和浮点进行运算，需要显式转换类型。

```go
i := 10
f := 1.2
// println(i * f)     ERROR: Invalid operation: i * f (mismatched types int and float64)
println(float64(i) * f)
println(i * int(f))
```



