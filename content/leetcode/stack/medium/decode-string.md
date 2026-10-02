+++
slug = "decode-string"
title = "字符串解码"
problems = [394]
problem_id = 394
difficulty = "Medium"
weight = 394
summary = "字符串解码的解题思路与 C++ 实现。"
+++

题目：[字符串解码](https://leetcode.cn/problems/decode-string/)


<a id="第三百九十四题字符串解码"></a>



使用到的是栈和递归

关于为什么是遇到‘【’就继续入栈：这是为了处理前置的字母，可以将其直接拼接到res的尾部

```cpp
string decodeString(string s)
{
    std::stack<std::pair<string, int>> stk;
    string res;
    int k = 0;
    for(char c : s)
    {
        if(isalpha(c)) res += c;
        else if(isdigit(c)) k = k * 10 + (c - '0');
        else if(c == '[')
        {
            stk.emplace(std::move(res), k);
            k = 0;
        }
        else
        {
            auto [pre_res, pre_k] = stk.top();
            stk.pop();
            while(pre_k--)
            {
                pre_res += res;
            }
            res = std::move(pre_res);
        }
    }
    return res;
}
```
