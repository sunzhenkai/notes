---
title: 机器学习 - 特征工程
categories: 
  - [研习录]
tags:
  - 研习录
date: "2024-06-25T00:00:00+08:00"
---

# 特征分类

- 按数据类型分类

  - 数值特征
    - 离散数值特征，有限的离散值，比如年龄
    - 连续数值类型，任意实数，比如体重

  - 分类特征
    - 有序分类特征，类别之间存在顺序，比如初中、高中、大学
    - 无序分类特征，类别之间没有顺序，比如血型

- 按生成方式分类

  - 原始特征，直接从数据集中获取的未经处理的特征
  - 衍生特征，通过对原始特征进行数学运算、转换或组合而生成的新特征

- 按特征稳定性分类

  - 稳定特征，在不同时间或数据集中变化较小的特征，如人的性别
  - 不稳定特征，容易随时间或数据分布变化而变化的特征，比如股票价格