---
title: on my zsh - usage
categories: 
  - 工具
  - zsh
tags:
  - zsh
date: "2025-05-28T00:00:00+08:00"
update: "2025-05-28T00:00:00+08:00"
---

# Zsh Usage

## 行编辑快捷键

> **平台差异说明**
>
> | 键位                  | macOS                                    | Linux / Windows             |
> | --------------------- | ---------------------------------------- | --------------------------- |
> | `Meta` 修饰键         | `⌥ Option`（需终端配置）或 `Esc` 前缀模式 | `Alt` 直接使用              |
> | `Esc` 前缀模式        | 先按 `Esc`，松开后再按下一个键           | 同样可用，但 `Alt` 更直接   |
>
> macOS 终端配置：iTerm2 → Preferences → Profiles → Keys → Left Option Key 设为 `Esc+`

### 光标移动

| macOS                          | Linux / Windows    | 功能                     |
| ------------------------------ | ------------------ | ------------------------ |
| `Ctrl + A`                     | `Ctrl + A`         | 移动到行首               |
| `Ctrl + E`                     | `Ctrl + E`         | 移动到行尾               |
| `⌥ + B` / `Esc` 再按 `B`      | `Alt + B`          | 向左跳一个词              |
| `⌥ + F` / `Esc` 再按 `F`      | `Alt + F`          | 向右跳一个词              |
| `Ctrl + B`                     | `Ctrl + B`         | 左移一个字符（等同 ←）    |
| `Ctrl + F`                     | `Ctrl + F`         | 右移一个字符（等同 →）    |

### 删除与编辑

| macOS                          | Linux / Windows    | 功能                       |
| ------------------------------ | ------------------ | -------------------------- |
| `Ctrl + W`                     | `Ctrl + W`         | 删除光标前一个词           |
| `⌥ + D` / `Esc` 再按 `D`      | `Alt + D`          | 删除光标后一个词           |
| `Ctrl + U`                     | `Ctrl + U`         | 删除光标前所有内容（整行） |
| `Ctrl + K`                     | `Ctrl + K`         | 删除光标后所有内容         |
| `Ctrl + H`                     | `Ctrl + H`         | 删除前一个字符（等同 ⌫）   |
| `Ctrl + D`                     | `Ctrl + D`         | 删除当前字符 / 发送 EOF    |
| `Ctrl + Y`                     | `Ctrl + Y`         | 粘贴上次删除的内容         |

### 历史 & 操作

| macOS                          | Linux / Windows    | 功能                         |
| ------------------------------ | ------------------ | ---------------------------- |
| `Ctrl + R`                     | `Ctrl + R`         | 反向搜索历史命令             |
| `Ctrl + P`                     | `Ctrl + P`         | 上一条历史（等同 ↑）         |
| `Ctrl + N`                     | `Ctrl + N`         | 下一条历史（等同 ↓）         |
| `Ctrl + L`                     | `Ctrl + L`         | 清屏                         |
| `Ctrl + C`                     | `Ctrl + C`         | 中断当前命令                 |
| `Ctrl + Z`                     | `Ctrl + Z`         | 挂起当前命令（`fg` 恢复）    |
| `Ctrl + T`                     | `Ctrl + T`         | 交换光标处两个字符位置       |
| `⌥ + .` / `Esc` 再按 `.`      | `Alt + .`          | 插入上一条命令的最后一个参数 |

### 历史扩展（跨平台通用）

| 语法         | 含义                                | 示例                             |
| ------------ | ----------------------------------- | -------------------------------- |
| `!!`         | 上一条完整命令                      | `sudo !!`                        |
| `!$`         | 上一条命令最后一个参数              | `mkdir foo && cd !$`             |
| `!*`         | 上一条命令所有参数                  |                                  |
| `!^`         | 上一条命令第一个参数                |                                  |
| `!?pattern?` | 最近一条包含 pattern 的命令         |                                  |
| `!n`         | 第 n 条历史命令                     |                                  |
| `!-n`        | 倒数第 n 条历史命令                 |                                  |

