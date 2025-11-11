---
title: Poetry
categories: 
  - [tools, Poetry]
tags:
  - Poetry
date: "2025-08-26T19:00:00+08:00"
update: "2025-08-26T19:00:00+08:00"
---

# 说明

Poetry 用于管理 Python 项目信息及依赖。

# 安装

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

# Workflow

## 初始化

```shell
poetry init
```

# Run

```shell
poetry run python ...
```

# Activate

```shell
poetry env activate
```

# 导出依赖项

最新版的 poetry 默认没有 export 命令了，需要安装插件。

```shell
poetry self add poetry-plugin-export
```

导出。

```shell
poetry export --without-hashes > requirements.txt
```

