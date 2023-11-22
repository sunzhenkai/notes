---
title: rapidjson - usage
categories: 
  - [coding, c++, library]
tags:
  - c++
  - rapidjson
date: 2023/11/21 21:00:00
---

# 加载

## 从字符串加载

```c++
#include "rapidjson/document.h"

// 加载 Object
rapidjson::Document doc;
doc.SetObject();
doc.Parse(data.c_str()); // data: std::string

// 加载 Array
rapidjson::Document arr;
arr.SetArray();
arr.Parse(data.c_str()); // data: std::string
```

# Type

```c++
kNullType = 0,      //!< null
kFalseType = 1,     //!< false
kTrueType = 2,      //!< true
kObjectType = 3,    //!< object
kArrayType = 4,     //!< array
kStringType = 5,    //!< string
kNumberType = 6     //!< number
```

# Object 

## 读

```c++
// 查找元素
auto it = doc.FindMember("field");
if (it == doc.MemberEnd()) ... // 判断是否存在
// 遍历元素
for (auto it = doc.MemberBegin(); it != doc.MemberEnd(); ++it) ...
```

# Array 

## 读

```c++
// 判断是否为空
arr.Empty();

// 遍历
for (auto it = arr.Begin(); it != arr.End(); ++it)
  
// 取第一个
auto e = arr.Begin();
e.GetObject(); // 作为 Object, e.GetObject().FindMember("field") 查找元素
e.GetString(); // 作为 String
```

# Value 

## 创建

```c++
// Object Value
rapidjson::Value v(rapidjson::kObjectType);
// Array Value
rapidjson::Value v(rapidjson::kArrayType);
// String Value
rapidjson::Value v("string_value");
// Number Value
rapidjson::Value v(1);
rapidjson::Value v(1.1);
```