## Tab 补全

| 操作             | 功能                     |
| ---------------- | ------------------------ |
| `Tab`            | 补全命令 / 路径           |
| `Tab` `Tab`      | 列出所有补全选项          |
| `Ctrl + I`       | 等同 Tab                  |

## 历史扩展

| 语法         | 含义                                | 示例                             |
| ------------ | ----------------------------------- | -------------------------------- |
| `!!`         | 上一条完整命令                      | `sudo !!`                        |
| `!$`         | 上一条命令最后一个参数              | `mkdir foo && cd !$`             |
| `!*`         | 上一条命令所有参数                  |                                  |
| `!^`         | 上一条命令第一个参数                |                                  |
| `!?pattern?` | 最近一条包含 pattern 的命令         |                                  |
| `!n`         | 第 n 条历史命令                     |                                  |
| `!-n`        | 倒数第 n 条历史命令                 |                                  |

## 通配符 (Globbing)

| 模式          | 含义                       |
| ------------- | -------------------------- |
| `*`           | 任意字符串                  |
| `?`           | 任意单个字符                |
| `[abc]`       | 匹配 a、b、c 之一          |
| `[0-9]`       | 匹配数字范围                |
| `**/`         | 递归匹配子目录              |
| `^pattern`    | 排除匹配（需 `setopt EXTENDED_GLOB`）|
| `(pattern)`   | 分组                        |

## Oh-My-Zsh 常用别名

### Git 插件别名（默认启用）

| 别名            | 命令                             |
| --------------- | -------------------------------- |
| `gs`            | `git status`                     |
| `ga`            | `git add`                        |
| `gaa`           | `git add --all`                  |
| `gc`            | `git commit -v`                  |
| `gc!`           | `git commit -v --amend`          |
| `gco`           | `git checkout`                   |
| `gcb`           | `git checkout -b`                |
| `gb`            | `git branch`                     |
| `gba`           | `git branch -a`                  |
| `gd`            | `git diff`                       |
| `gds`           | `git diff --staged`              |
| `gl`            | `git pull`                       |
| `gp`            | `git push`                       |
| `glog`          | `git log --oneline --decorate`   |
| `gst`           | `git status`                     |

### 目录跳转别名

| 别名            | 命令                             |
| --------------- | -------------------------------- |
| `..`            | `cd ..`                          |
| `...`           | `cd ../..`                       |
| `....`          | `cd ../../..`                    |
| `-`             | `cd -`（返回上一个目录）          |

## 常用技巧

### 重定向

```shell
$ command > file        # stdout 写入文件（覆盖）
$ command >> file       # stdout 追加到文件
$ command 2> file       # stderr 写入文件
$ command &> file       # stdout + stderr 写入文件
$ command 2>&1          # stderr 重定向到 stdout
```

### 进程管理

```shell
$ command &             # 后台运行
$ jobs                  # 查看后台任务
$ fg %1                 # 将任务 1 调到前台
$ bg %1                 # 将任务 1 放到后台
$ kill %1               # 终止任务 1
$ disown %1             # 使任务脱离终端
```

### 变量与扩展

```shell
$ export VAR=value      # 设置环境变量
$ echo $VAR             # 读取变量
$ unset VAR             # 删除变量
$ echo ${VAR:-default}  # 变量未设置时使用默认值
$ echo ${#VAR}          # 变量长度
```

### 子字符串

```shell
$ str="hello world"
$ echo ${str:0:5}       # => "hello"（从位置 0 取 5 个字符）
$ echo ${str/world/zsh} # => "hello zsh"（替换）
$ echo ${str/h/H}       # => "Hello world"（首处替换）
$ echo ${str//l/L}      # => "heLLo worLd"（全局替换）
```
