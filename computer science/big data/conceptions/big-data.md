---
title: 大数据相关概念
categories: 
  - 大数据
  - 概念
tags:
  - 大数据
date: 2020/11/13 16:00:00
update: 2020/11/13 16:00:00
---

# 处理

- 数据清理
- 数据集成
  - 将不同来源于格式的数据逻辑上或物理上进行集成的过程

# 分析

- 联邦分析
  - 一种数据科学方法实践，用于分析存储在用户本地设备中的原始数据，本地计算然后汇总

# 查询

- 联邦查询
  - 对多个不同数据源进行检索进行查询

# 概念

- 数据孤岛
  - 物理性
    - 数据在不同部门相互独立存储，独立维护，彼此间相互孤立
  - 逻辑性
    - 不同部门站在自己角度定义数据，使得数据被赋予不同含义，加大了跨部门数据合作的沟通成本

- 数据仓库
  - 是一个面向主题的、集成的、相对稳定的、反映历史变化的数据集合，用于支持管理决策和信息的全局共享
  - 主要处理历史的、结构化的数据
- 数据集市
  - 数据仓库的特殊形式，正如数据仓库，数据集市也包含对操作数据的快照，便于用户基于历史趋势与经验进行战略决策。两者关键的区别在于数据集市的创建是在有具体的、预先定义好了的对被选数据分组并配置的需求基础之上的。配置数据集市强调对相关信息的易连接性
  - 通俗讲，数据是专门针对特定用户/团队处理后的，以提高数据易用性
- 数据湖
  - 数据湖是一个存储企业各种各样原始数据的大型仓库，其中的数据可供存取、处理、分析和传输
  - 可以包括结构化数据（关系数据库数据）、半结构化数据（json，xml等）、非结构化数据（电子邮件，文档）、二进制数据（音视频等）

# 文章

- [开源SQL执行引擎](https://36kr.com/p/1721504677889)

# 参考

- [数据孤岛 - 百度百科](https://baike.baidu.com/item/%E6%95%B0%E6%8D%AE%E5%AD%A4%E5%B2%9B/10305414?fr=aladdin)
- [数据湖](https://blog.csdn.net/xinshucredit/article/details/88641697)
- [数据集市 - 维基百科](https://zh.wikipedia.org/wiki/%E8%B3%87%E6%96%99%E8%B6%85%E5%B8%82)
- [数据仓库、数据集市、数据湖](https://blog.csdn.net/murkey/article/details/105725924#1.1%E3%80%81%E6%95%B0%E6%8D%AE%E4%BB%93%E5%BA%93%E5%9F%BA%E6%9C%AC%E5%AE%9A%E4%B9%89)
