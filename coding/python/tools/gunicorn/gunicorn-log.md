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

使用 gunicorn 启动 python 服务，会使用多进程。如果每个进程使用单独的 logger，操作相同的日志文件，那么对于按时间滚动的日志（TimedRotatingFileHandler），会出现冲突（多个进程同一时间 reopen 日志文件）。冲突造成的现象比较复杂，比如丢失日志，再比如开始运行正常但是过一段时间无法写入日志。[这里](https://github.com/benoitc/gunicorn/issues/1272) 可以了解，gunicorn 使用 os.fork 创建的多进程，可以公用日志文件的 offset 和句柄。但是对于多进程写到同一个文件仍可能有问题，解决方案可以参考[这里](https://docs.python.org/3/howto/logging-cookbook.html)，方式是使用 QueueHandler 或 SocketHandler。

另外一种方案，是把日志写到一个文件里面，使用 [logrotate](https://linux.die.net/man/8/logrotate) 工具分隔日志。建议使用这种方式，不使用内置的 TimedRotatingFileHandler，代价是新增一个 logrotate 的配置 + crontab 配置。

当然，还有其他方式，比如继承 TimedRotatingFileHandler，使用锁来规避问题，[这里](https://www.jianshu.com/p/b6bbf22e98d7) 和 [这里](https://blog.csdn.net/dustless927/article/details/122061953)是个示例。

# logrotate

```shell
# /home/ubuntu/server/config/server-logrotate.conf
/home/ubuntu/server/logs/server.log {
    daily
    rotate 30
    missingok
    nocompress
    copytruncate
    notifempty
    dateext
    dateyesterday
}
# crontab
0 0 * * * cd /home/ubuntu/server; logrotate -v -s logs/logrotate-status configs/logrotate.conf >> logs/logrotate.log 2>&1 &
```

## Log Server

一个 Log Server 可以对应多个 Python 服务，只需修改 config 文件即可。多个进程 / 线程通过网络把日志写到日志服务，日志服务负责落日志，这样就避免了多个进程同时操作同一个日志文件的问题。

```python
import logging
import logging.config
import logging.handlers
import pickle
import socketserver
import struct

logging.config.fileConfig('config/log_config.ini')


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)


class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = True

    def __init__(self, host='127.0.0.1',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort


def run(port: int = logging.handlers.DEFAULT_TCP_LOGGING_PORT):
    tcpserver = LogRecordSocketReceiver(port=port)
    print('About to start TCP server...')
    tcpserver.serve_until_stopped()


if __name__ == '__main__':
    run()
```

## 日志配置

```ini
; declarations
[loggers]
keys = root,serving,webhook

[handlers]
keys = generic,serving,webhook

[formatters]
keys = generic

; loggers
[logger_root]
level = INFO
handlers = generic

[logger_serving]
level = INFO
handlers = serving
propagate = 0
qualname = serving

[logger_webhook]
level = INFO
handlers = webhook
propagate = 0
qualname = webhook

; handlers
[handler_generic]
class = handlers.TimedRotatingFileHandler
args = ('./logs/generic.log', 'midnight', 1, 30,)
level = INFO
formatter = generic

[handler_serving]
class = handlers.TimedRotatingFileHandler
args = ('./logs/serving.log', 'midnight', 1, 30,)
level = INFO
formatter = generic

[handler_webhook]
class = handlers.TimedRotatingFileHandler
args = ('./logs/webhook.log', 'midnight', 1, 30,)
level = INFO
formatter = generic

; formatters
[formatter_generic]
format = %(asctime)s-%(levelname)s: %(message)s
datefmt = %Y-%m-%d %H:%M:%S%z
class = logging.Formatter
```

## 使用

```shell
def get_logger(name, port: int = logging.handlers.DEFAULT_TCP_LOGGING_PORT, level=logging.INFO):
    log = logging.getLogger(name)
    log.setLevel(level)
    # socket handler
    sh = logging.handlers.SocketHandler('127.0.0.1', port)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s: %(message)s')
    # consul handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)

    log.addHandler(sh)
    log.addHandler(ch)
    return log


logger = get_logger('serving')
webhook_logger = get_logger('webhook')
```

