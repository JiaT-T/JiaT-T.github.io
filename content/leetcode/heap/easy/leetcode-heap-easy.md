+++
title = "库存管理 III"
slug = "leetcode-heap-easy"
summary = "库存管理 III的解题思路与 C++ 实现。"
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "堆"]
date = "2026-05-25T10:57:48.000Z"
lastmod = "2026-05-25T10:59:58.000Z"
draft = false
yuque_slug = "yqdwdfptic3ez88z"
source = "https://www.yuque.com/u62694975/iaaa/yqdwdfptic3ez88z"
problems = ["LCR 159"]
problem_id = "LCR 159"
difficulty = "Easy"
weight = 159
+++

题目：[库存管理 III](https://leetcode.cn/problems/zui-xiao-de-kge-shu-lcof/)


<a id="第一百五十九题"></a>

<a id="pjWBH"></a>

<a id="u64e1cbf1"></a>使用内置的函数 nth\_element（）

<a id="u5fa5023c"></a>难绷

<a id="QAIzJ"></a>
inventoryManagement（）
```cpp
vector<int> inventoryManagement(vector<int>& stock, int cnt)
{
    if(stock.empty() || cnt == 0) return {};

    std::nth_element(stock.begin(), stock.begin() + cnt, stock.end());

    std::vector<int> res(stock.begin(), stock.begin() + cnt);
    return res;
}
```

原文：[easy](<https://www.yuque.com/u62694975/iaaa/yqdwdfptic3ez88z>)
