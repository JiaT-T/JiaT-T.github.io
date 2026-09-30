---
title: "LeetCode 字符串：简单题组"
slug: "leetcode-string-easy"
summary: "记录字符串相加中的逐位计算、进位处理和 C++ 实现。"
categories: ["LeetCode"]
tags: ["LeetCode", "C++", "字符串"]
date: "2026-06-11T03:16:27.000Z"
lastmod: "2026-06-11T04:29:40.000Z"
draft: false
yuque_slug: "szdzq62cywq3al39"
source: "https://www.yuque.com/u62694975/iaaa/szdzq62cywq3al39"
problems: [415]
---

<a id="geenO"></a>
#### <span style="color: #DF2A3F">第四百一十五题</span>：[<span style="color: rgb(10, 132, 255)">字符串相加</span>](<https://leetcode.cn/problems/add-strings/>)

<a id="ua8d7a8a5"></a>从后往前对两个字符串进行处理

<a id="XsMKV"></a>
addStrings（）
```cpp
string addStrings(string num1, string num2)
{
    // 进位数字
    int carry = 0;
    int n1 = num1.size() - 1, n2 = num2.size() - 1;

    string res = "";
    // 这里的 carry 是为了处理最高位相加之后的进位情况
    while(0 <= n1 || 0 <= n2 || carry)
    {
        // 只有还有剩余数字时才取值
        int num1_c = 0 <= n1 ? num1[n1] - '0' : 0;
        int num2_c = 0 <= n2 ? num2[n2] - '0' : 0;
        int sum = num1_c + num2_c + carry;
        carry = (sum) / 10;
        res.push_back((sum % 10) + '0');
        n1--;n2--;
    }
    // 因为是从后往前处理所以最后需要进行一次翻转操作
    reverse(res.begin(), res.end());
    return res;
}
```

原文：[easy](<https://www.yuque.com/u62694975/iaaa/szdzq62cywq3al39>)
