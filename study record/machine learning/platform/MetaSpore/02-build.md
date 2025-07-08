---
title: MetaSpore - 构建
categories: 
    - [研习录, 机器学习]
tags:
    - 机器学习
date: "2025-06-11T00:00:00+08:00"
---

# 步骤

- 构建基础镜像（dev / compile 镜像）
- 训练
  - 构建 Training Build 镜像（打包 MetaSpore Wheel 安装包）
  - 构建 Training Build Release 镜像（训练镜像，包含 Spark 等依赖）
- 开发
  - 构建 Jupyter 镜像
  - 构建 Code Server 镜像
- 在线 Serving
  - 构建 Serving Build 镜像（基于 dev 镜像）
  - 构建 Serving Release 镜像（Release 版本的可发布镜像，基于 ubuntu 镜像，安装必要依赖、拷贝 Release 版本二进制文件）

# 构建

在 Fork 的代码库中新增了 [Makefile](https://github.com/sunzhenkai/MetaSpore/blob/main/Makefile) 用于方便地构建目标、镜像。

```shell
.PHONY: dev training serving jupyter code-server all

REPOSITORY := sunzhenkai
VERSION := 0.0.1
RUNTIME := cpu
FIX_ARG := --network host --build-arg RUNTIME=$(RUNTIME) --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy}
DOCKER_CMD := DOCKER_BUILDKIT=1 docker build $(FIX_ARG)

DEV_IMAGE := $(REPOSITORY)/metaspore-dev-$(RUNTIME):$(VERSION)
TRAINING_BUILD_IMAGE := $(REPOSITORY)/metaspore-training-build:$(VERSION)
TRAINING_RELEASE_IMAGE := $(REPOSITORY)/metaspore-training-release:$(VERSION)
SERVING_BUILD_IMAGE := $(REPOSITORY)/metaspore-serving-build:$(VERSION)
SERVING_RELEASE_IMAGE := $(REPOSITORY)/metaspore-serving-release:$(VERSION)
JUPYTER_IMAGE := $(REPOSITORY)/metaspore-training-jupyter:$(VERSION)
CODESERVER_IMAGE := $(REPOSITORY)/metaspore-codeserver:$(VERSION)

dev:
	@$(DOCKER_CMD) $(FIX_ARG) -f docker/ubuntu20.04/Dockerfile_dev -t $(DEV_IMAGE) .

training: dev
	@DOCKER_BUILDKIT=1 docker build $(FIX_ARG) -f docker/ubuntu20.04/Dockerfile_training_build --build-arg DEV_IMAGE=$(DEV_IMAGE) -t $(TRAINING_BUILD_IMAGE) .
	@DOCKER_BUILDKIT=1 docker build $(FIX_ARG) -f docker/ubuntu20.04/Dockerfile_training_release --build-arg METASPORE_RELEASE=build --build-arg METASPORE_BUILD_IMAGE=$(TRAINING_BUILD_IMAGE) -t $(TRAINING_RELEASE_IMAGE) --target release .

serving: dev
	@DOCKER_BUILDKIT=1 docker build $(FIX_ARG) -f docker/ubuntu20.04/Dockerfile_serving_build --build-arg DEV_IMAGE=$(DEV_IMAGE) -t $(SERVING_BUILD_IMAGE) .
	@DOCKER_BUILDKIT=1 docker build $(FIX_ARG) -f docker/ubuntu20.04/Dockerfile_serving_release --build-arg BUILD_IMAGE=$(SERVING_BUILD_IMAGE) -t $(SERVING_RELEASE_IMAGE) --target serving_release .

jupyter:
	@DOCKER_BUILDKIT=1 docker build $(FIX_ARG) -f docker/ubuntu20.04/Dockerfile_jupyter --build-arg RELEASE_IMAGE=$(TRAINING_RELEASE_IMAGE) -t $(JUPYTER_IMAGE) docker/ubuntu20.04

code-server:
	@DOCKER_BUILDKIT=1 docker build $(FIX_ARG) -f docker/ubuntu20.04/Dockerfile_codeserver --build-arg RELEASE_IMAGE=$(TRAINING_RELEASE_IMAGE) -t $(CODESERVER_IMAGE) docker/ubuntu20.04

all: dev training serving jupyter code-server
```

运行 `make all` 就可以构建基础镜像、Serving、Training、Jupyter、Code Server 镜像。
