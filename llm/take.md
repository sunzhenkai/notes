---
title: 大语言模型小试
categories: 
	- [大语言模型]
tags:
	- 大语言模型
date: 2023/06/15 00:00:00
update: 2023/06/15 00:00:00
---

# Vicuna

[Vicuna](https://lmsys.org/blog/2023-03-30-vicuna/)，[Github - FastChat](https://github.com/lm-sys/FastChat)。

# 运行

## 安装依赖

```shell
$ pip3 install torch transformers fschat
# 安装 lfs
## ubuntu
sudo apt install git-lfs
# 验证
$ git lfs install
```

## 下载

```shell
# llama 原始模型
$ git clone https://huggingface.co/decapoda-research/llama-13b-hf
# vicuna 模型
$ git clone https://huggingface.co/lmsys/vicuna-13b-delta-v1.1
```

## 更新参数

```shell
$ python3 -m fastchat.model.apply_delta \
    --base-model-path /data/llama-13b-hf \
    --target-model-path /data/vicuna-13b \
    --delta-path /data/vicuna-13b-delta-v1.1
```

## Serving

```shell
nohup python3 -m fastchat.serve.controller &
nohup python3 -m fastchat.serve.model_worker --model-path /data/vicuna-13b --device cpu &
nohup python3 -m fastchat.serve.gradio_web_server &
```

