---
title: manjaro usage
categories: 
	- [linux,distro,manjaro]
tags:
	- distro
date: 2023/06/20 00:00:00
---

# 包管理工具

- pacman / pamac (GUI)
- AUR
- snap
- flatpak

# 初始化

```shell
# 安装并启用 sshd.service
$ sudo pacman install openssl openssh
$ sudo systemctl enable sshd.service
$ sudo systemctl start sshd.service
```

# pacman

## 查看帮助

```shell
$ pacman -h
$ pacman -S -h
```

## 切换源

```shell
# 1. 刷新
$ sudo pacman-mirrors -i -c China -m rank
# 选择合适的源
# 2. 更新
$ sudo pacman -Syy
```

或选择最近源。

```shell
$ sudo pacman-mirrors --geoip && sudo pacman -Syyu
```

## 参数

```shell
# -S
-S 安装
-S --needed --noconfirm
--needed: 跳过已经安装到最新版本的包
--noconfirm: 跳过确认

-R 卸载
```

## 查看安装的包

```shell
# 所有安装的包
$ pacman -Q
# 查询指定包
$ pacman -Q vim
```

## 搜索包

```shell
$ pacman -Ss vim
```

# AUR

AUR（Arch User Repository）。

## 使用

可以手动[搜索包](https://aur.archlinux.org/packages)，然后使用 git clone，并使用命令 `makepkg  -s` 编译，使用命令 `makepkg -i` 安装，或直接使用 `makepkg -is` 命令编译安装。也可以通过 pamac 命令使用 aur。 

```shell
# 安装 pamac
$ pacman -S pamac-cli
# 搜索 aur 包
$ pamac search ttf-ms-fonts --aur
# 安装
$ pamac build ttf-ms-fonts 
```

> 安装 AUR 包
>
> pamac build pkg
>
> 安装官方包
>
> pamac install pkg 
