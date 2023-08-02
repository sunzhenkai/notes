---
title: Go 代码规范
categories: 
  - [coding, go]
tags:
  - go
date: 2021/03/01 00:00:00
update: 2021/03/01 00:00:00
---

# 命名

命名中的首字母大小写，大写指明可被外部访问，小写指明私有。对于 bool 类型，首字母应该为 `Has` 、`Is` 、`Can`、`Allow`。

## 结构体

- 驼峰，首字母根据访问控制选择大写、小写

## 变量

- 变量名尽量短
  - 局部变量，`c` 好于 `lineCount`，`i` 好于 `slliceIndex` 
  - 方法参数，一两个字母即可
  - 全局变量，需要更多的描述信息
- 如果使用长单词
  - 驼峰，首字母根据访问控制选择大写、小写

## 包名

- 包中所有名称引用都会使用包名，所以可以简化引用的名称，如使用 `chubby.File` 代替 `chubby.ChubbyFile` 

## 文件

- 小写单词
- 下划线 `_` 分隔

# 注释

## 包

```go
// Package math provides basic constants and mathematical functions.
package math

/*
Package template implements data-driven templates for generating textual
output such as HTML.
....
*/
package template
```

