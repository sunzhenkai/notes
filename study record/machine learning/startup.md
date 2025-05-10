---
title: 机器学习 - 入门
categories: 
  - [研习录, 机器学习]
tags:
  - 机器学习
date: "2024-05-28T00:00:00+08:00"
---

# 概述

机器学习是一门多领域交叉学科，涉及概率论、统计学、逼近论、凸分析、算法复杂度理论等多门学科。其专门研究计算机怎样模拟或实现人类的学习行为，已获得新的知识或技能，重新组织已有的知识机构使之不断改善自身的性能。

# 流程

根据《Data Science Solutions》，完整的解答工作流程包含七个阶段：

- 问题或课题定义
- 获取训练及测试样例集
- 整理、预处理、清洗数据
- 分析、识别模式、探索数据
- 建模、预测、解决问题
- 可视化、汇报、呈现问题解决步骤和最终解决方案
- 提交结果

上述工作流指出了通用的步骤顺序。但是，有时候会有些例外。

- 需要将多个步骤组合在一起
- 需要通过可视化进行分析
- 将一些步骤提前
- 某些步骤重复多次
- 跳过某些步骤

# 目标

数据科学解决方案流程通常有七个主要目标：

- 分类（Classifying）
- 关联（Correlating）
- 转换（Converting）
- 补全（Completing）
- 修正（Correcting）
- 新建（Creating）
- 可视化（Charting）

# 问题分类

- 监督学习（Supervised Learning），数据带有明确的标签或目标值
  - 分类问题（Classification）
    - 目标，将数据点划分到不同的类别中
    - 示例，垃圾邮件判定、良性/恶性肿瘤判定
  - 回归问题（Regression）
    - 目标，预测一个连续的值
    - 示例，房价、股票价格
- 无监督学习（Unsupervised Learning），数据没有明确的标签
  - 聚类
  - 降维
- 强化学习（Reinforcement Learning），智能体通过与环境进行交互并根据奖励信号来学习最佳策略
- 半监督学习（Semi-supervised Learning），使用少量有标签数据和大量无标签数据进行学习
- 主动学习（Active Learning），通过选择最有价值的数据进行标注来提高学习效率
- 迁移学习（Transfer Learning），利用已有的知识和模型来解决新的但相关的问题

## 监督学习

## 回归问题

### 模型

#### 线性回归（Linear Regression）

最基本的回归模型，它假设自变量和因变量之间存在线性关系。

# 参考

- [Kaggle: Intro to Machine Learning](https://www.kaggle.com/learn/intro-to-machine-learning)