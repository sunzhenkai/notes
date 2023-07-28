---
title: 安卓基础
categories: 
	- [前端, 安卓]
tags:
	- 安卓
date: 2021/01/09 19:00:00
update: 2021/01/09 19:00:00
---

# 生命周期

![](basic/002.png)

![](basic/001.png)

**状态**

- INITIALIZED
- CREATED
- STARTED
- RESUMED
- DESTROYED

**HOOK**

- onCreate()
- onStart()
- onResume()
- onPause()
- onStop()
- onDestroy()
- onRestart()

# 启动模式

- standard
- singleTop
  - 阻止创建栈顶Activity
- singleTask
  - 阻止常见重复Activity
- singleInstance
  - 使用独立栈