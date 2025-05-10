---
title: CUDA - 版本及环境搭建
categories: 
    - 研习录
tags:
    - 研习录
date: "2023-12-18T00:00:00+08:00"
---

CUDA （**Compute Unified Device Architecture**）是英伟达开发的并行计算平台，为使用 GPU 加速的程序提供开发环境（当前仅针对英伟达设备）。

# API

CUDA 提供两层 API，驱动（Driver） API 及运行时（Runtime） API。Runtime API 是基于 Driver API 编写的、使用更为简便的 API。

# Compute Capability

英伟达每款 GPU 会有一个叫做 Compute Capability 的版本号，用于标识设备的**计算平台兼容性**。其直译 **计算能力** 略有歧义，并非代表设备的计算性能。