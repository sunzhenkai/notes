---
title: brpc
categories: 
  - [computer science, engineering architecture, rpc]
tags:
  - rpc
  - brpc
date: 2023/05/23 00:00:00
update: 2023/05/23 00:00:00
---

# 自定义协议

**示例**

```shell
  Protocol protocol = { ParseMessage,
                        SerializeRequest, PackRequest,
                        ProcessHttpRequest, ProcessResponse,
                        VerifyRequest, ParseServerAddress,
                        GetMethodName,
                        CONNECTION_TYPE_SINGLE,
                        "h2" };
  if (RegisterProtocol(PROTOCOL_H2, protocol) != 0) {
      exit(1);
  }
```

**客户端调用顺序**

- 去程
  - SerializeRequest
  - PackRequest
- 回程
  - ParseMessage
  - ProcessResponse

# bthread

## timer_thread

```shell
#include "bthread/timer_thread.h"
bthread::TimerThread timer;
timer.schedule(ConfigData::load, this, {60}); // schedule every 60 seconds
```

