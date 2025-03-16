---
title: css
categories: 
  - [前端,css]
tags:
  - 前端
  - css
date: 2022/08/06 00:00:00
---

### 1. Flexbox 布局（推荐首选）

```css
.parent {
  display: flex;
  justify-content: center;  /* 水平居中 */
  align-items: center;      /* 垂直居中 */
}
```

- **特点**：无需计算子元素尺寸，支持动态内容，代码简洁，兼容现代浏览器（IE10+）。
- **适用场景**：响应式布局、简单居中和复杂布局混合场景。

------

### 2. 绝对定位 + Transform

```css
.parent {
  position: relative;  /* 父元素需设置定位 */
}
.child {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);  /* 自动计算偏移量 */
}
```

- **特点**：不依赖子元素尺寸，兼容性较好（IE9+）。
- **适用场景**：固定尺寸父容器、需要精准控制的定位场景。

------

### 3. 绝对定位 + Margin Auto

```css
.parent {
  position: relative;
}
.child {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  margin: auto;
}
```

- **特点**：需子元素固定宽高，兼容性极佳（IE7+）。
- **适用场景**：已知子元素尺寸的传统项目或需要兼容旧浏览器。

------

### 4. Grid 布局（现代方案）

```css
.parent {
  display: grid;
  place-items: center;  /* 同时水平和垂直居中 */
}
```

- **特点**：代码最简洁，支持复杂布局，但兼容性略差（IE 不支持）。
- **适用场景**：现代浏览器项目、需要网格布局的场景。

------

### 5. 表格布局

```css
.parent {
  display: table-cell;
  vertical-align: middle;  /* 垂直居中 */
  text-align: center;      /* 水平居中 */
}
.child {
  display: inline-block;    /* 行内块元素 */
}
```

- **特点**：兼容性好（IE8+），但语义化较差。
- **适用场景**：需要兼容旧版浏览器且不固定宽高的内容。

------

### 6. 传统负 Margin 法

```css
.parent {
  position: relative;
}
.child {
  position: absolute;
  left: 50%;
  top: 50%;
  margin-left: -50px;  /* 子元素宽度一半 */
  margin-top: -50px;   /* 子元素高度一半 */
}
```

- **特点**：需明确子元素尺寸，兼容性极佳（IE6+）。
- **适用场景**：传统项目且子元素尺寸固定。

------

### **总结选择建议**

|          方法          | 是否需要子元素尺寸 |   兼容性   | 适用优先级 |
| :--------------------: | :----------------: | :--------: | :--------: |
|        Flexbox         |         否         |   IE10+    |   ★★★★★    |
|  绝对定位 + Transform  |         否         |    IE9+    |   ★★★★☆    |
|       Grid 布局        |         否         | 现代浏览器 |   ★★★★☆    |
| 绝对定位 + Margin Auto |         是         |    IE7+    |   ★★★☆☆    |
|        表格布局        |         否         |    IE8+    |   ★★☆☆☆    |
|       负 Margin        |         是         |    IE6+    |   ★★☆☆☆    |

------

### **关键注意事项**

1. 父元素尺寸：若使用百分比（如height: 100%），需确保父元素的父级有明确高度（如html, body { height: 100% }）
2. 盒模型干扰：若子元素有 padding 或 border ，建议设置 box-sizing: border-box 防止溢出
3. 浏览器前缀：老旧项目可能需要为 transform 或 flex 添加 -webkit- 等前缀
4. 推荐优先使用 **Flexbox** 或 **Grid 布局**，其次是 **绝对定位 + Transform**，其他方法可作为备选方案。