---

---

# 3128 proxy

macos desktop pull 镜像时遇到 proxyconnect 错误。

```shell
docker: Error response from daemon: Get "https://registry-1.docker.io/v2/": proxyconnect tcp: dial tcp 172.17.0.1:3128: connect: connection refused.
```

搞不定了，把容器全删了之后好了。

```shell
# 删除所有容器数据
rm -rf ~/Library/Containers/com.docker.docker
```

