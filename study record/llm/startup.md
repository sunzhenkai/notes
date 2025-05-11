---
title: LLM - startup
categories: 
  - [LLM]
tags:
  - LLM
date: "2023-06-15T00:00:00+08:00"
update: "2023-06-15T00:00:00+08:00"
---

# 问题排查

## nvidia-container-cli: initialization error: load library failed: libnvidia-ml.so.1 #154

详见[这里](https://github.com/NVIDIA/nvidia-container-toolkit/issues/154)。

```shell
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl restart docker
```

## no compatible GPUs were discovered / Failed to initialize NVML: Unknown Error

Ollama docker 容器找不到 GPU。

如果使用 docker compose，配置如下。

```shell
services:
  ollama:
    image: ollama/ollama:latest
    restart: always
    hostname: ollama
    runtime: nvidia
    user: root
    ports:
      - '11434:11434'
    volumes:
      - /data/docker/llm/ollama:/root/.ollama
    networks:
      - default
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

解决。宿主机编辑 `/etc/nvidia-container-runtime/config.toml`。

```shell
no-cgroups = false # 修改, true -> false
```

重启 docker。

```shell
sudo systemctl restart docker
```

