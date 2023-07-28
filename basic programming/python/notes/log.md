---
title: python logger
categories: 
	- [python, notes]
tags:
	- python
date: 2021/11/25 00:00:00
update: 2021/11/25 00:00:00
---

# 自定义 Logger

```python
logger = logging.getLogger()
# 设置 level，不然可能不打印
logger.setLevel(logging.INFO)

# 打印格式
fmt = logging.Formatter('[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s',
                        '%Y-%m-%d %H:%M:%S')
# 打印到标准输
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(fmt)
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)
# 写入文件
file_handler = logging.handlers.RotatingFileHandler(file_path,
maxBytes=per_file_size,
backupCount=log_file_number)
file_handler.setFormatter(fmt)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
```