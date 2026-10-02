+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "字符串", "基础算法"]
date = "2026-03-17T07:29:04.000Z"
lastmod = "2026-05-27T03:48:13.000Z"
draft = false
yuque_slug = "trgf9fggzg79cepi"
source = "https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi"
slug = "palindrome-number"
title = "回文数"
problems = [9]
problem_id = 9
difficulty = "Easy"
weight = 9
summary = "回文数的解题思路与 C++ 实现。"
+++

题目：[回文数](https://leetcode.cn/problems/palindrome-number/)


<a id="第九题"></a>

<a id="yRBbC"></a>

<a id="u71bbcfa6"></a><span style="color: inherit">因为负数不可能为回文数，所以直接排除</span>

<a id="u74988073"></a><span style="color: inherit">之后就和之前的题目一样，把反转后的数字再与原数字比较就行</span>

<a id="ub8e73afd"></a><span style="color: inherit">（注意：这里使用int会报错--超出了类型范围，所以改用了unsigned int，因为负数在第一关就被筛掉了）</span>

<a id="kIIqv"></a>
isPalindrome()
```cpp
bool isPalindrome(int x)
    {
        if(x < 0) return false;
        unsigned int result = 0, x_copy = x;
        while(x != 0)
        {
            unsigned int a = x % 10;
            x /= 10;
            result = result * 10 + a;
        }
        if(result == x_copy)
            return true;
        return false;
    }
```

<a id="cujuE"></a>


<a id="QLYAs"></a>


<a id="AWZDC"></a>

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi)
