+++
title = "最小覆盖子串"
slug = "leetcode-substring-hard"
summary = "最小覆盖子串的解题思路与 C++ 实现。"
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "子串", "滑动窗口"]
date = "2026-06-03T04:09:47.000Z"
lastmod = "2026-06-03T04:39:14.000Z"
draft = false
yuque_slug = "pexszspw259pqf38"
source = "https://www.yuque.com/u62694975/iaaa/pexszspw259pqf38"
problems = [76]
problem_id = 76
difficulty = "Hard"
weight = 76
+++

题目：[最小覆盖子串](https://leetcode.cn/problems/minimum-window-substring/)


<a id="第七十八题"></a>

<a id="iGpGa"></a>

<a id="Y69po"></a>
minWindow（）
```cpp
string minWindow(string s, string t)
{
    if(s.size() < t.size()) return "";

    std::vector<int> need(128, 0);
    std::vector<int> window(128, 0);

    // 统计 t 中出现的所有字符种类数量（total_kinds）
    int total_kinds = 0;
    for(char c : t)
    {
        if(need[c] == 0) total_kinds++;
        // 统计 t 中每个字符的出现次数
        need[c]++;
    }

    // 窗口的左右边界（窗口是在 s 中进行滑动）
    int left = 0, right = 0;
    // 最小覆盖子串的起始字符以及长度
    int start = 0, min_length = INT_MAX;
    // 窗口中的满足 t 条件数的字符数量
    int valid = 0;
    while(right < s.size())
    {
        // 提取右边界字符
        char c = s[right];
        // 扩大窗口
        right++;

        // 只有当 t 中也包含当前字符时
        // 才进行后续的“更新 window”、“判断有效字符数量”的操作
        if(need[c] != 0)
        {
            // window 数组中对应的字符出现次数加 1
            window[c]++;
            // 当 window 中此字符的出现次数与 t 中一样时
            // 就可以认为这个字符已经满足了条件
            // 有效字符加 1
            if(window[c] == need[c])
                valid++;
        }

        // 当所有字符都已经满足“出现次数”的条件时
        while(valid == total_kinds)
        {
            // 如果此时子串长度小于之前记录的长度
            // 就更新最小长度
            if(right - left < min_length)
            {
                start = left;
                min_length = right - left;
            }

            char d = s[left];
            // 左边界收缩
            left++;

            // 如果当前字符在 t 中出现过
            if(need[d] != 0)
            {
                // 同时如果此字符是一个“满足条件”的字符
                // 就将有效字符数减 1（因为左边界收缩之后，这个字符就被抛弃了）
                if(window[d] == need[d])
                    valid--;
                // 它在窗口中的出现次数也要减 1
                window[d]--;
            }
        }
    }
    // 如果最终 min_length 都没有被改变的话
    // 说明根本就没有进入循环，此时直接返回空字符串
    return min_length == INT_MAX ? "" : s.substr(start, min_length);
}
```

原文：[hard](<https://www.yuque.com/u62694975/iaaa/pexszspw259pqf38>)
