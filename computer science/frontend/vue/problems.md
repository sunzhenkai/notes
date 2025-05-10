---
dtitle: vue 常见问题
categories: 
  - [前端,vue]
tags:
  - vue
date: "2020-12-24T19:00:00+08:00"
---

# 跨域

## webpack

```js
// config/index.js
module.exports = {
  dev: {
    ...
    proxyTable: {
      '/api': {
        target: "http://localhost:8000", 
        changeOrigin: true,
        pathRewrite: {
          '^/api': 'api'
        }
      },
    },
    ...
  }
}
```

