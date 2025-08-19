---
title: MinIO
categories:
  - [tools, MinIO]
tags:
  - tools
  - MinIO
date: "2025-07-25T22:00:00+08:00"
---

# Server

## Docker

```shell
mkdir -p ~/minio/data

docker run \
   -p 9000:9000 \
   -p 9001:9001 \
   --name minio \
   -v ~/minio/data:/data \
   -e "MINIO_ROOT_USER=ROOTNAME" \
   -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
   quay.io/minio/minio server /data --console-address ":9001"
```

## Docker Compose

```yaml
version: '3.8'

services:
  minio:
    image: quay.io/minio/minio
    container_name: minio
    ports:
      - "9000:9000"  # API 端口
      - "9001:9001"  # 控制台端口
    environment:
      MINIO_ROOT_USER: ROOTNAME
      MINIO_ROOT_PASSWORD: CHANGEME123
    volumes:
      - ~/minio/data:/data
    command: server /data --console-address ":9001"
```

# Client

[官方文档](https://min.io/docs/minio/linux/reference/minio-mc.html#minio-client)

## Linux

```shell
# Linux
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/mc
# Alias
mc alias set local http://127.0.0.1:9000 {MINIO_ROOT_USER} {MINIO_ROOT_PASSWORD}
mc admin info local
```

## Mac

```shell
brew install minio/stable/mc
```

# 客户端常用命令

[官方文档](https://min.io/docs/minio/linux/reference/minio-mc.html?ref=docs)