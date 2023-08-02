---
title: seastar compile
categories: 
  - [架构,java,框架,seastar]
tags:
  - seastar
date: 2021/12/15 00:00:00
update: 2021/12/15 00:00:00
---

# Clone

```shell
$ git clone --recurse-submodules -j8 git@github.com:scylladb/seastar.git
```

# Install

## dpdk

```shell
$ git clone http://dpdk.org/git/dpdk
$ cd dpdk
$ export RTE_SDK=$(pwd)
$ export RTE_TARGET=x86_64-native-linuxapp-gcc  # depends on your env
$ make -j8 install T=$RTE_TARGET DESTDIR=/usr/local
```

## alter gcc/g++

```shell
# install alter
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 50
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 50
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 40
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 40

# config alter
sudo update-alternatives --config gcc
```

## seastar

```shell
./cooking.sh -t Release -- -DSeastar_DPDK=ON
```

# tag 20.05

## dpdk

内核版本 > 5.4.0 会导致编译出错，详见[这里](https://bugs.launchpad.net/ubuntu/+source/dpdk/+bug/1848585)，做下面改动。

- [fix for pci-aspm](https://bugs.launchpad.net/ubuntu/+source/dpdk/+bug/1848585/+attachment/5298807/+files/dpdk-kni-pci-aspm-fix.patch)
- [num-online-cpus](https://bugs.launchpad.net/ubuntu/+source/dpdk/+bug/1848585/+attachment/5298831/+files/dpdk-kni-fix-num_online_cpus.patch) 
- [skb conversion to bio_vec](https://bugs.launchpad.net/ubuntu/+source/dpdk/+bug/1848585/+attachment/5298857/+files/dpdk-kni-skb-rename.patch) 
