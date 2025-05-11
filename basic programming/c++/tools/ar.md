---
title: ar
categories: 
  - [coding, c++, tools]
tags:
  - c++
  - ar
date: "2024-06-14T00:00:00+08:00"
update: "2024-06-14T00:00:00+08:00"
---

# 打包多个静态库

```shell
# liba.a, libb.a
$ mkdir objects_a && cd objects_a && ar -x ../liba.a && cd ..
$ mkdir objects_b && cd objects_b && ar -x ../libb.a && cd ..
$ ar crs libc.a objects_a/*.o objects_b/*.o 
```

