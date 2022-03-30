---
title: mongo - cxx driver
categories: 
	- [架构, 存储, mongodb]
tags:
	- mongodb
date: 2022/3/23 00:00:00
update: 2022/3/23 00:00:00
---

# 安装

```shell
# brew
brew insall mongo-cxx-deriver
```

其他参考[这里](http://mongocxx.org/mongocxx-v3/installation/)。

# 示例

官方示例参考[这里](https://github.com/mongodb/mongo-cxx-driver/tree/master/examples)。

## 连接数据库

```shell
mongocxx::instance instance{};
mongocxx::uri uri("mongodb://192.168.4.13:27017");
mongocxx::client client(uri);
```

## 读取数组

```c++
auto arr_element = doc["contribs"];
if (arr_element && arr_element.type() == bsoncxx::type::k_array) {
    bsoncxx::array::view arr(arr_element.get_array().value);
    std::cout << arr.length() << std::endl; // 67; not count of elements
    for (auto e: arr) {
        std::cout << "E " << e.get_utf8().value.to_string() << std::endl;
    }
}
```

