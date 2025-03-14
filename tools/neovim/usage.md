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

# 编辑

## 跳转

```shell
gd    # 跳转到上一个编辑的位置，可跨文件
%     # 跳转到成对符号的另一侧, 比如 {}, [], ()
[{    # 跳转到代码块的开始位置
}]    # 跳转到代码块的结束位置
```

## 移动

```shell
Ctrl+[,j/k # Ctrl+[ 后快速按 j/k 键可以移动当前行上移/下移一行，注意必须要快；此外 Ctrl+[ 后会进入 command 模式
```

# 快捷键

## LazyVim

```shell
<space>-e      # 打开 NeoTree
<ctrl>-o       # 上一个编辑的位置
<ctrl>-i       # 下一个编辑的位置，<ctrl>-o 的逆操作
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

## 无法复制到系统粘贴板

场景是，登录到远程机器，并使用 nvim 编译，无法复制选中的文本，解决方案是使用快捷键，下面是 Max OS 下的快捷键操作，Windows/Linux 下可尝试探索。

```shell
<option + 拖动鼠标> : 选中连续文本，可跨行
<option + command + 拖动鼠标> : 选中矩形区域，可跨行
```

选中后，再按系统的复制快捷键即可（或右键弹出菜单、选择复制）。

## FZF 搜索窗口无法复制寄存器内容

核心思想是针对 fzf 窗口，自定义快捷键，调用 `getreg()` 来获取寄存器内容，搜索到使用 `getreg(nr2char(getchar()))` 命令，但是不行。在 `init.lua` 文件中添加任意一个方案的内容，在搜索时使用快捷键 `Ctrl + V` 即可粘贴寄存器内容。

方案一，使用 nvim 的 lua  api 命令创建。

```lua
local autogrp = vim.api.nvim_create_augroup("FZF", { clear = true })
vim.api.nvim_create_autocmd("FileType", {
	pattern = "fzf",
	group = autogrp,
	callback = function()
		vim.api.nvim_set_keymap("t", "<C-r>", "getreg()", { noremap = true, expr = true, silent = true })
	end,
})
```

方案二，使用 `vim.cmd`。

```lua
vim.cmd([[
  autocmd! FileType fzf tnoremap <expr> <C-r> getreg()
]])
```

# Lazy.nvim

## Mason

- mason 仅安装 LSP Server，最终还是要使用 lspconfig 插件来完成 LSP

### 唤出

```shell
:Mason
```

![image-20241227184840062](usage/image-20241227184840062.png)

![image-20241227184849311](usage/image-20241227184849311.png)

修改 Mason 配置后，可手动唤出 Mason 面板安装。

## 分屏

```shell
<space> -> <shift> + \ : 水平分屏
<space> -> - : 垂直分屏
```

切换分屏。

```shell
<ctrl> + H/左 : 左
<ctrl> + L/右 : 右
<ctrl> + J/下 : 下
<ctrl> + K/上 : 上
```

# 拷贝到系统剪贴板

```shell
:"+y
```

**Iterm2 额外配置**

![image-20250314132955546](/Users/wii/workspace/public/notes/tools/neovim/usage/image-20250314132955546.png)
