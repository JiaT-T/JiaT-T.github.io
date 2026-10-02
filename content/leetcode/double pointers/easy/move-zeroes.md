+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "双指针"]
date = "2026-04-11T05:23:52.000Z"
lastmod = "2026-06-30T04:18:45.000Z"
draft = false
yuque_slug = "ilsg74kn6vu4qdhw"
source = "https://www.yuque.com/u62694975/iaaa/ilsg74kn6vu4qdhw"
slug = "move-zeroes"
title = "移动零"
problems = [283]
problem_id = 283
difficulty = "Easy"
weight = 283
summary = "移动零的解题思路与 C++ 实现。"
+++

题目：[移动零](https://leetcode.cn/problems/move-zeroes/)


<a id="第二百八十三题"></a>

<a id="GlvDn"></a>

<a id="uf68262a9"></a>思路：使用两个指针，一个从前往后对数组进行遍历，另一个始终指向前端的非零元素；只要指针 i 指向的元素非零，就将指针 k 当前指向的元素赋值为 num&#91;i&#93; ，最后再将指针 k 后面的元素全部置为零即可

<a id="QKl0t"></a>
moveZeroes（）
```cpp
void moveZeroes(vector<int>& nums)
{
    int k = 0;
    for(int i = 0; i < nums.size(); i++)
    {
        if(nums[i] != 0)
        {
            nums[k] = nums[i];
            k++;
        }
    }
    for(int j = k; j < nums.size(); j++)
    {
        nums[j] = 0;
    }
}
```

原文：[easy](<https://www.yuque.com/u62694975/iaaa/ilsg74kn6vu4qdhw>)
