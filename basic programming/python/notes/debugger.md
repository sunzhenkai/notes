---
title: python debugger
categories: 
  - [python, notes]
tags:
  - python
date: "2021-10-02T00:00:00+08:00"
update: "2021-10-02T00:00:00+08:00"
---

# 调试

# gdb

```shell
$ export PYTHONPATH=/path/to/python/lib/python3.6/site-packages/Cython/Debugger:$PYTHONPATH
$ gdb /path/to/python <pid>
(gdb) python import libpython
(gdb) py-bt
```

# 参考

- [gdb 调试手册](https://devguide.python.org/gdb/)
- https://blog.csdn.net/github_40094105/article/details/81287572
- https://www.codenong.com/52258378/
- https://www.cnblogs.com/sting2me/p/7745551.html

