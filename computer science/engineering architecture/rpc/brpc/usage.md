---
title: brpc
categories: 
  - [computer science, engineering architecture, rpc]
tags:
  - rpc
  - brpc
date: "2023-05-23T00:00:00+08:00"
update: "2023-05-23T00:00:00+08:00"
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

## 初始化

```shell
bthread_t bid;
bthread_attr_t attr;
bthread_attr_init(&attr);

auto s = [](void *) -> void * {
    auto r = bthread_usleep(1000 * 1000 * 3);
    return nullptr;
};
bthread_start_urgent(&bid, &attr, s, nullptr);
bthread_join(bid, nullptr);
```

## 使用

```shell
#include "bthread/bthread.h"
auto s = [](void *) -> void * {
    bthread_usleep(1000 * 15);
};

bthread_t th1;
bthread_start_urgent(&th1, &attr, s, nullptr);
bthread_join(th1, nullptr);
```

## timer_thread

NOTE: 执行一次，且时间为时间戳（通常是未来时间），非间隔执行。

```c++
#include "bthread/timer_thread.h"
bthread::TimerThread timer;
bthread::TimerThreadOptions options;
timer.start(&options); 
// 或者 timer.start(nullptr); 
timer.schedule(ConfigData::load, this, {butil::seconds_from_now{5}}); // 5秒后执行一次
```

**自定义 Period Timer**

```c++
// brpc_period_timer.h
typedef void (*BrpcPeriodTimerFunction)(void *);

struct BrpcTimerContext {
    BrpcPeriodTimerFunction function;
    void *argument;
    int interval_s;
    bthread::TimerThread *timer;
};

class BrpcPeriodTimer {
public:
    BrpcPeriodTimer();
    ~BrpcPeriodTimer();

    static void Wrapper(void *ctx);
    void Schedule(BrpcTimerContext *);
private:
    bthread::TimerThread timer_;
};

// brpc_period_timer.cpp
BrpcPeriodTimer::BrpcPeriodTimer() {
    timer_.start(nullptr);
}

BrpcPeriodTimer::~BrpcPeriodTimer() {
    timer_.stop_and_join();
}

void BrpcPeriodTimer::Wrapper(void *ctx) {
    auto c = (BrpcTimerContext *) ctx;
    c->function(c->argument);
    c->timer->schedule(BrpcPeriodTimer::Wrapper, ctx, butil::seconds_from_now(c->interval_s));
}

void BrpcPeriodTimer::Schedule(BrpcTimerContext *ctx) {
    auto c = (BrpcTimerContext *) ctx;
    ctx->timer = &timer_;
    timer_.schedule(BrpcPeriodTimer::Wrapper, ctx, butil::seconds_from_now(c->interval_s));
}

// test
TEST(Utils, PeriodTimer) {
    auto payload = [](void *) {
        std::cout << "run payload" << std::endl;
    };

    BrpcPeriodTimer timer;
    BrpcTimerContext ctx{payload, nullptr, 1};
    timer.Schedule(&ctx);

    sleep(10);
}

// output
Testing started at 17:45 ...
run payload
run payload
run payload
run payload
run payload
run payload
run payload
run payload
run payload
Process finished with exit code 0
```

