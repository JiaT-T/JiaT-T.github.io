+++
slug = "find-all-anagrams-in-a-string"
title = "找到字符串中所有字母异位词"
problems = [438]
problem_id = 438
difficulty = "Medium"
weight = 438
summary = "找到字符串中所有字母异位词的解题思路与 C++ 实现。"
+++

题目：[找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)


<a id="第四百三十八题找到字符串中所有字母异位词"></a>



思路：从左往右移动窗口，每次移动一格；移动的过程中不断**对 left 与 right 指向的元素进行“是否存在于‘p’中“的判断**——如果存在，那么对应字符的出现频率减一.....直到最后整个哈希表清零，就可以认为这个窗口中的元素满足条件，将其存入res中
```cpp

vector<int> findAnagrams(string s, string p)

{

    int ns = s.size(), np = p.size();

    if(ns < np) return {};

    std::vector<int> res;



    std::vector<int> count(26, 0);

    for(auto c : p) count[c - 'a']++;



    int left = 0, right = 0, need = np;

    while(right < ns)

    {

        char c = s[right];

        // 扩大窗口

        if(count[c - 'a'] > 0) need--;

        count[c - 'a']--;

        right++;



        // 缩小窗口

        if(right - left > np)

        {

            char d = s[left];

            if(count[d - 'a'] >= 0) need++;

            count[d - 'a']++;

            left++;

        }



        if(need == 0) res.push_back(left);

    }

    return res;

}
```
