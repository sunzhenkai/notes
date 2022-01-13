---
title: boost - processing
categories: 
	- [coding, c++, library]
tags:
	- c++
date: 2021/11/22 00:00:00
---

# Introduction

Boost Preprocessing Library 是 boost 定义的宏（macros）库。

# Data Types

## arrays

### 定义

```c++
#define ARRAY (3, (x, y, z))
```

### 原语

- [BOOST_PP_ARRAY_DATA](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/array_data.html)
- [BOOST_PP_ARRAY_ELEM](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/array_elem.html)
- [BOOST_PP_ARRAY_SIZE](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/array_size.html)

## lists

### 定义

```c++
#define OLD \
   BOOST_PP_LIST_CONS( \
      a, \
      BOOST_PP_LIST_CONS( \
         b, \
         BOOST_PP_LIST_CONS( \
            c, \
            BOOST_PP_LIST_NIL \
         ) \
      ) \
   ) \
   /**/

#define NEW (a, (b, (c, BOOST_PP_NIL)))
```

### 原语

- [BOOST_PP_LIST_FIRST](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/list_first.html)
- [BOOST_PP_LIST_REST](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/list_rest.html)
- [BOOST_PP_NIL](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/nil.html)

## sequences

### 定义

```c++
BOOST_PP_SEQ_ELEM(1, (a)(b)(c)) // expands to b

#define SEQ \
   (0)(1)(2)(3)(4)(5)(6)(7)(8)(9) \
   (10)(11)(12)(13)(14)(15)(16)(17)(18)(19) \
   (20)(21)(22)(23)(24)(25)(26)(27)(28)(29) \
   (30)(31)(32)(33)(34)(35)(36)(37)(38)(39) \
   (40)(41)(42)(43)(44)(45)(46)(47)(48)(49) \
   (50)(51)(52)(53)(54)(55)(56)(57)(58)(59) \
   (60)(61)(62)(63)(64)(65)(66)(67)(68)(69) \
   (70)(71)(72)(73)(74)(75)(76)(77)(78)(79) \
   (80)(81)(82)(83)(84)(85)(86)(87)(88)(89) \
   (90)(91)(92)(93)(94)(95)(96)(97)(98)(99) \
   /**/

BOOST_PP_SEQ_ELEM(88, SEQ) // expands to 88
```

### 原语

- [BOOST_PP_SEQ_ELEM](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/seq_elem.html)

## tuples

### 定义

```c++
#define TUPLE (a, b, c, d)
```

### 原语

- [BOOST_PP_TUPLE_ELEM](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/tuple_elem.html)

# Reference

## SEQ

### [BOOST_PP_SEQ_FOR_EACH](https://www.boost.org/doc/libs/1_71_0/libs/preprocessor/doc/ref/seq_for_each.html)

```c++
BOOST_PP_SEQ_FOR_EACH(macro, data, seq)
```

遍历 SEQ 中的每个元素，应用新的宏。

## STRING

### BOOST_PP_CAT

### BOOST_PP_STRINGIZE