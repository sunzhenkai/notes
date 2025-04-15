---
title: fswatch
categories: 
  - [工具,fswatch]
tags:
  - emacs
date: 2022/09/17 00:00:00
---

# 参数

```shell
fswatch -e ".*" -i '.*\.md$' . | xargs -I {} echo {}
```

**注意**

- 默认包含所有文件，如果只配置 `-i` 是没有任何效果的，必须配合 `-e` ，比如 `-e '.*'` 屏蔽所有，在 `-i '.*md$'` 包含 md 结尾文件

```shell
fswatch -e ".*" -i '.*\.md$'  . | xargs -I {} mmdc -e png -i {}
```

