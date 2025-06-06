---
title: on my zsh - install
categories: 
  - [工具,zsh]
tags:
  - zsh
date: "2021-05-10T00:00:00+08:00"
update: "2021-05-10T00:00:00+08:00"
---

# Install

```shell
$ sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

# Config

```shell
$ chsh -s /bin/zsh
$ chsh -s /bin/bash
```

# Plugins

```shell
$ pip install powerline-status --user
```

**Install**

```shell
$ cd ~/.oh-my-zsh/custom/plugins/
$ git clone <plugin-repo>
$ vim ~/.zshrc
```

**高亮**

```shell
$ cd ~/.oh-my-zsh/custom/plugins/
$ git clone https://github.com/zsh-users/zsh-syntax-highlighting.git
$ vim ~/.zshrc
```

**补全**

```shell
$ cd ~/.oh-my-zsh/custom/plugins/
$ git clone https://github.com/zsh-users/zsh-autosuggestions
$ vim ~/.zshrc

plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
    )
```

