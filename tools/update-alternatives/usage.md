---
wtitle: update-alternatives
categories: 
  - [工具,update-alternatives]
tags:
  - update-alternatives
date: 2020/12/30 00:00:00
update: 2020/12/30 00:00:00
---

# 安装

```shell
$ sudo pacman -S dpkg
```

# 示例

```shell
# 添加一个 alt
#                                  链接创建路径 名称   实际文件路径     优先级
sudo update-alternatives --install /usr/bin/cc cc /usr/bin/gcc-4.9 10  
```

```shell
sudo update-alternatives --config cc  # 选择并设置默认版本
```

