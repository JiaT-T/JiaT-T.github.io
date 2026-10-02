+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "双指针"]
date = "2026-04-11T05:23:52.000Z"
lastmod = "2026-06-30T04:18:45.000Z"
draft = false
yuque_slug = "ilsg74kn6vu4qdhw"
source = "https://www.yuque.com/u62694975/iaaa/ilsg74kn6vu4qdhw"
slug = "remove-element"
title = "移除元素"
problems = [27]
problem_id = 27
difficulty = "Easy"
weight = 27
summary = "移除元素的解题思路与 C++ 实现。"
+++

题目：[移除元素](https://leetcode.cn/problems/remove-element/)


<a id="第二十七题"></a>

<a id="yz2me"></a>

<a id="u52742daf"></a>解法一：

<ol data-yuque-indent="1" style="margin-left: 2em"><li id="u579eacb1"><span id="u9ff48d23">先对整个数组进行排序，将相同元素堆到一起</span></li><li id="u75357cb9"><span id="ueabdace5">然后通过两次遍历找到重复元素的起始、终止下标</span></li><li id="u4f0e98c4"><span id="uec0f0271">最后一键清除</span></li></ol>

<a id="j1OWQ"></a>
removeElement（）
```cpp
int removeElement(vector<int>& nums, int val)
{
    std::sort(nums.begin(), nums.end());
    int start = 0;
    while(start < nums.size() && nums[start] != val)
    {
        start++;
    }
    if(start == nums.size()) return nums.size();
    int end = start;
    while(end < nums.size() && nums[end] == val)
    {
        end++;
    }

    nums.erase(nums.begin() + start, nums.begin() + end);
    return nums.size();
}
```

<a id="u631fc81b"></a>解法二：
       使用到的是<strong>快慢指针</strong>

<a id="u98d76299"></a>快指针负责遍历整个数组，慢指针负责指向下一个“不等于 val”的元素的位置

<a id="u57a36819"></a>如果 fast 指向的不是 val，就将这个元素放到前面去，最后 slow 前面的元素代表的就全是“不等于 val”的数字

<a id="bGeZo"></a>
removeElement（）
```cpp
int removeElement(vector<int>& nums, int val)
{
    int slow = 0, fast = 0;
    for(; fast < nums.size(); fast++)
    {
        if(nums[fast] != val)
        {
            nums[slow] = nums[fast];
            slow++;
        }
    }
    return slow;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ilsg74kn6vu4qdhw)
