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
- homebrew

# 搜索包

- [base/extra package](https://archlinux.org/packages/)
- [aur](https://aur.archlinux.org/packages)

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
# manjaro
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

## AUR Helpers

AUR helpers 可以帮助我们搜索、下载、编译 AUR 包，常见的 AUR helpers 有 yay、paru等。

## Yay

```shell
sudo pacman -S --needed git base-devel
cd /tmp
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```

## Paru

### 安装

```shell
$ sudo pacman -S --needed base-devel
$ git clone https://aur.archlinux.org/paru.git
$ cd paru
$ makepkg -si
```

### 使用示例

```shell
# 搜索
$ paru -Ss gcc7
```

```shell
paru <target> -- Interactively search and install <target>.
paru -- Alias for paru -Syu.
paru -S <target> -- Install a specific package.
paru -Sua -- Upgrade AUR packages.
paru -Qua -- Print available AUR updates.
paru -G <target> -- Download the PKGBUILD and related files of <target>.
paru -Gp <target> -- Print the PKGBUILD of <target>.
paru -Gc <target> -- Print the AUR comments of <target>.
paru --gendb -- Generate the devel database for tracking *-git packages. This is only needed when you initially start using paru.
paru -Bi . -- Build and install a PKGBUILD in the current directory.
```

## 其他

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
> pamac build pkgp
>
> 安装官方包
>
> pamac install pkg 

# Hyprland

```shell
sudo pacman -S hyprland 
# yay -S hyprland-git

# tools
## mako 通知
## xdg-desktop-portal-hyprland 通讯
## dolphin 文件管理器
## sddm 桌面显示管理器
## pipewire、wireplumber 屏幕共享 
## waybar 状态栏
## hyprpaper 设置壁纸
## brightnessctl 调整亮度
## playerctl 播放控制
## network-manager-applet 网络图形界面
## polkit-kde-agent 权限认证界面
## wl-clipboard	粘贴板
sudo pacman -S sddm dolphin mako pipewire wireplumber xdg-desktop-portal-hyprland waybar hyprpaper brightnessctl playerctl network-manager-applet polkit-kde-agent firefox wl-clipboard	uwsm
yay -S cliphist wl-clip-persist eww

# start tools
sudo systemctl enable --now sddm.service

# fonts
sudo pacman -S ttf-dejavu ttf-liberation noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-droid ttf-opensans ttf-fira-code ttf-font-awesome
```

