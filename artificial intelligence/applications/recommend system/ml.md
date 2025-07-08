---
title: 推荐系统
categories: 
  - [架构, 推荐系统]
tags:
  - 推荐系统
date: "2022-09-02T00:00:00+08:00"
---

# 概念

## 特征

**特征类型**

- Sparse
  - Sparse Id
  - Sparse Real
    - 相对与 Sparse Id 特征，有权重 / 频次信息
- Dense

- [序列特征](https://zhuanlan.zhihu.com/p/461393899)

# 模型

| 模型         | 时间   | 类型         | 说明                                                         |
| ------------ | ------ | ------------ | ------------------------------------------------------------ |
| LR           | ~1990s | 线性         | 逻辑回归模型                                                 |
| FFM          | 2014   | 线性         | Field-aware Factorization Machine，考虑字段交叉；适合稀疏特征场景 |
| PNN          | 2016   | DNN + 内积   | Product-based NN，引入特征内积作为输入结构                   |
| Wide & Deep  | 2016   | 混合         | Google Wide & Deep 结构，线性部分负责记忆，DNN 负责泛化      |
| DeepFM       | 2017   | 混合         | 经典 Wide & Deep 架构，FM 部分显式建模交叉，DNN 学习非线性组合 |
| DCN          | 2017   | 显式交叉     | Deep & Cross Network，引入 Cross Layer 显式建模高阶交叉      |
| FWFM         | 2018   | 线性 + 权重  | Field-weighted FM，FFM 的进化版，引入不同字段间权重          |
| xDeepFM      | 2018   | 混合         | 引入 CIN 层（压缩交叉网络），兼顾显式/隐式交叉               |
| DIN          | 2018   | 序列建模     | Deep Interest Network，加入用户历史行为对当前点击的注意力机制 |
| MMOE         | 2018   | 多任务       | Multi-gate Mixture-of-Experts，用于多目标CTR/CVR建模         |
| ESMM         | 2018   | 多任务归一化 | 用于 CTR + CVR 等场景，解决 CVR 标签稀疏问题                 |
| DIEN         | 2019   | 序列建模     | DIN 的升级版，加入 GRU 进行兴趣建模和演化建模                |
| AutoInt      | 2019   | 自注意力结构 | 自动建模特征交叉，基于 multi-head self-attention             |
| BST          | 2019   | 树 + DNN     | Behavior Sequence Transformer，序列建模与 Transformer 融合   |
| AFN          | 2019   | 非线性建模   | Adaptive Factorization Network，采用 log-bilinear 函数建模特征组合 |
| FiBiNet      | 2019   | 动态建模     | Feature Importance and Bilinear Feature Interaction，建模特征重要性 |
| PLE          | 2020   | 多任务       | Progressive Layered Extraction，多任务建模效果更好           |
| DCN-Mix      | 2021   | 显式交叉     | DCN v2 加强版，融合多个 Cross Network 和 Expert 路径         |
| StarNN       | 2023   | Transformer  | 阿里提出的新一代 CTR Transformer 模型，高效建模稀疏序列      |
| RetentiveNet | 2023   | 新结构       | Meta 提出，结合注意力与遗忘机制，适合序列长程建模            |

> 上面除了 LR、FFM、FWFM 均为 NN 模型。

## 分类

- 线性模型
- 浅层交叉模型
- 深度神经网络（DNN）模型
- 序列建模模型（基于行为序列建模）
- 树模型

```shell
推荐模型
├── 一、线性类（无神经网络）
│   ├── FFM        - Field-aware Factorization Machine（2014）
│   └── FWFM       - Field-weighted FM（2018）
│
├── 二、混合类（线性 + NN）
│   ├── Wide & Deep  - Wide（记忆）+ Deep（泛化）（2016）
│   ├── DeepFM       - FM + DNN（2017）
│   ├── xDeepFM      - CIN（显式交叉）+ DNN（2018）
│   └── DCN          - Cross Network + DNN（2017）
│       └── DCN-Mix  - 多 Cross Network 路径（2021）
│
├── 三、序列建模类（兴趣建模）
│   ├── DIN          - Attention over behavior（2018）
│   ├── DIEN         - DIN + GRU + Interest Evolve（2019）
│   └── BST          - Transformer 架构 + 序列建模（2019）
│
├── 四、注意力机制类（自注意力 / 注意力增强）
│   ├── AutoInt      - Multi-Head Self-Attention + DNN（2019）
│   ├── AFN          - 自适应 log-bilinear 特征组合（2019）
│   └── FiBiNet      - SENet + Bilinear interaction（2019）
│
├── 五、多任务建模类
│   ├── MMOE         - 多专家门控结构（2018）
│   ├── PLE          - 多层渐进专家结构（2020）
│   └── ESMM         - CVR 归一化建模结构（2018）
│
└── 六、下一代结构（Transformer/轻结构）
    ├── StarNN        - 高效稀疏序列 Transformer（2023, 阿里）
    └── RetentiveNet  - Meta 提出，Transformer 替代结构（2023）
```

# 系列文章

- https://zhuanlan.zhihu.com/p/462090167