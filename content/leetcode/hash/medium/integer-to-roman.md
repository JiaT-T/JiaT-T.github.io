+++
slug = "integer-to-roman"
title = "整数转罗马数字"
problems = [12]
problem_id = 12
difficulty = "Medium"
weight = 12
summary = "整数转罗马数字的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/di3nplg5fg7crhpz"
+++

题目：[整数转罗马数字](https://leetcode.cn/problems/integer-to-roman/)


<a id="第十二题整数转罗马数字"></a>

<a id="QLYAs"></a>

<a id="u3bee1bf5"></a>使用到的是类似哈希表的结构

<a id="ud635a40f"></a>当当前数字大于此时values中存储的值时，认为其满足“如果该值不是以 4 或 9 开头，请选择可以从输入中减去的最大值的符号，将该符号附加到结果，减去其值，然后将其余部分转换为罗马数字”的条件，需要找到此时value对应的key，拼接到res的末尾

<a id="u3597ff96"></a><strong>注意：</strong>在这里，我们将4，9，10等特殊值直接存储到哈希表结构中，因为可以原算法就是通过顺序遍历的方法进行对应值的筛选

<a id="lcPbj"></a>
intToRoman（）
```cpp
string intToRoman(int num)
    {
        std::array<int, 13> values = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
        std::array<std::string, 13> keys = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
        std::string res = "";
        for(int i = 0; i < 13; i++)
        {
            while(values[i] <= num)
            {
                num -= values[i];
                res += keys[i];
            }
        }
        return res;
    }
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/di3nplg5fg7crhpz)
