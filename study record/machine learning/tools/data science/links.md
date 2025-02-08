---
title: datascience - links
categories: 
    - [play, server]
tags:
    - development
date: 2023/07/27 00:00:00
update: 2023/07/27 00:00:00
---
如果你搭建了 datascience 开发环境，并在 hosts 中配置了 datascience 解析，那么下面的链接你可能会用到。
# UI
- [Airflow](http://datascience:8208)
    - `username: admin, password: admin`

- [Azkaban](http://datascience:8261)
    - `username: azkaban, password: azkaban`
- [Consul](http://datascience:8500)
- [Dolphinscheduler](http://datascience:12345/dolphinscheduler/ui)
    - `username: admin, password: dolphinscheduler123`

- [Flink JobManager](http://datascience:8220)
- [Gitlab](http://datascience:8929)
- [Grafana](http://datascience:3000)
- [Jupyter Server](http://datascience:8285)
    - `password: jupyter`
- [PhpMyAdmin](http://datascience:8283)
    - `username: root, password: <empty>`
- [Portainer](http://datascience:8263)
- [Prometheus](http://datascience:8290)
- [Spark](http://datascience:8286)
- [Zeeplin](http://datascience:8280)


# Ports
```shell
# development ssh
datascience:2025
# hadoop
datascience:8020
# kafka
datascience:9092
# gitlab ssh port
datascience:2224
# mariadb
datascience:3306
# mongodb
datascience:27017
# postgresql
datascience:5432
# prometheus
datascience:8290
# redis
datascience:6379
# zookeeper
datascience:2181