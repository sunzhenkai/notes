---
title: element ui
categories: 
  - [前端,element ui]
tags:
  - 前端
  - element ui
date: 2020/12/25 00:00:00
update: 2020/12/25 00:00:00
---

# 表单输入默认居中

使用vue-cli初始化项目，element-ui form 组件，输入项居中显示。

![](problems/001.jpg)

**解决**

调整样式

```vue
<style>
#app {
  ...
  text-align: left;  // center -> left
  ...
}
</style>
```

