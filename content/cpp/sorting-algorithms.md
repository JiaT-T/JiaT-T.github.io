---
title: "排序算法：快速排序"
slug: "sorting-algorithms"
summary: "记录快速排序的区间划分、基准值放置和递归实现，保留对应 C++ 代码与参考链接。"
categories: ["C++", "编程基础"]
tags: ["C++", "Algorithms", "Sorting", "Quick Sort"]
date: "2026-05-30T11:44:59.000Z"
lastmod: "2026-06-11T08:55:56.000Z"
draft: false
yuque_slug: "dvq44f3av82df43l"
source: "https://www.yuque.com/u62694975/iaaa/dvq44f3av82df43l"
---

<a id="uOmph"></a>
### <span style="color: #DF2A3F">一：快速排序</span>

<a id="u55b695dd"></a>[https://zhuanlan.zhihu.com/p/63202860](<https://zhuanlan.zhihu.com/p/63202860>)

<a id="u5d2d31b8"></a>[https://zhuanlan.zhihu.com/p/642152546](<https://zhuanlan.zhihu.com/p/642152546>)

<a id="MOhOU"></a>
quickSort
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

// 统一采取 “左闭右闭” 区间
int partition(std::vector<int>& vec, int left, int right)
{
    // 选取一个基准值
    int pivot = vec[right];

    int i = left;
    // 从左往右逐个与基准值比较
    for (int j = left; j < right; j++)
    {
        // 如果当前值小于等于基准值
        // 就把更小的数(vec[j])放到前面
        // 同时将"小数值"的区域向后扩大一位
        if (vec[j] <= pivot)
        {
            std::swap(vec[i], vec[j]);
            i++;
        }
    }

    // 把基准值与第一个大于它的元素换位
    // 确保 i 左边都是小于它的元素
    // i 右边都是大于他的元素
    std::swap(vec[i], vec[right]);
    // 返回基准值的下标
    return i;
}
void quickSort(std::vector<int>& vec, int left, int right)
{
    if (left < right)
    {
        int pivotIndex = partition(vec, left, right);
        // 递归地对划分出来的左右区域进行排序
        quickSort(vec, left, pivotIndex - 1);
        quickSort(vec, pivotIndex + 1, right);
    }
}
// 对外接口
void quickSort(std::vector<int>& vec)
{
    quickSort(vec, 0, vec.size() - 1);
}

int main()
{
    std::vector<int> vec{ 9, 8, 7, 6, 5, 4, 3, 2, 1 };
    std::ranges::for_each(vec, [](const int a) {std::cout << a << " "; });
    std::cout << '\n';
    quickSort(vec);
    std::ranges::for_each(vec, [](const int a) {std::cout << a << " "; });
}
```

原文：[排序算法](<https://www.yuque.com/u62694975/iaaa/dvq44f3av82df43l>)
