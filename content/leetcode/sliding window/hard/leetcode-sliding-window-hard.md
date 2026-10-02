+++
title = "滑动窗口最大值"
slug = "leetcode-sliding-window-hard"
summary = "滑动窗口最大值的解题思路与 C++ 实现。"
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "滑动窗口", "单调队列"]
date = "2026-05-30T02:42:58.000Z"
lastmod = "2026-05-30T02:43:42.000Z"
draft = false
yuque_slug = "nkkgc4p5l9qyiauc"
source = "https://www.yuque.com/u62694975/iaaa/nkkgc4p5l9qyiauc"
problems = [239]
problem_id = 239
difficulty = "Hard"
weight = 239
+++

题目：[滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/)


<a id="第二百三十九题"></a>

<a id="dH8b1"></a>

<a id="TymbF"></a>
maxSlidingWindow（）
```cpp
vector<int> maxSlidingWindow(vector<int>& nums, int k)
{
    int n = nums.size();
    std::vector<int> res(n - k + 1);
    std::deque<int> dq;

    for(int i = 0; i < n; i++)
    {
        while(!dq.empty() && nums[dq.back()] <= nums[i])
        {
            dq.pop_back();
        }
        dq.push_back(i);

        int left = i - k + 1;
        if(dq.front() < left)
        {
            dq.pop_front();
        }

        if(0 <= left)
        {
            res[left] = (nums[dq.front()]);
        }
    }
    return res;
}
```

原文：[hard](<https://www.yuque.com/u62694975/iaaa/nkkgc4p5l9qyiauc>)
