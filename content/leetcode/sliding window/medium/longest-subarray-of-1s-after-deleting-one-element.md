+++
slug = "longest-subarray-of-1s-after-deleting-one-element"
title = "删掉一个元素以后全为 1 的最长子数组"
problems = [1493]
problem_id = 1493
difficulty = "Medium"
weight = 1493
summary = "删掉一个元素以后全为 1 的最长子数组的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/yg57x00m0sytet7u"
+++

题目：[删掉一个元素以后全为 1 的最长子数组](https://leetcode.cn/problems/longest-subarray-of-1s-after-deleting-one-element/)


<a id="第一千四百九十三题删掉一个元素以后全为-1-的最长子数组"></a>

<a id="eN0b2"></a>

<strong>原笔记（代码待复核）</strong>



<a id="uffe18c70"></a>维护一个滑动窗口，窗口内只能存在一个零，同时每一步都动态更新最长子数组的长度

<a id="u6312f1b2"></a>当窗口内零的数量大于一时，将左边界右移，直到零的数量变为一

<a id="on0TP"></a>
longestSubarray（）
```cpp
int longestSubarray(vector<int>& nums)
{
    int left = 0, zero_count = 0, res = 0;

    for(int right = 0; right < nums.size(); right++)
    {
        if(nums[right] == 0)
            zero_count++;

        while(1 < zero_count)
        {
            if(nums[left] == 0)
                zero_count--;

            left++;
        }

        res = std::max(right - left + 1 - 1,);
    }
    return res;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/yg57x00m0sytet7u)
