---
title: grpc python3
categories: 
    - [架构, rpc, gRPC]
tags:
    - gRPC
date: "2021-10-12T00:00:00+08:00"
update: "2021-10-12T00:00:00+08:00"
---

# 安装

```shell
$ pip3 install grpcio
```

# 示例

```python
import grpc
channel = grpc.insecure_channel('localhost:8000')
grpc.channel_ready_future(self.channel).result(10)    # 等待 channel ready， 超时 10s
stub = EchoServiceGRPC.EchoServiceStub(self.channel)  # 创建 stub
stub.ping('pong')                                     # 远程调用
```

