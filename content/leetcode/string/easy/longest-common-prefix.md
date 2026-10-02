+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "字符串", "基础算法"]
date = "2026-03-17T07:29:04.000Z"
lastmod = "2026-05-27T03:48:13.000Z"
draft = false
yuque_slug = "trgf9fggzg79cepi"
source = "https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi"
slug = "longest-common-prefix"
title = "最长公共前缀"
problems = [14]
problem_id = 14
difficulty = "Easy"
weight = 14
summary = "最长公共前缀的解题思路与 C++ 实现。"
+++

题目：[最长公共前缀](https://leetcode.cn/problems/longest-common-prefix/)


<a id="第十四题"></a>

<a id="kXHuc"></a>

<a id="uf0a9421e"></a>思路：从第一个元素的第一个字符开始，先逐渐向后遍历，检查第一个字符是否都相同，然后再进行第二个字符的遍历.....直到出现不同的字符，然后返回公共前缀

<a id="u9f81048b"></a>结尾的“return strs【0】”代表着：如果循环正常结束，就说明第一个元素就是公共的前缀

<a id="f2gA1"></a>
longestCommonPrefix（）
```cpp
string longestCommonPrefix(vector<string>& strs)
    {
        if(strs.empty()) return "";

        for(int i = 0; i < strs[0].length(); i++)
        {
            for(int j = 0; j < strs.size(); j++)
            {
                if(i == strs[j].length() || strs[j][i] != strs[0][i])
                    return std::string(strs[0].substr(0, i));
            }
        }
        return strs[0];
    }
```

<a id="tb3Ir"></a>


<a id="ADPJG"></a>


<a id="rlJ4S"></a>


<a id="Xp1bE"></a>


<a id="n55JW"></a>


<a id="vfqUX"></a>


<a id="Acr0E"></a>


<a id="PZjti"></a>


<a id="FluPn"></a>


原文：[LeetCode](<https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi>)
