+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "字符串", "基础算法"]
date = "2026-03-17T07:29:04.000Z"
lastmod = "2026-05-27T03:48:13.000Z"
draft = false
yuque_slug = "trgf9fggzg79cepi"
source = "https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi"
slug = "reverse-integer"
title = "整数反转"
problems = [7]
problem_id = 7
difficulty = "Medium"
weight = 7
summary = "整数反转的解题思路与 C++ 实现。"
+++

题目：[整数反转](https://leetcode.cn/problems/reverse-integer/)


<a id="第七题"></a>

<a id="vjwgC"></a>

<a id="u80f4573e"></a><span style="color: inherit">通过对输入数字模10得到最低位的数字，然后将输入数字除10，减少输入数字的一位位数，使用此数字进行下一轮循环，直到输入数字最终等于零</span>

<a id="u006283f7"></a><span style="color: inherit">注意：在循环过程中，可能出现溢出的情况，因此需要在每一次循环开始前对已经反转的数字进行范围判断，如果已经溢出，则返回零</span>

<a id="OtMzj"></a>
reverse()
```cpp
int reverse(int x)
    {
        int rev = 0;
        while(x != 0)
        {
            if(rev < INT_MIN/10 || rev > INT_MAX/10) return 0;
            int d = x % 10;
            x /= 10;
            rev = rev * 10 + d;
        }
        return rev;
    }
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi)
