---
title: Neovim
categories: 
  - [tools,Neovim]
tags:
  - tools
  - Neovim
date: 2020/11/13 22:00:00
update: 2020/11/13 22:00:00
---

# 配置

使用 [LazyVim](https://github.com/LazyVim/LazyVim) 进行配置。

```shell
git clone https://github.com/LazyVim/starter ~/.config/nvim
```

## 安装字体（可选）

如果是通过 ssh 远程登录，需要在本地机器安装，并设置 terminal font。

```shell
wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/JetBrainsMono.zip
unzip JetBrainsMono.zip -d ~/.local/share/fonts
```

ubuntu

```shell
sudo apt install fontconfig
fc-cache -fv
```

# 概念

## Buffer

NeoVim 以 Buffer List 的方式管理打开的文件，每个打开的文件是一个 Buffer，并且有唯一的 id（`:ls` 可查看打开的文件列表及 id）。

# 快捷键

## LazyVim

```shell
<space>e      # 打开 NeoTree
```

## Buffer

```shell
bd            # 删除当前 buffer
bn            # 下一个 buffer
bn{number}    # 下面的第 {number} 个
bp            # 前一个
bp{number}    # 前面的第 {number} 个
b#            # 切换到最近激活的 buffer
ls						# 列出所有 buffer
```

## NeoTree

```shell
?							# 打开帮助框
a							# 添加文件/文件夹，添加文件夹则以 '/' 结尾，否则添加文件
H							# 显式/折叠隐藏文件
.							# 设置选定的目录为 root dir
```

# 使用

## 多行编辑

```shell
<ctrl>-v    # 开启矩阵选择
```



# 插件

# 常见问题

## 图标显示异常

修改 terminal font，以 iterm2 为例。字体可从 [nerd fonts](https://www.nerdfonts.com/font-downloads) 下载。

![image-20240922102745830](./usage/image-20240922102745830.png)
