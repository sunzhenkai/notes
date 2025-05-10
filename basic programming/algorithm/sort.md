---
title: 排序
categories: 
  - [coding, 算法]
tags:
  - 算法
date: "2021-04-12T00:00:00+08:00"
update: "2021-04-12T00:00:00+08:00"
---

# 快排

## 说明

图解 [思路](https://leetcode-cn.com/problems/sort-an-array/solution/pai-xu-shu-zu-by-leetcode-solution/) 参考 leetcode，忽略 random 优化的思路步骤如下。

- 每次排序选第一个元素作为**基准元素**，将基准元素保存在变量 pivot 中，此时空出一个位置（即基准元素，不必重置元素值）
- 定义两个**游标 left、right** 分别从数组两端遍历，其中分别初始化为待排序子数组的左边界索引和右边界索引
- 然后从右边找一个小于基准值的元素，放到左侧空出的位置，此时该位置空置
- 然后从左侧找一个大于基准值的元素，放到右侧空出的位置，此时该位置空置
- **重复前两步**，直到左右游标相遇（left == right），此时游标所指位置空置
- 将基准元素放入游标位置，此时游标左侧的值都小于基准值，游标右侧的值都大于基准值
- 递归的对游标左侧数组和右侧数组排序
- 得到一个排序完成的数组

## Javascript

```javascript
/**
 * 快速排序
 * @param nums  数组
 * @param left  排序的左边界索引
 * @param right 排序的右边界索引
 */
function qsort(nums, left, right) {
    if (left >= right) return;

    var pivot = nums[left], i = left, j = right;
    while (i < j) {
        while (i < j && nums[j] > pivot) --j;
        nums[i] = nums[j];

        while (i < j && nums[i] <= pivot) ++i;
        nums[j] = nums[i];
    }
    nums[i] = pivot;
    qsort(nums, left, i-1);
    qsort(nums, i+1, right);
}
```

**测试**

```javascript

var v;
v = [3, 2, 1, 3, 4, 0, -1, 8, 9, 1, 0];
qsort(v, 0, v.length - 1);
console.log(v);

v = [];
qsort(v, 0, v.length - 1);
console.log(v);

v = [5, 4, 3, 2, 1];
qsort(v, 0, v.length - 1);
console.log(v);
```

**输出**

```shell
[ -1, 0, 0, 1, 1, 2, 3, 3, 4, 8, 9 ]
[]
[ 1, 2, 3, 4, 5 ]
```

