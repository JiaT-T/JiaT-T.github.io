+++
slug = "group-anagrams"
title = "字母异位词分组"
problems = [49]
problem_id = 49
difficulty = "Medium"
weight = 49
summary = "字母异位词分组的解题思路与 C++ 实现。"
+++

题目：[字母异位词分组](https://leetcode.cn/problems/group-anagrams/)


<a id="第四十九题字母异位词分组"></a>



实现思路：记录每个字符串中单个字母的出现频率，并以字符串形式存储起来（如”0110200000....")，可以提前将字符串的空间预留26位（对应26个字母），然后将这个字符串作为哈希表的key，用来查找表中存储着异位词的vector值

```cpp
vector<vector<string>> groupAnagrams(vector<string>& strs)
{
    std::vector<vector<string>> res;
    std::unordered_map<string, std::vector<string>> um_pair;
    for(auto& str : strs)
    {
        string count(26, 0);
        for(auto& c : str)
        {
            count[c - 'a'] += 1;
        }
        um_pair[count].push_back(str);
    }
    for(auto& pair : um_pair)
    {
        res.push_back(pair.second);
    }
    return res;
}
```
