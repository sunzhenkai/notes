---
title: gunicorn logging
categories: 
	- [python, tools, gunicorn]
tags:
	- python
    - gunicorn
date: 2022/03/30 00:00:00
---

# 多进程日志问题

使用 gunicorn 启动 python 服务，会使用多进程。如果每个进程使用单独的 logger，操作相同的日志文件，那么对于按时间滚动的日志（TimedRotatingFileHandler），会出现冲突（多个进程同一时间 reopen 日志文件）。冲突造成的现象比较复杂，比如丢失日志，再比如开始运行正常但是过一段时间无法写入日志。[这里](https://github.com/benoitc/gunicorn/issues/1272) 可以了解，gunicorn 使用 os.fork 创建的多进程，可以公用日志文件的 offset 和句柄。对于多进程同时滚动日志的问题，貌似可以使用 gunicorn 的日志配置解决（不确定，但是经验证貌似可以工作）。

# 日志配置

需要注意的是，loggers 必须是 `gunicorn.error,gunicorn.access`，这个是 gunicorn 固定的。

```ini
; declarations
[loggers]
keys = root,gunicorn.error,gunicorn.access

[handlers]
keys = consul,access,standard

[formatters]
keys = standard

; loggers
[logger_root]
level = INFO
handlers = consul,standard

[logger_gunicorn.access]
level = INFO
handlers = access
propagate = 0
qualname = gunicorn.access

[logger_gunicorn.error]
level = INFO
handlers = consul,standard
propagate = 0
qualname = gunicorn.error

; handlers
[handler_consul]
class = StreamHandler
level = INFO
formatter = standard
args = (sys.stdout,)

[handler_access]
class = handlers.TimedRotatingFileHandler
args = ('./logs/gunicorn_access.log', 'midnight', 1, 30,)
level = INFO
formatter = standard

[handler_standard]
class = handlers.TimedRotatingFileHandler
args = ('./logs/gunicorn.log', 'midnight', 1, 30,)
level = INFO
formatter = standard

; formatters
[formatter_standard]
format = %(asctime)s-%(levelname)s: %(message)s
datefmt = %Y-%m-%d %H:%M:%S%z
class = logging.Formatter
```

