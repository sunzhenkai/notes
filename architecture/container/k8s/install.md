---
title: k8s 安装
categories: 
	- [架构,container,k8s]
tags:
	- k8s
date: 2021/08/25 00:00:00
update: 2021/08/25 00:00:00
---

[toc]

# 安装

## 安装运行时

**[docker](https://docs.docker.com/engine/install/#server)**

```shell
# ubuntu
## 安装依赖
sudo apt-get install -y ca-certificates curl gnupg lsb-release
## 添加 GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
## 添加 sources repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
## install docker engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

对于新版的 k8s，使用 docker 还需要安装 [cri-docker](https://github.com/Mirantis/cri-dockerd)，从[这里]( https://github.com/Mirantis/cri-dockerd/releases )下载二进制程序，把下面的内容保存为两个文件 `cri-docker.service` 和 `cri-docker.socket`。

```shell
# cri-docker.service
[Unit]
Description=CRI Interface for Docker Application Container Engine
Documentation=https://docs.mirantis.com
After=network-online.target firewalld.service docker.service
Wants=network-online.target
Requires=cri-docker.socket

[Service]
Type=notify
ExecStart=/usr/bin/cri-dockerd --container-runtime-endpoint fd:// --network-plugin=
ExecReload=/bin/kill -s HUP $MAINPID
TimeoutSec=0
RestartSec=2
Restart=always

# Note that StartLimit* options were moved from "Service" to "Unit" in systemd 229.
# Both the old, and new location are accepted by systemd 229 and up, so using the old location
# to make them work for either version of systemd.
StartLimitBurst=3

# Note that StartLimitInterval was renamed to StartLimitIntervalSec in systemd 230.
# Both the old, and new name are accepted by systemd 230 and up, so using the old name to make
# this option work for either version of systemd.
StartLimitInterval=60s

# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity

# Comment TasksMax if your systemd version does not support it.
# Only systemd 226 and above support this option.
TasksMax=infinity
Delegate=yes
KillMode=process

[Install]
WantedBy=multi-user.target
```

```shell
# cri-docker.socket
[Unit]
Description=CRI Docker Socket for the API
PartOf=cri-docker.service

[Socket]
ListenStream=%t/cri-dockerd.sock
SocketMode=0660
SocketUser=root
SocketGroup=docker

[Install]
WantedBy=sockets.target
```

**移动文件**

```shell
# 移动二进制
sudo mv cri-docker /usr/bin
# 移动 systemd 配置
sudo mv cri-docker.service /etc/systemd/system/
sudo mv cri-docker.socket /etc/systemd/system/
```

**systemd 启动服务**

```shell
sudo systemctl daemon-reload
sudo systemctl enable cri-docker.service
sudo systemctl enable --now cri-docker.socket

# 启动服务
sudo service cri-docker start
```

## 安装 kub*

安装 kubeadm、kubelet、kubectl，国内源参考 [阿里云镜像](https://developer.aliyun.com/mirror/kubernetes?spm=a2c6h.13651102.0.0.3e221b114M3BYV) 或者 [清华开源镜像站](https://mirrors.tuna.tsinghua.edu.cn/help/kubernetes/)。

```shell
sudo apt-get update && apt-get install -y apt-transport-https
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | sudo apt-key add - 
# root 用户运行
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
```

## 拉取镜像

```shell
$ sudo kubeadm config images pull \
	--image-repository registry.aliyuncs.com/google_containers \
	--cri-socket unix:///var/run/cri-dockerd.sock
```

## 初始化

```shell
# 10.244.0.0/16 是 chennel 扩展的配置
# --apiserver-advertise-address 是 master 节点的 ip，如果是单机，即为该机器 ip 地址
$ kubeadm init --image-repository registry.aliyuncs.com/google_containers \
  --pod-network-cidr 10.244.0.0/16 \
  --control-plane-endpoint 10.1.0.145 \
	--cri-socket unix:///var/run/cri-dockerd.sock
```

## root 用户使用

需要配置 `KUBECONFIG=/etc/kubernetes/admin.conf`。

```shell
root@k8s-master-1:/home/ubuntu# export KUBECONFIG=/etc/kubernetes/admin.conf
root@k8s-master-1:/home/ubuntu# kubectl get nodes
NAME           STATUS   ROLES           AGE     VERSION
k8s-master-1   Ready    control-plane   5m55s   v1.24.1
```

## 配置 none root 用户使用

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## 验证

```shell
ubuntu@k8s-master-1:~$ kubectl get nodes
NAME           STATUS   ROLES           AGE     VERSION
k8s-master-1   Ready    control-plane   4m52s   v1.24.1
```

## 回滚操作

```shell
kubeadm reset [glags] 

preflight              Run reset pre-flight checks
update-cluster-status  Remove this node from the ClusterStatus object.
remove-etcd-member     Remove a local etcd member.
cleanup-node           Run cleanup node.
```

## 配置网络

这一步很关键，如不能正确配置集群网络，pod 间可能无法通讯，kubectl proxy 无法正常访问（通常表现为 pod 运行正常，但提示连接拒绝）。以 flannel 为例，首先安装 flannel。

```shell
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

[使用工具 mk-docker-opts.sh](https://github.com/flannel-io/flannel/blob/master/dist/mk-docker-opts.sh)生成网络信息，这个工具也可以使用 `sudo find / -name 'mk-docker-opts.sh'` 在 docker 容器中找到。

```shell
$ mk-docker-opts.sh -d /run/docker_opts.env -c
```

修改 docker service。

```shell
# root 用户执行
$ vim /lib/systemd/system/docker.service
# 添加这一行
EnvironmentFile=/run/docker_opts.env
# 修改这一行
ExecStart=/usr/bin/dockerd $DOCKER_OPTS -H fd:// ...

# 重启 docker
$ systemctl daemon-reload
$ systemctl restart docker
```

## 添加节点

对添加的节点同样需要配置网络，且不可复用其他节点的 docker_opts.env 文件。

```shell
# 在 master 节点
$ kubeadm token create --print-join-command
... 

# 在待加入的节点, 在上面生成的命令后面指定 cri socket
$ kubeadm join 10.1.0.145:6443 --token nxxcv7.gge00x97wiphualw --discovery-token-ca-cert-hash sha256:cfb324b2ee7ee548b08e38d2e6d60905e392553bf6715504e87888183a1238fd
u --cri-socket unix:///var/run/cri-dockerd.sock

# 为新节点指定 label
$ kubectl label node k8s-worker-1 node-role.kubernetes.io/worker=worker

# 验证
ubuntu@k8s-master-1:~$ kubectl get nodes
NAME           STATUS   ROLES           AGE     VERSION
k8s-master-1   Ready    control-plane   9h      v1.24.1
k8s-worker-1   Ready    worker          3m17s   v1.24.1
```

## 安装  dashboard

```shell
# 安装 dashboard
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.6.0/aio/deploy/recommended.yaml

# 启动代理
$ kubectl proxy --address=0.0.0.0
```

**创建服务账号**

 保存到 `account.yaml`。

```shell
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
```

然后运行。

```shell
kubectl apply -f account.yaml
```

**设置权限**

保存到 `permission.yaml`。

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

然后运行。

```shell
kubectl apply -f permission.yaml
```

也可以放到一个文件里面。

```shell
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard

---

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

**获取 token**

```shell
kubectl -n kubernetes-dashboard create token admin-user
```

### **https 证书**

k8s dashboard 默认会自己生成证书，可以跳过。对于 https 证书，可以自己生成证书，可以用证书认证服务商。对于自己生成证书，可以手动生成，也可以通过添加 `--auto-generate-certificates`  来自动生成，更多参数参考[这里](https://github.com/kubernetes/dashboard/blob/master/docs/common/dashboard-arguments.md)。

```shell
# 自认证证书
# 生成 dashboard.pass.key
$ openssl genrsa -des3 -passout pass:over4chars -out dashboard.pass.key 2048
# 生成 dashboard.key
$ openssl rsa -passin pass:over4chars -in dashboard.pass.key -out dashboard.key
$ rm dashboard.pass.key # 可以删除了
# 生成 dashboard.csr
$ openssl req -new -key dashboard.key -out dashboard.csr # 一直回车
# 生成 dashboard.crt
$ openssl x509 -req -sha256 -days 365 -in dashboard.csr -signkey dashboard.key -out dashboard.crt
```

### 删除 dashboard

```shell
$ kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.6.0/aio/deploy/recommended.yaml
```

# 网络扩展

## flannel

### 安装

```shell
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

# 常用命令

## 查看节点信息

```shell
$ kubectl get nodes
NAME                    STATUS     ROLES                  AGE     VERSION
localhost.localdomain   NotReady   control-plane,master   2m13s   v1.22.1
```

## 查看 pod 信息

```shell
$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                            READY   STATUS    RESTARTS   AGE
kube-system   coredns-78fcd69978-9dk4n                        0/1     Pending   0          2m52s
kube-system   coredns-78fcd69978-w52zc                        0/1     Pending   0          2m52s
kube-system   etcd-localhost.localdomain                      1/1     Running   0          3m6s
kube-system   kube-apiserver-localhost.localdomain            1/1     Running   0          3m6s
kube-system   kube-controller-manager-localhost.localdomain   1/1     Running   0          3m8s
kube-system   kube-proxy-4w84n                                1/1     Running   0          2m52s
kube-system   kube-scheduler-localhost.localdomain            1/1     Running   0          3m6s
```

# pod 管理

```shell
# 查看 pod  信息
$ kubectl get pods -A  # A = all-namespaces

# 删除 pod
$ kubectl delete pod kubernetes-dashboard --namespace=kubernetes-dashboard
```

# 参考

- http://blog.hungtcs.top/2019/11/27/23-K8S%E5%AE%89%E8%A3%85%E8%BF%87%E7%A8%8B%E7%AC%94%E8%AE%B0/
- https://www.youtube.com/watch?v=ACypx1rwm6g

# 问题

## 配置

k8s 配置在这里 `/etc/kubernetes/kubelet.conf`。

## 找不到节点

```shell
ubuntu@k8s-master-1:~$ systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
     Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/kubelet.service.d
             └─10-kubeadm.conf
     Active: active (running) since Wed 2022-06-08 16:18:53 UTC; 2s ago
       Docs: https://kubernetes.io/docs/home/
   Main PID: 69055 (kubelet)
      Tasks: 29 (limit: 38495)
     Memory: 39.5M
     CGroup: /system.slice/kubelet.service
             └─69055 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/co>

Jun 08 16:18:55 k8s-master-1 kubelet[69055]: E0608 16:18:55.158403   69055 kubelet_node_status.go:92] "Unable to register node with API server" err="Post \"https://10.1.0>
Jun 08 16:18:55 k8s-master-1 kubelet[69055]: E0608 16:18:55.193156   69055 kubelet.go:2419] "Error getting node" err="node \"k8s-master-1\" not found"
...
```

[这里](https://github.com/kubernetes/kubeadm/issues/2370) 有说，可能是 api server 不能连接，由于 cri 用了 docker，随检查 docker 状态。

> node not found is a misleading error by the kubelet. at this point it means that the kubelet was unable to register a Node object with the api server.
>
> > https://nalshsvrk8ss01.railcarmgt.com:6443/healthz?timeout=10s in 0 milliseconds
>
> this means that the api server cannot be connected. could be caused by a number of things (including firewall).

```shell
root@k8s-master-1:~# service docker status
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2022-06-08 16:30:32 UTC; 34min ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 1039 (dockerd)
      Tasks: 23
     Memory: 134.1M
     CGroup: /system.slice/docker.service
             └─1039 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

Jun 08 17:04:52 k8s-master-1 dockerd[1039]: time="2022-06-08T17:04:52.874831490Z" level=error msg="Handler for POST /v1.40/images/create returned error: Get \"https://k8s.gcr.io/v2/\": context deadline exceeded"
Jun 08 17:04:58 k8s-master-1 dockerd[1039]: time="2022-06-08T17:04:58.867350258Z" level=warning msg="Error getting v2 registry: Get \"https://k8s.gcr.io/v2/\": net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)"
...
```

果然是镜像有问题，从 k8s.gcr.io 拉取镜像失败。可以根据[这里](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#custom-images)的说明，来指定自定义的镜像地址。

```shell
# 查看服务实时日志
$ journalctl -u docker -f
```

设置 `--image-repository`可以拉下来镜像，但还是会在启动 control plane 时超时。

```shell
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[kubelet-check] Initial timeout of 40s passed.
```

老老实实挂代理吧。

```shell
sudo mkdir -p /etc/systemd/system/docker.service.d 
sudo touch /etc/systemd/system/docker.service.d/proxy.conf
sudo chmod 777 /etc/systemd/system/docker.service.d/proxy.conf
sudo echo '
[Service]
Environment="HTTP_PROXY=socks5://192.168.6.19:3213" 
Environment="HTTPS_PROXY=socks5://192.168.6.19:3213"
' >> /etc/systemd/system/docker.service.d/proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl restart kubelet
```

## 使用 kubectl proxy 无法访问其他节点服务

下面是访问 dashboard 的错误信息，运行时是 docker，kubernetes-dashboard 运行在另外一台 worker node 上，使用 master node 的 proxy 访问 dashboard 服务会报下面的错误。

```shell
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {
    
  },
  "status": "Failure",
  "message": "error trying to reach service: dial tcp 172.17.0.3:8443: connect: connection refused",
  "reason": "ServiceUnavailable",
  "code": 503
}
```

原因是 docker 容器使用的网络（172.17.0.1/16）和网络扩展（用的是 flannel，10.244.0.0/32）不是统一个网络，导致无法访问。这里的 172.17.0.3 其实是 worker node 的网络地址，这是因为 proxy 容易部署早于 flannel，不在同一个网络。

```shell
# 查看 flannel 网络
$ cat /run/flannel/subnet.env
FLANNEL_NETWORK=10.244.0.0/16
FLANNEL_SUBNET=10.244.0.1/24
FLANNEL_MTU=1400
FLANNEL_IPMASQ=true
```

生成 docker 环境变量 DOCKER_OPTS。

```shell
# 找到 mk-docker-opts.sh，在 flannel 镜像里面；也可以下载 flannel 的二进制包找到这个脚本
$ sudo find / -name 'mk-docker-opts.sh'
/var/lib/docker/overlay2/8779d2bd83ddf0e237da15f5c0e62fd79bbf6d3868cea87ec926c471f1184774/merged/opt/bin/mk-docker-opts.sh
/var/lib/docker/overlay2/99462f1d9e955f5c40a11844119dc1e0f295208c20a696e7bea76b39324a9943/diff/opt/bin/mk-docker-opts.sh

# root 用户; 生成 docker opts
$ alias mk-docker-opts="/var/lib/docker/overlay2/99462f1d9e955f5c40a11844119dc1e0f295208c20a696e7bea76b39324a9943/diff/opt/bin/mk-docker-opts.sh"
$ mk-docker-opts -d /run/docker_opts.env -c
```

修改 docker service。

```shell
# root 用户执行
$ vim /lib/systemd/system/docker.service
# 添加这一行
EnvironmentFile=/run/docker_opts.env
# 修改这一行
ExecStart=/usr/bin/dockerd $DOCKER_OPTS -H fd:// ...

# 重启 docker
$ systemctl daemon-reload
$ systemctl restart docker
```

验证 pod ip。

```shell
# alias k8s="kubectl --namespace=default"
$ k8s get pods
NAME                                        READY   STATUS    RESTARTS   AGE
dashboard-metrics-scraper-8c47d4b5d-2bbbx   1/1     Running   0          43s
kubernetes-dashboard-59fccbc7d7-9wmn9       1/1     Running   0          43s
$ k8s describe pod kubernetes-dashboard-59fccbc7d7-9wmn9
Name:         kubernetes-dashboard-59fccbc7d7-9wmn9
Namespace:    default
Priority:     0
Node:         k8s-worker-1/10.1.0.123
Start Time:   Sat, 11 Jun 2022 07:03:10 +0000
Labels:       k8s-app=kubernetes-dashboard
              pod-template-hash=59fccbc7d7
Annotations:  seccomp.security.alpha.kubernetes.io/pod: runtime/default
Status:       Running
IP:           10.244.1.3
...
```

这里需要注意的是，需要在每个 node 执行上面的操作，docker_opt.env 文件不能共用。

## dashboard 无法登录

使用 proxy 的方式打开登录界面之后，会发现无法登录，有如下提示。

```shell
Insecure access detected. Sign in will not be available. Access Dashboard securely over HTTPS or using localhost. Read more here .
```

即便添加如下参数。

```shell
--auto-generate-certificates
--namespace=default
--insecure-bind-address=0.0.0.0
--insecure-port=8080
--enable-insecure-login	
```

根据 [这里](https://github.com/kubernetes/dashboard/issues/6693) 说的，`--enable-insecure-login` 仅适用在 `127.0.0.1` 和 `localhost` 使用 http 登录的情景，对于使用 kubectl proxy 使用 http 协议并不适用。

**端口转发**

```shell
$ kubectl port-forward -n default service/kubernetes-dashboard 18082:443 --address='0.0.0.0' 
```

## 解决方案

dashboard 的 ssl 认证有点坑，可以确认下面几点。

- 不允许使用非 `localhost` 和 `127.0.0.1` 地址使用 HTTP 协议访问，没有配置可以规避这个问题，所以

  - `kubectl proxy` 方式只能是在本机安装 k8s 时使用
  - 基本可以放弃使用 HTTP 访问了

- 非 `localhost` 和 `127.0.0.1` 只能使用 HTTPS 协议访问了

所以，对于使用 HTTPS ，可以从两个方向来解决。

- 购买证书认证商的认证服务，使用域名，并配置域名解析
- 搭建 self-signed 站点

购买证书认证服务就不说了，**记录几个可行的解决方案。**

- 端口转发
  - Firefox 可以访问
  - Chrome 不能查看证书，Safari、Chrome、Opera 不能访问
- 搭建 nginx 服务并做自认证
  - Safari、Firefox 可以忽略风险直接访问
  - Chrome 需要先下载证书，标记信任后可访问

## 搭建 nginx 并配置自认证

至于搭建参考[这里](https://www.howtogeek.com/devops/how-to-create-and-use-self-signed-ssl-on-nginx/)吧，端口类型改为 NodePort。

```shell
kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: default
spec:
  ports:
    - port: 443
      targetPort: 8443
  type: NodePort
  selector:
    k8s-app: kubernetes-dashboard
```

添加 nginx 配置。

```shell
upstream k8s-dashboard {
    server 10.244.1.2:8443;
}

server {
    # auth_basic "Auth Message";
    # auth_basic_user_file /etc/apache2/.htpasswd;
    client_max_body_size 100m;
	  listen 8443 ssl default_server;
	  listen [::]:8443 ssl default_server;
	  server_name  192.168.6.103;
	  include snippets/self-signed.conf;

    location / {
        proxy_pass         https://k8s-dashboard;
        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        
        # enable websocket
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

然后就可以使用 Chrome 访问了。

```shell
# 浏览器输入地址
https://192.168.6.103:8443/#/login
```

