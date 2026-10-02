+++
slug = "roman-to-integer"
title = "罗马数字转整数"
problems = [13]
problem_id = 13
difficulty = "Easy"
weight = 13
summary = "罗马数字转整数的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/di3nplg5fg7crhpz"
+++

题目：[罗马数字转整数](https://leetcode.cn/problems/roman-to-integer/)


<a id="第十三题罗马数字转整数"></a>

<a id="AWZDC"></a>

<a id="u739bd817"></a>同样使用到了哈希表

<a id="u33a92af3"></a>不同的是，这次并没有将4，9等特殊数字存储进来，而是选择在后面的分支中进行处理：如果下一个字符代表的数字大于当前字符，那么就减去当前字符代表的数字（如：此次读取到了I，而下一个字符为V，也就是说这两个字符本来是连在一起的（IV：4），这是就需要减去1，而5会在下一次循环中加上去）

<a id="lbAYc"></a>
romanToInt（）
```cpp
class Solution
{
public:
    unordered_map<char, int> symbolValues =
    {
        {'I', 1},
        {'V', 5},
        {'X', 10},
        {'L', 50},
        {'C', 100},
        {'D', 500},
        {'M', 1000},
    };

    int romanToInt(string s)
    {
        int res = 0;
        int n = s.size();
        for(int i = 0; i < n; i++)
        {
            int currValue = symbolValues[s[i]];
            if (i < n - 1 && currValue < symbolValues[s[i + 1]])
                res -= currValue;
            else
                res += currValue;
        }
        return res;
    }
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/di3nplg5fg7crhpz)
