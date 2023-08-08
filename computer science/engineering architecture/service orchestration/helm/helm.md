---
title: helm
categories: 
  - 架构
  - container
  - k8s
  - helm
tags:
  - k8s
  - helm
date: 2022/09/07 00:00:00
---

# 安装

```shell
# brew
brew install helm

# snap
sudo snap install helm --classic

# microk8s
microk8s enable helm3
## 使用
microk8s helm3 ...

# arch
sudo pamac install helm
```

# 概念

Helm 可以安装 Charts 到 k8s 集群中，为每次安装创建新的 Release。为了获取新的 Charts，可以搜索 Helm Charts Repositories。

## Chart

在 Helm 中，Chart 是一个集合，包含所有必要的的资源定义来运行一个应用、工具或者 k8s 集群中的服务。

## Repository

Repository 是 Charts 收集和分享的地方。

## Release

Release 是 Chart 运行在 k8s 集群中的实例。一个 Chart 可以在相同的集群被安装多次，每次安装都会创建一个新的 Release。

# 使用

## Repo

```shell
# 添加
helm repo add <name> <url>

# 查看 repo 下的 charts
helm search repo <repo-name>

# 更新 repo
helm repo update <repo-name>

# 列出添加的 repo
helm repo list

# 移除 repo
helm repo remove <repo-name>

# 打包 repo
helm package <relative-path-to-chart>

# 生成 index
helm repo index
```

## Chart

```shell
# 搜索
helm search repo <repo-name> # 在添加的 repo 中搜索
helm search hub <repo-name> # 在 hub 中搜索

# 安装一个 Chart
helm install <chart> --generate-name
helm install <release-name> <chart>

# 列出安装的 chart
helm list # 或 helm ls

# 写在一个 chart
helm uninstall <release-name>

# 查看一个 helm 的状态
helm status <release-name>
```

### Values

```shell
# 查看 chart values
helm show values bitnami/wordpress
# 查看 release values
helm show values <release-name>

# 覆盖 values (使用文件)
echo '{mariadb.auth.database: user0db, mariadb.auth.username: user0}' > values.yaml
helm install -f values.yaml bitnami/wordpress --generate-name
# 覆盖 values (使用命令行参数)
helm install --set mariadb.auth.database=user0db,sample.list={1,2,3},sample.empty.list=[] bitnami/wordpress --generate-name
```

## 升级与回滚

### 升级

```shell
echo "mariadb.auth.username: user1" > panda.yaml
helm upgrade -f panda.yaml <release-name> <chart> 

# 示例
helm upgrade -f panda.yaml happy-panda bitnami/wordpress
```

### 回滚

```shell
helm rollback <release-name> <REVISION> --timeout <timeout> --wait

# 查看 revision
helm history <release-name>
```

## 模板

```shell
# 查看生成 Manifest
helm template --debug <relative-path-to-chart>
```

# ArtifactHUB

[helm artifact hub](https://artifacthub.io/packages/search?kind=0)
