---
title: python coroutines
categories: 
	- [python, notes]
tags:
	- python
date: 2021/06/05 00:00:00
---

# 协程

由程序负责任务切换，可以减少线程/进程上下文切换的消耗。用户态实现任务切换，无需进入内核态。

# 用途

虽然 Python 有多线程的概念，但是由于 GIL 的存在，并不能利用多核资源。如果易不能充分利用单进程资源，可能会带来严重的性能问题。

# 相关

## EventLoop

python 默认只为主线程创建 loop。如下 tornado 代码实现了自动为创建 loop 的功能，使用 `asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())` 来生效。

```python
if sys.platform == "win32" and hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    # "Any thread" and "selector" should be orthogonal, but there's not a clean
    # interface for composing policies so pick the right base.
    _BasePolicy = asyncio.WindowsSelectorEventLoopPolicy  # type: ignore
else:
    _BasePolicy = asyncio.DefaultEventLoopPolicy


class AnyThreadEventLoopPolicy(_BasePolicy):  # type: ignore
    """Event loop policy that allows loop creation on any thread.

    The default `asyncio` event loop policy only automatically creates
    event loops in the main threads. Other threads must create event
    loops explicitly or `asyncio.get_event_loop` (and therefore
    `.IOLoop.current`) will fail. Installing this policy allows event
    loops to be created automatically on any thread, matching the
    behavior of Tornado versions prior to 5.0 (or 5.0 on Python 2).

    Usage::

        asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

    .. versionadded:: 5.0

    """

    def get_event_loop(self) -> asyncio.AbstractEventLoop:
        try:
            return super().get_event_loop()
        except (RuntimeError, AssertionError):
            # This was an AssertionError in Python 3.4.2 (which ships with Debian Jessie)
            # and changed to a RuntimeError in 3.4.3.
            # "There is no current event loop in thread %r"
            loop = self.new_event_loop()
            self.set_event_loop(loop)
            return loop
```

# 示例

## 定时器

下面是使用协程实现的定时器。

```python
# coding: utf-8
import asyncio
import threading
import time
from datetime import datetime
from typing import Callable


class Scheduler:
    cache: set[str] = set()

    @classmethod
    async def _do_schedule(cls, name: str, delay: int, interval: int, cb: Callable, args, kwargs):
        await asyncio.sleep(delay)
        while name in cls.cache:
            try:
                cb(*args, **kwargs)
            except Exception as e:
                print('execute target failed, e=', e)
            await asyncio.sleep(interval)

    @classmethod
    def _schedule_wrapper(cls, name: str, delay: int, interval: int, cb: Callable, args, kwargs):
        asyncio.run(cls._do_schedule(name, delay, interval, cb, args, kwargs))

    @classmethod
    def schedule(cls, name: str, delay: int, interval: int, cb: Callable, *args, **kwargs):
        assert name not in cls.cache, 'duplicate scheduler with name ' + name
        threading.Thread(target=cls._schedule_wrapper,
                         args=(name, delay, interval, cb, args, kwargs),
                         daemon=True).start()

        cls.cache.add(name)

    @classmethod
    def stop(cls, name: str):
        if name in cls.cache:
            cls.cache.remove(name)


def cbk(a, b, c):
    print('execute at', datetime.now(), 'with args:', (a, b, c))


if __name__ == '__main__':
    Scheduler.schedule('first', 1, 1, cbk, 'a', 'b', c='c')
    Scheduler.schedule('second', 1, 1, cbk, 'd', 'e', c='f')
    time.sleep(3)
    Scheduler.stop('first')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
```

# 异常

## loop argument must agree with Future

下看下抛出异常的代码。

```python
def ensure_future(coro_or_future, *, loop=None):
    """Wrap a coroutine or an awaitable in a future.
    If the argument is a Future, it is returned directly.
    """
    if futures.isfuture(coro_or_future):
        if loop is not None and loop is not coro_or_future._loop:
            raise ValueError('loop argument must agree with Future')
        return coro_or_future
    elif coroutines.iscoroutine(coro_or_future):
        if loop is None:
            loop = events.get_event_loop()
        task = loop.create_task(coro_or_future)
        if task._source_traceback:
            del task._source_traceback[-1]
        return task
    elif compat.PY35 and inspect.isawaitable(coro_or_future):
        return ensure_future(_wrap_awaitable(coro_or_future), loop=loop)
    else:
        raise TypeError('A Future, a coroutine or an awaitable is required')
```

# 参考

- https://docs.python.org/zh-cn/3/library/asyncio-task.html