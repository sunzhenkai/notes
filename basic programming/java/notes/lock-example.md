---
title: java lock example
categories: 
  - [coding,java,notes]
tags:
  - java
date: "2021-09-25T00:00:00+08:00"
update: "2021-09-25T00:00:00+08:00"
---

# 场景

## 等待条件发生

比如，有这样一个场景，在 spring boot 工程里面，有一个 controller，他会接受数据并把数据写入 kafka，然后返回写入 kafka 的结果。在调用 send 方法后，会得到一个 `ListenableFuture` 对象，这个对象可以传入 callback 对象，这是一个异步的过程，需要等待回调执行后，才能将结果返回给客户端。

我们就需要一种机制等待回调事件，这里用的模式如下。

```java
Object mutex = new Object();

onSuccess/onFailure[callback] {
    synchronized (mutex) {
        // 发送消息成功后, 唤醒在等待的线程
        mutex.notify(); 
    }
}

// 程序会先走到这里, 并等待 mutex 唤醒
synchronized (mutex) {
    mutex.wait();
}

return ...;
```



```java
@Controller
@RequestMapping("kafka")
public class KafkaController {
    static class Keeper {
        String result;
    }

    @Resource
    KafkaTemplate<String, String> template;

    @RequestMapping(value = "put", method = RequestMethod.POST,
            produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public ResponseEntity<String> check(@RequestBody Message message) throws InterruptedException {
        ListenableFuture<SendResult<String, String>> f = template.send("example", message.getKey(), message.getMessage());
        Object mutex = new Object();
        final Keeper keeper = new Keeper();
        keeper.result = "unknown";
        f.addCallback(new ListenableFutureCallback<SendResult<String, String>>() {
            @Override
            public void onFailure(@SuppressWarnings("NullableProblems") Throwable throwable) {
                keeper.result = "send message failed";
                synchronized (mutex) {
                    mutex.notify();
                }
            }

            @Override
            public void onSuccess(SendResult<String, String> stringStringSendResult) {
                keeper.result = "send message success";
                synchronized (mutex) {
                    mutex.notify();
                }            }
        });

        synchronized (mutex) {
            mutex.wait();
        }

        return ResponseEntity.ok(keeper.result);
    }
}
```

