---

---

# gflags

[官方文档](https://gflags.github.io/gflags/)。

```cmake
# 查找、链接库
set(gflags_DIR <prefix>/lib/cmake/gflags) # 安装在非系统默认路径需要设置
find_package(gflags REQUIRED)
target_link_libraries(<target> gflags::gflags)
```

