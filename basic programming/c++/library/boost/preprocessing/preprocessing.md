---
title: boost - processing
categories: 
  - [coding, c++, library]
tags:
  - c++
date: "2021-11-22T00:00:00+08:00"
---

# Introduction

Boost Preprocessing Library 是 boost 定义的宏（macros）库，官方文档在[这里](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/)。

# Data Types

Boost 的 Preprocess 库有四种数据类型，array、lists、sequences、tuples。

## arrays

arrays 是包含两个元素的 tuple，第一个元素是 array 中元素的数量，第二个元素是包含 array 元素的 tuple。

### 定义

```c++
#define ARRAY (3, (a, b, c))
```

### 原语

- [BOOST_PP_ARRAY_DATA](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/array_data.html)
- [BOOST_PP_ARRAY_ELEM](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/array_elem.html)
- [BOOST_PP_ARRAY_SIZE](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/array_size.html)

## lists

lists 是一个有头和尾的简单列表。头是一个元素，尾是另外一个 list 或者 BOOST_PP_NIL。

### 定义

```c++
#define LISTS (a, (b, (c, BOOST_PP_NIL)))
```

### 原语

- [BOOST_PP_LIST_FIRST](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/list_first.html)
- [BOOST_PP_LIST_REST](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/list_rest.html)
- [BOOST_PP_NIL](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/nil.html)

## sequences

sequences 是一组相邻的带括号的元素。

### 定义

```c++
#define SEQ (0)(1)(2)(3)
```

### 原语

- [BOOST_PP_SEQ_ELEM](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/seq_elem.html)

## tuples

元组是一个括号内用逗号分隔的元素列表。

### 定义

```c++
#define TUPLE (a, b, c)
```

### 原语

- [BOOST_PP_TUPLE_ELEM](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/tuple_elem.html)

# Reference

## seq

### [BOOST_PP_SEQ_FOR_EACH](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/seq_for_each.html)

```c++
// 遍历 SEQ 中的每个元素，应用新的宏。
BOOST_PP_SEQ_FOR_EACH(macro, data, seq)
```

- macro
    - 形如 macro(r, data, elem) 的宏。BOOST_PP_SEQ_FOR_EACH 遍历每个元素并使用该宏展开。
    - 元素
        - r：当前元素的索引（从 1 开始）
        - data：辅助数据
        - elem：当前元素
- data: 辅助数据（可以不使用，使用 `_` 作为占位符）
- seq: 定义的序列

**示例**

```c++
#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#define SEQ (w)(x)(y)(z)
// cat
#define MACRO(r, data, elem) BOOST_PP_CAT(elem, data)
BOOST_PP_SEQ_FOR_EACH(MACRO, _, SEQ) // expands to w_ x_ y_ z_
// stringize
#define SIMPLE_SEQ (a)(b)(c)
#define MACRO(r, data, elem) BOOST_PP_STRINGIZE(r) BOOST_PP_STRINGIZE(data) BOOST_PP_STRINGIZE(elem)
    std::string v = BOOST_PP_SEQ_FOR_EACH(MACRO, _, SIMPLE_SEQ); // v: 1_a2_b3_c
#undef MACRO
```

## tuple



## string

### BOOST_PP_CAT

### BOOST_PP_STRINGIZE