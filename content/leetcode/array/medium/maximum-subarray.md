+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "数组"]
date = "2026-04-21T09:45:56.000Z"
lastmod = "2026-05-09T05:18:34.000Z"
draft = false
yuque_slug = "xt819i2tgf9y60tp"
source = "https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp"
slug = "maximum-subarray"
title = "最大子数组和"
problems = [53]
problem_id = 53
difficulty = "Medium"
weight = 53
summary = "最大子数组和的解题思路与 C++ 实现。"
+++

题目：[最大子数组和](https://leetcode.cn/problems/maximum-subarray/)


<a id="第五十三题"></a>

<a id="Otsui"></a>

<a id="u2f40c28a"></a>核心判断条件：

<a id="ubdb70aea"></a><strong>如果前一段子序列之和与当前元素相加之后，还没有当前元素本身大，那么就直接从当前元素开始重新计算</strong>

<a id="u053f6147"></a>具体实现：

<a id="uabdb2f4d"></a>首先定义两个和，一个用于记录目前为止的最大和（max\_val），一个用于在循环中进行判断（curr\_val）

<a id="udb81649a"></a>之后进入循环，通过上述判断条件对当前最大和进行更新，再用当前最大和与之前保持的最大和进行比较

<a id="w6FY6"></a>
maxSubArray（）
```cpp
int maxSubArray(vector<int>& nums)
{
    int curr_val = nums[0];
    int max_val = nums[0];

    for(int i = 1; i < nums.size(); i++)
    {
        if(curr_val + nums[i] < nums[i])
            curr_val = nums[i];
        else
            curr_val = curr_val + nums[i];

        if(curr_val > max_val)
            max_val = curr_val;
    }
    return max_val;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp)
