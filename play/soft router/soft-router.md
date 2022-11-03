---
title: soft router
categories: 
	- [play,soft router]
tags:
	- soft router
date: 2022/10/16 00:00:00
---

# 镜像

- [lede](https://github.com/coolsnowwolf/lede)

# 主题

- https://github.com/jerrykuku/luci-theme-argon

# LEDE

## 更新源配置

**腾讯**

```shell
src/gz openwrt_core https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/targets/x86/64/packages
src/gz openwrt_base https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/packages/x86_64/base
src/gz openwrt_luci https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/packages/x86_64/luci
src/gz openwrt_packages https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/packages/x86_64/packages
src/gz openwrt_routing https://mirrors.cloud.tencent.com/openwrt/releases/22.03.2/packages/x86_64/routing
src/gz openwrt_telephony https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/telephony
```

**清华源**

```shell
src/gz openwrt_core https://mirrors.cloud.tencent.com/lede/snapshots/targets/x86/64/packages
src/gz openwrt_base https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/base
src/gz openwrt_helloworld https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/helloworld
src/gz openwrt_kenzo https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/kenzo
src/gz openwrt_luci https://mirrors.cloud.tencent.com/lede/releases/18.06.9/packages/x86_64/luci
src/gz openwrt_packages https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/packages
src/gz openwrt_routing https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/routing
src/gz openwrt_small https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/small
src/gz openwrt_telephony https://mirrors.cloud.tencent.com/lede/snapshots/packages/x86_64/telephony
```

