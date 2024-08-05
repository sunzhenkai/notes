---
title: helm - usage
categories: 
  - k8s
  - helm
tags:
  - k8s
  - helm
date: 2024/08/05 00:00:00
---

# local git repo

## 目录结构

```shell
$ tree
.
├── ace
│   ├── nginx
│   │   ├── Chart.yaml
│   │   ├── configmap
│   │   │   └── sources.list
│   │   ├── templates
│   │   │   ├── configmap.yaml
│   │   │   ├── deployment.yaml
│   │   │   ├── _helpers.tpl
│   │   │   └── service.yaml
│   │   └── values.yaml
│   └── ...
├── Makefile
└── README.md
```

## 安装 Chart

```shell
$ helm install ace ace/nginx
NAME: ace
LAST DEPLOYED: Mon Aug  5 13:42:17 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

## 更新 Chart

```shell
$ helm upgrade ace ace/nginx
Release "ace" has been upgraded. Happy Helming!
NAME: ace
LAST DEPLOYED: Mon Aug  5 13:47:34 2024
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
```

## 示例

```shell
$ helm upgrade --install {release-name} {chart-path} \
	--create-namespace -n ${kubeNamespace} 
	-f {path-to-helm-values-file} \
  --set app.tag={tag-value} \
  --kube-context {kube-context} \
  --kubeconfig {path-to-kube-config-file}
```

**解释**

- `--install` ：更新 release，如果不存在则安装
- `--create-namespace`：如果 namespace 不存在，则创建，和 `--install` 配合使用
- `--set app.tag` ：指定 Value `app.tag` 的值
