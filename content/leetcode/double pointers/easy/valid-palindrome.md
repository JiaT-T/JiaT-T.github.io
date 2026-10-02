+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "双指针"]
date = "2026-04-11T05:23:52.000Z"
lastmod = "2026-06-30T04:18:45.000Z"
draft = false
yuque_slug = "ilsg74kn6vu4qdhw"
source = "https://www.yuque.com/u62694975/iaaa/ilsg74kn6vu4qdhw"
slug = "valid-palindrome"
title = "验证回文串"
problems = [125]
problem_id = 125
difficulty = "Easy"
weight = 125
summary = "验证回文串的解题思路与 C++ 实现。"
+++

题目：[验证回文串](https://leetcode.cn/problems/valid-palindrome/)


<a id="第一百二十五题"></a>

<a id="pwggh"></a>

<a id="qZpKX"></a>
isPalindrome（）
```cpp
bool isPalindrome(string s)
{
    if(s.size() == 1) return true;
    // 定义左右指针
    int left = 0, right = s.size() - 1;
    // 不需要考虑 left = right 的情况
    // 因为中间多一个字符的情况可以直接当作偶数串处理
    while(left < right)
    {
        // 拿到左边的数字或字符
        while(left < right && !isalnum(s[left]))
        {
            left++;
        }

        // 拿到右边的数字或字符
        while(left < right && !isalnum(s[right]))
        {
            right--;
        }

        // 如果是大写就将其转换为小写
        // 如果已经是小写或数字就原样返回
        if(std::tolower(s[left]) != std::tolower(s[right])) return false;
        // 移动指针
        left++;right--;
    }
    return true;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ilsg74kn6vu4qdhw)
