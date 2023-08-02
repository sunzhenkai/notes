---
title: 广告推荐
categories: 
  - [架构, 推荐系统, 广告推荐]
tags:
  - 推荐系统
    - 广告推荐
date: 2022/04/12 00:00:00
update: 2022/04/12 00:00:00
---

# 指标

- eCPM，期望价值，用于评估当前请求的预估价值
  - 基于 eCPM 来控制利润率

- 填充率，FillRate，有效请求量(有广告填充) / 总请求量
- ROI

> ROI ，投资回报率（Return on Investment），利润 / 花费

- CTR，点击率（点击 / 展示）
- CVR，点击转化率（转化 / 点击）
- IVR，曝光转化率（转化 / 展示）

> eCPM = ivr * price * 1000

# 术语

- [Offer](https://www.cnwangzhuan.com/post/4722.html)，在广告行业，广告主投的广告为 Offer，开发者接受 Offer，广告交易平台的作用是撮合开发者拿到广告主的 Offer
- Campaign，广告活动，一个 Offer 可以拆分多个 Campaign
- Supply，供给方，媒体
- Demand，需求方，广告主
- Advertiser，广告主
- [PMP](https://www.zhihu.com/question/26188653)，Private Marketplace，优质媒体私有化购买

# 服务

## DMP

数据管理平台（Data Management Platform，DMP），用于存储设备用户的兴趣、安装列表、以及人物画像等数据。

# 其他

- [PCOC](https://zhuanlan.zhihu.com/p/398235467)，Predict Click Over Click，校准之后的点击率与后验点击率（近似真实概率）的比值
