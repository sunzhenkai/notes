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

广告商可以在广告交易平台，选择适合需求的计费模型和指标来优化广告投放。

# 买量方式

不同的广告系统，会根据业务的不同选择不同的买量方式（出价方式），程序化广告交易平台支持的常用买量方式有 CPI、CPC、CPM、深度转化出价、Target-CPE、Target-ROAS 等。对于视频平台广告系统可能会有 CPV 等买量方式。

- CPI，Cost Per Install，每次安装成本
- CPC，Cost Per Click，每次点击成本
- CPM，Cost Per Mille，每千次展示成本
- 双出价 / 深度转化出价
- Target-CPE
- Target-ROAS
- CPA，Cost Per Acquisition，每次获客成本
- CPV，Cost Per View，每次观看成本，主要用于视频广告

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

- LTV，Lifetime Value，指一个用户在其与企业之间的整个生命周期内产生的总价值或收益

# 术语

- [Offer](https://www.cnwangzhuan.com/post/4722.html)，在广告行业，广告主投的广告为 Offer，开发者接受 Offer，广告交易平台的作用是撮合开发者拿到广告主的 Offer
- Campaign，广告活动，一个 Offer 可以拆分多个 Campaign
- Supply，供给方，媒体
- Demand，需求方，广告主
- Advertiser，广告主
- [PMP](https://www.zhihu.com/question/26188653)，Private Marketplace，优质媒体私有化购买
- IAA，In-App Advertising，应用内广告，通过展示广告来获得收入
- IAP，In-App Purchases，应用内购买，帮助开发者实现收入来源
- EGR，Engagement Rate，参与率，广告或营销活动中用户互动的比率
- SKAN，基于苹果官方归因解决方案 SKAdNetwork 的回传数据做出的一个帮助广告主衡量 iOS 端投放效果的榜单，属于确定性归因

# 服务

## DMP

数据管理平台（Data Management Platform，DMP），用于存储设备用户的兴趣、安装列表、以及人物画像等数据。

# 其他

- [PCOC](https://zhuanlan.zhihu.com/p/398235467)，Predict Click Over Click，校准之后的点击率与后验点击率（近似真实概率）的比值

# 参考

- [什么是广告支出回报率（ROAS）](https://zhuanlan.zhihu.com/p/472354040)
- [一文读懂广告各种出价模式](https://zhuanlan.zhihu.com/p/452443071)
