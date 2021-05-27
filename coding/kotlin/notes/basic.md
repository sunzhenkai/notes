---
title: kotlin 基础
categories: 
	- [coding, kotlin, notes]
tags:
	- kotlin
date: 2021/01/09 19:00:00
update: 2021/01/09 19:00:00
---

# 安装

**homebrew**

```shell
$ brew install kotlin
```

**下载**

在[这里](https://github.com/JetBrains/kotlin)找最新的Release，贴一个[v1.4.21链接](https://github.com/JetBrains/kotlin/releases/tag/v1.4.21)。

**交互式终端**

```shell
$ kotlinc-jvm
```

 # HELLO WORLD

**code**

```kotlin
// file: hello.kt
fun main() {
    println("Hello Wrold!")
}
```

**compile**

```shell
$ kotlinc hello.kt -include-runtime -d hello.jar
```

**run**

```shell
$ java -jar hello.jar
```

# 组织

## 文件

kotlin 源文件通常以`.kt` 作为扩展名。

## 包

```kotlin
package base

import kotlin.text.*
```

# 数据类型

## 类型

### 数字

| 类型   | 长度 |
| ------ | ---- |
| Double | 64   |
| Float  | 32   |
| Long   | 64   |
| Int    | 32   |
| Short  | 16   |
| Byte   | 8    |

### 字符

| 类型   | 长度 |
| ------ | ---- |
| Char   | 字符 |
| String | -    |

### 布尔

| 类型    | 长度 |
| ------- | ---- |
| Boolean | -    |

## 限定

| 修饰符           | 意图                         | 目标           | 注意                        |
| ---------------- | ---------------------------- | -------------- | --------------------------- |
| var              | 变量                         | 属性           |                             |
| val              | 不可变量                     | 属性           |                             |
| companion object | 静态                         | -              |                             |
| final            | 不可继承，默认值             | 类、属性、方法 | 不可修饰局部变量            |
| open             | 开放继承权限                 | 类、属性、方法 | 不可修饰局部变量            |
| const            | 修饰可执行 **宏替换** 的常量 | 属性           | 只能修饰不可变量（val定义） |

**注：**

- 宏替换
  - **宏变量** 指编译时常量，**宏替换**指在编译阶段就会被**替换掉**
  - 宏替换条件
    - 使用 const 和 val 修饰的属性，如果进行拼接或者运算，被拼接的其他变量也要是宏变量
    - 位于顶层或者是对象表达式的成员
    - 初始值是基本数据类型
    - 没有自定义的getter方法

## 常量

```kotlin
// 10 进制 
1234567890
1234567890L
1_234_567_890

// 16 进制
0x0f
0xFF_EC_DE_5E

// 2 进制
0b00001011
```

## 定义

```kotlin
[final/open] [var/val] name : [Type] = ...
[final/open] [var/val] name : [Type]? = null
const val name : [Type][?] = ...

// example
var it : Int = 100
var ns : String? = null

object TestVars {
    const val name : String = ""
}
```

# 数据结构

## 数组

## 列表

## 集合

## 映射

# 语法

## 程序结构

## 注释

```kotlin
// 这是单行注释

/*
这是
多行注释
*/
```

## 条件控制

## 运算符

## 循环

## 判断

## 函数

```kotlin
fun [funName](arga: [Type], argb: [Type], ...) : [Type] {
  return ...
}

// example
fun sum(a: Int, b: Int): Int {
    return a + b
}

// no body
fun sum(a: Int, b: Int) = a + b

// return no meaning value
fun printSum(a: Int, b: Int): Unit {   	// Unit 可省略
    println("sum of $a and $b is ${a + b}")
}
```

## 类

# 特性

## 语法糖

## 空指针处理

## 函数式编程

## 泛型编程

# 参考

- https://kotlinlang.org/docs/reference/basic-syntax.html