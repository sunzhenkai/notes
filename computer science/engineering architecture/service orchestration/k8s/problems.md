---
title: k8s problems
categories: 
  - [架构,container,k8s]
tags:
  - k8s
date: 2022/08/27 00:00:00
---

# Pod 无法解析域名

Pod DNS 策略模式是 ClusterFirst，系统 `/etc/resolve.conf` 内容如下。

```shell
nameserver 127.0.0.53
options edns0 trust-ad
search .
```

导致 Pod 里面的 `/etc/resolv.conf` 配置也是如此，无法正常解析域名。先删除 `/etc/resolv.conf`（`/run/systemd/resolve/stub-resolv.conf` 的软链） ，再创建并写入如下内容。

```shell
nameserver 223.5.5.5
nameserver 8.8.8.8
```

```shell
sudo rm /etc/resolv.conf
sudo vim /etc/resolv.conf
```

重启 Pods。

```shell
kubectl delete pods --all -n=<namespace> # 删除所有 pods
```

# pod didn't trigger scale-up

**错误信息**

```shell
.. (combined from similar events): pod didn't trigger scale-up (it wouldn't fit if a new node is added): 2 Insufficient memory, 7 can't increase node group size
```

**原因**

- pod 添加的 container 的内存、CPU 资源超过资源池机器的限制，导致无法扩容

**解决**

- 减少 container 的 memory / cpu

# Core Dump 及保存

**设置 core dump 保存路径及命名**

在 `deployment.yaml` 中配置，运行命令 `echo "core.%p" > /proc/sys/kernel/core_pattern` 。

映射 HostPath，容器重启不删除文件。

```yaml
# deployment.yaml
spec:
	template:
		spec:
			volumes:
				- name: core-dump-volume
          hostPath:
            path: /data/core
            type: DirectoryOrCreate
			containers:
				- name: {container-name}
					volumeMounts:
						- name: core-dump-volume
							mountPath: /data/core
```

