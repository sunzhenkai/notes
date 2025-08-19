---
title: Jupyter
categories: 
  - [tools, Jupyter]
tags:
  - Jupyter
date: "2025-08-19T00:00:00+08:00"
update: "2025-08-19T00:00:00+08:00"
---

# 部署

Jupyter 的镜像定义在[这里](https://github.com/jupyter/docker-stacks?tab=readme-ov-file)，Docker Hub 中的 [Jupyter 组织](https://hub.docker.com/u/jupyter)下镜像不再更新。

关于镜像选择，all-spark-notebook 基于 pyspark-notebook 构建。

## Docker Compose 部署

```yaml
version: "3.9"

services:
  jupyter:
    image: quay.io/jupyter/all-spark-notebook:latest
    container_name: jupyterlab
    restart: unless-stopped
    ports:
      - "8888:8888"
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - JUPYTER_TOKEN=jupyter
    volumes:
      - jupyter-data:/home/jovyan/work
volumes:
  jupyter-data:
```

**ROOT 权限**

```shell
$ docker exec -it -u root jupyterlab bash # root 用户登录容器，可以在 root 下赋予 jovyan 管理员权限
```

