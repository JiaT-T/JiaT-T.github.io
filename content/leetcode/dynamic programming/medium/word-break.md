+++
slug = "word-break"
title = "单词拆分"
problems = [139]
problem_id = 139
difficulty = "Medium"
weight = 139
summary = "单词拆分的解题思路与 C++ 实现。"
+++

题目：[单词拆分](https://leetcode.cn/problems/word-break/)


<a id="第一百三十九题单词拆分"></a>



    1. 确定状态：dp[ i ] 代表前 i 个字符组成的字符串是否能够被拆分
    2. 状态转移：dp[ i ] = (**dp[ j ]** && **s.substr(j, i - j)**也能够被拆分)，其中 j 为区间 [ 0, i ] 的任意整数



具体实现：

首先将字典转换为无序集合，提高查找速度；原字符串拷贝至string_view类型，以实现零开销访问范围内的部分字符串；最后定义dp数组，用来记录前 i 个字符能否被拆分，注意这里的首位元素为真，因为空字符串肯定是能够被拆分的，其他位默认为假

进入循环——外层循环遍历原字符串，内层循环遍历字典；之后根据上述的 b 条件，确定字符串前i个元素是否能拆分

```cpp
bool wordBreak(string s, vector<string>& wordDict)
{
    std::unordered_set<string_view> dict(wordDict.begin(), wordDict.end());
    std::string_view sv = s;
    std::vector<bool> dp(s.size() + 1, false);
    dp[0] = true;

    for(int i = 1; i <= s.size(); i++)
    {
        for(int j = 0; j < i; j++)
        {
            if(dp[j] && dict.find(sv.substr(j, i - j)) != dict.end())
            {
                dp[i] = true;
                break;
            }
        }
    }
    return dp[s.size()];
}
```
