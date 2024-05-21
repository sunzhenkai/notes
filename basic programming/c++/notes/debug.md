---
title: c++ debug
categories: 
  - [coding, c++]
tags:
  - c++
date: 2021/03/11 00:00:00
update: 2021/03/11 00:00:00
---

# addr2line

```shell
addr2line -f -e path/to/binary <address>
```

# nm

列出对象文件中的符号

```shell
nm libssl.a 
nm -an libssl.a 
```

