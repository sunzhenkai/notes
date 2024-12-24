---
title: GitHub
categories: 
  - [工具,GitHub]
tags:
  - GitHub
date: 2020/11/20 00:00:00
update: 2020/11/20 00:00:00
---

# 认证

在 Workflow 中可以使用 `${{ secrets.GITHUB_TOKEN }}` 获取 Access Token，详见[文档](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication)。

```shell
    steps:
      - name: '[talking-ground] checkout repository'
        uses: actions/checkout@v3
        with: 
          repository: "sunzhenkai/talking-ground"
          token: ${{ secrets.GITHUB_TOKEN }}
```

