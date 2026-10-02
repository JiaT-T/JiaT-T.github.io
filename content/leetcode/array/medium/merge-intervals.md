+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "数组"]
date = "2026-04-21T09:45:56.000Z"
lastmod = "2026-05-09T05:18:34.000Z"
draft = false
yuque_slug = "xt819i2tgf9y60tp"
source = "https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp"
slug = "merge-intervals"
title = "合并区间"
problems = [56]
problem_id = 56
difficulty = "Medium"
weight = 56
summary = "合并区间的解题思路与 C++ 实现。"
+++

题目：[合并区间](https://leetcode.cn/problems/merge-intervals/)


<a id="第五十六题"></a>

<a id="wKqUt"></a>

<a id="u3258046e"></a>思路：

<a id="u28d6402e"></a>难点在于“如何对重叠区间进行合并”，这里选用的判断条件是---如果当前区间左边界小于结果数组尾部区间的右边界，则选取两者中更大的右边界进行合并

<a id="ud472c054"></a>具体实现：

<a id="u98f74a5e"></a>首先以左边界为基准对原数组进行了排序，这样就能从左往右更好地判断是否重叠

<a id="u8621cd47"></a>这里使用到了<span style="background-color: #FBDE28">lambda表达式</span>，它的语法是：

<a id="u6346a97d"></a>// &#91;捕获列表&#93;(参数列表) -&gt;  返回值类型     { 函数体 }

<a id="ub8365dcb"></a>auto    my\_func = &#91; &#93;(int a, int b) { return a + b; };

<a id="uea2275aa"></a>但实际上，<strong>返回值类型</strong>通常可以省略，让编译器自己去猜。所以最常用的长这样：

<a id="u145689cb"></a>`[] (int a, int b) { return a + b; }`

<a id="uf057c0ee"></a>至于这里为什么是直接在res中进行修改，这是因为可以避免多次push\_back的开销

<a id="wti4B"></a>
merge（）
```cpp
vector<vector<int>> merge(vector<vector<int>>& intervals)
{
    if(intervals.empty()) return {};
    std::sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b){return a[0] < b[0];});

    vector<vector<int>> res{intervals[0]};

    for(int i = 1; i < intervals.size(); i++)
    {
        // 当前元素左边界小于等于上一个区间右边界 -->  发生重合！
        if(intervals[i][0] <= res.back()[1])
            // 取更大的有边界合并
            res.back()[1] = std::max(res.back()[1], intervals[i][1]);
        else
            res.push_back(intervals[i]);
    }
    return res;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp)
