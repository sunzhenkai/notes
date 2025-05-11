---
title: phpmyadmin
categories: 
  - [架构, 存储, mariadb]
tags:
  - phpmyadmin
    - mariadb
date: "2022-08-27T00:00:00+08:00"
---

# Docker

```shell
docker pull phpmyadmin
docker run --name phpmyadmin -d -e PMA_ARBITRARY=1 -p 8080:80 phpmyadmin
```

