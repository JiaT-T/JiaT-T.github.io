+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "数组"]
date = "2026-04-21T09:45:56.000Z"
lastmod = "2026-05-09T05:18:34.000Z"
draft = false
yuque_slug = "xt819i2tgf9y60tp"
source = "https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp"
slug = "product-of-array-except-self"
title = "除了自身以外数组的乘积"
problems = [238]
problem_id = 238
difficulty = "Medium"
weight = 238
summary = "除了自身以外数组的乘积的解题思路与 C++ 实现。"
+++

题目：[除了自身以外数组的乘积](https://leetcode.cn/problems/product-of-array-except-self/)


<a id="第二百三十八题"></a>

<a id="wiZba"></a>

<a id="uf0bff13e"></a>思路如下：

<a id="u05d775e0"></a>因为不能使用除法——通过一次遍历计算整个数组的乘积，之后再进行一次遍历，每次除以当前元素的值

<a id="u24d464c0"></a>同时要求时间复杂度是O(n)，空间复杂度要求是O(1)，但是输出的数组不计入额外空间，所以需要直接对输出数组进行操作；

<a id="ub1aa922e"></a>可以先通过一次遍历计算出左边的乘积，再从后往前进行一次遍历，将右边的乘积再乘到res的当前元素上去，这样最终得到的res数组就是除自身外的元素的乘积

<a id="ua419e9af"></a>注：这里需要提前预留好res的空间，而不是在循环中每次都调用push\_back

<a id="GsEGy"></a>
productExceptSelf（）
```cpp
vector<int> productExceptSelf(vector<int>& nums)
{
    const int sz = nums.size();
    std::vector<int> res(sz);
    res[0] = 1;

    int temp = 1;
    for(int i = 0; i < sz; i++)
    {
        res[i] = temp;
        temp *= nums[i];
    }

    temp = 1;
    for(int j = sz - 1; 0 <= j; j--)
    {
        res[j] *= temp;
        temp *= nums[j];
    }

    return res;
}
```

原文：[medium](<https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp>)
