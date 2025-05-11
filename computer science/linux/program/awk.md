---
title: awk
categories: 
  - [linux,程序]
tags:
  - awk
date: "2021-01-27T00:00:00+08:00"
update: "2021-01-27T00:00:00+08:00"
---

# 说明

- 默认按空白符分隔（`\s+`），多个连续空白符不切分

- 列数从 1 开始

# 打印

```shell
# 打印
ls -l | awk '{print $5}'   # 打印第 5 列
```

# 统计

```shell
# 统计大小
ls -l | awk '{sum+=$5}END{print sum/1024/1024"MB"}'
```

