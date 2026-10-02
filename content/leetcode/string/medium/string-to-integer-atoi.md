+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "字符串", "基础算法"]
date = "2026-03-17T07:29:04.000Z"
lastmod = "2026-05-27T03:48:13.000Z"
draft = false
yuque_slug = "trgf9fggzg79cepi"
source = "https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi"
slug = "string-to-integer-atoi"
title = "字符串转换整数 (atoi)"
problems = [8]
problem_id = 8
difficulty = "Medium"
weight = 8
summary = "字符串转换整数 (atoi)的解题思路与 C++ 实现。"
+++

题目：[字符串转换整数 (atoi)](https://leetcode.cn/problems/string-to-integer-atoi/)

相关笔记：[整数反转]({{< relref "leetcode/string/medium/reverse-integer.md" >}})


<a id="第八题"></a>

<a id="MoKD1"></a>

<a id="uff3cbf62"></a>根据题目的要求逐步实现函数功能：

<a id="u0f40be6c"></a>1.空格：读入字符串并丢弃前导空格--在循环外定义字符串下标，通过while循环判断前面的字符是否为“ ”，如果是，则i加一并进入下一次是否为空格的判断

<a id="u6481a35b"></a>2.符号：检查下一个字符为“-”还是“+”--通过if判断之后的字符有无符号，有则将sign标记为-1或1（在得出了最后的数字之后乘上），没有则默认为1

<a id="uc3171c76"></a>3.转换：跳过前置零，直至最后一个字符--这里的零不用单独写一条if语句来判断，可以通过与上一题相同的方法来解决（rev = rev \*10 + d）。要注意的是，string使用【】得出的是char类型的字符，而不是整数，需要减去‘0’才能变为int类型

<a id="ucec30b32"></a>4.舍入：范围 `[−231,  231 − 1]`--在进行转换之前需要先对上一次的计算结果进行范围判断，如果大于INT\_MAX/10或等于INT\_MAX/10但是下一位大于7，则直接返回上一次的值（原因：如果上一次的值已经大于了INT\_MAX/10，那么经过这次的循环之后，必然会超出范围；又因为最大值是`231 − 1`，因此在等于INT\_MAX的情况下，个位最大值只能是7）

<a id="jNhK5"></a>
myAtoi()
```cpp
int myAtoi(string s)
    {
        int i = 0, result = 0, sign = 1;
        while(i < s.size() && s[i] == ' ') i++;
        if(i == s.size()) return 0;
        if(s[i] == '-' || s[i] == '+')
        {
            sign = s[i] == '-' ? -1 : 1;
            i++;
        }
        while(i < s.size() && s[i] >= '0' && s[i] <= '9')
        {
            int digit = s[i] - '0';
            if(result > INT_MAX / 10 || (result == INT_MAX / 10 && digit > 7))
                return sign == 1 ? INT_MAX : INT_MIN;
            result = result * 10 + digit;
            i++;
        }
        return result * sign;
    }
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi)
