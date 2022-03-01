---
title: c++ - holes
categories: 
	- [coding, c++]
tags:
	- c++
date: 2022/02/09 00:00:00
---

# 模板

- 模板类的定义和实现不能分隔
  - https://stackoverflow.com/questions/115703/storing-c-template-function-definitions-in-a-cpp-file
  - https://isocpp.org/wiki/faq/templates#templates-defn-vs-decl
  - https://isocpp.org/wiki/faq/templates#separate-template-class-defn-from-decl

> 类似需要在编译期展开的代码实现，不能放在 cpp 文件中，而应该放在 header 中