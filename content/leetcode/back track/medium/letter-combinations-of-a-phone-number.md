+++
slug = "letter-combinations-of-a-phone-number"
title = "电话号码的字母组合"
problems = [17]
problem_id = 17
difficulty = "Medium"
weight = 17
summary = "电话号码的字母组合的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/tvmshwlzcw3s2ta1"
+++

题目：[电话号码的字母组合](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/)


<a id="第十七题电话号码的字母组合"></a>

<a id="ADPJG"></a>

<a id="u9a74a1cf"></a>使用到的知识点是 哈希表 和 回溯算法

<a id="u58e87fe6"></a>因为未知输入字符串的长度，所以不能手动的定义for循环去暴力求解

<a id="u7847db98"></a>联想到树的结构，从一个分支一直走到底，再返回上一个最近的分支；与此题类似，以前一个字符串为基点，向后遍历每一个出现的字符，组成新的字符串。

<a id="u224db552"></a>难点在于如何回溯：这里使用到的是递归函数

<a id="u1f04fbb9"></a>根据传入的index确定当前数字，然后再根据数字在map中得到对应的字符，以每一个字符为起点，进行函数的递归调用，直到index与输入字符串长度相同

<a id="wMmcg"></a>
letterCombinations（）
```cpp
class Solution
{
public:
    void backTrack(const string& digits, int index, std::unordered_map<char, string>& phoneMap, string& combination, std::vector<string>& combinations)
    {
        if(index == digits.size())
            combinations.push_back(combination);
        else
        {
            char num = digits[index];
            const string& letters = phoneMap[num];
            for(const char& letter : letters)
            {
                combination.push_back(letter);
                backTrack(digits, index + 1, phoneMap, combination, combinations);
                combination.pop_back();
            }
        }
    }

    vector<string> letterCombinations(string digits)
    {
        if(digits.empty()) return {};
        std::unordered_map<char, string> phoneMap
        {
            {'2', "abc"},
            {'3', "def"},
            {'4', "ghi"},
            {'5', "jkl"},
            {'6', "mno"},
            {'7', "pqrs"},
            {'8', "tuv"},
            {'9', "wxyz"}
        };
        std::vector<string> combinations;
        string combination;
        backTrack(digits, 0, phoneMap, combination, combinations);
        return combinations;
    }
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/tvmshwlzcw3s2ta1)
