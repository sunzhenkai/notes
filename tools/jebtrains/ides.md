---
title: Jetbrains
categories: 
  - [tools, jetbrains]
tags:
  - jetbrains
date: 2021/3/3 00:00:00
update: 2021/3/3 00:00:00
---

# 替换

**正则**

```java
// 将 :***.*** 替换为 ${***.***}
:([\w.]+*)  // 匹配
#{$1}				// 替换，选取分组
```

