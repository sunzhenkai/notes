---
title: ant design
categories: 
  - [前端,antd]
tags:
  - 前端
  - antd
date: 2022/08/06 00:00:00
---

# Upload 集成在菜单/下拉框选项

```typescript
let items = [            
  {
    label: <Upload
  		multiple={false}
  		showUploadList={false}
  		accept=".json"
  		customRequest={onSelect}>导入</Upload>,
  icon: <ImportOutlined/>,
  key: 1
  }
]

<Menu
	selectedKeys={1}
	items={menuItems}
/>
    
// 自定义上传逻辑
const onSelect = (info: any) => {
    let {file} = info
    let reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
    if (e && e.target && e.target.result) {
        let space: string = e.target.result.toString();
        importSpace(JSON.parse(space))   // importSpace: 发送请求, 返回 Promise 对象
        .then(() => {
        	message.success("导入成功");
        })
        .catch(e => message.error("导入失败"));
    }
    };
    reader.readAsText(file);
};
```

# TroubleShooting

## V4 升 V5

组件兼容

```shell
yarn add @ant-design/compatible@v5-compatible-v4

import { Comment } from '@ant-design/compatible';
```

Babel 配置

```json
{
  "presets": [
    ...
  ],
  "plugins": [
    ...
    [
      "import",
      {
        "libraryName": "antd",
        "libraryDirectory": "es",
        "style": true
      }
    ]
  ]
}
```

