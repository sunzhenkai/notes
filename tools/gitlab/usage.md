---
title: gitlab 使用
categories: 
  - [工具,gitlab]
tags:
  - gitlab
date: 2020/11/20 00:00:00
update: 2020/11/20 00:00:00
---

# 配置

## 修改外部访问地址

- 修改配置文件 `/etc/gitlab/gitlab.rb`
  - `external_url 'http://git.sample.com:port'`
  - 注意：修改后，gitlab 监听的 port 也会随之更改

## 修改 clone 地址

- http
  - 设置路径：Admin -> General -> Visibility and access controls -> Custom Git clone URL for HTTP(S) 
- ssh
  - 修改配置文件：`/etc/gitlab/gitlab.rb`，注意：host 和 port 要分开修改
    - `gitlab_rails['gitlab_ssh_host'] = 'git.sample.com'`
    - `gitlab_rails['gitlab_shell_ssh_port'] = 2222`

# Runner

```shell
# create volumn
$ docker volume create gitlab-runner-config-1
# create container
$ docker run -d --name gitlab-runner-1 --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v gitlab-runner-config-1:/etc/gitlab-runner \
  -p 8093:8093 \
  gitlab/gitlab-runner:latest
  
# register
$ docker exec -it gitlab-runner gitlab-runner register
```

