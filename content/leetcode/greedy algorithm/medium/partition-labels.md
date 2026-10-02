+++
slug = "partition-labels"
title = "划分字母区间"
problems = [763]
problem_id = 763
difficulty = "Medium"
weight = 763
summary = "划分字母区间的解题思路与 C++ 实现。"
+++

题目：[划分字母区间](https://leetcode.cn/problems/partition-labels/)


<a id="第七百六十三题划分字母区间"></a>



<font style="background-color:#FBDE28;">思路：</font>

记录每个字母最后出现的位置，从第一个元素开始不断进行划分，（除第一次外）每一次的起始位置都是上一次结束位置的下一个位置

之所以这么做，是因为每个相同的字母都必须出现在同一区间，也就是说划分出来的子区间至少要包含这个字母第一次出现到最后一次出现的区间；同时区间也可能出现覆盖的情况（比如 a 的区间是 [0, 8]，而 b 的区间是 [1, 7]，那么此时就要以 a 的区间为最终划分的依据，这也就是为什么记录每个元素最后一次出现的位置的原因

<font style="background-color:#FBDE28;">具体实现：</font>

首先使用一个数组得到每个字母各自的区间末端（注意不要使用哈希表或者map，这两个数据结构对链式结构很不友好，实测array的时间复杂度超过100%， map超过54%，unordered_map超过11%）

之后再通过一个循环，不断对end进行更新，直到下标走到end的位置，此时也就意味着第一个区间被划分出来了，那么就更新start，从当前end的下一个下标开始新一个区间的划分

```cpp
vector<int> partitionLabels(string s)
{
    std::array<int, 26> lastPos;
    for(int i = 0; i < s.size(); i++)
    {
        lastPos[s[i] - 'a'] = i;
    }

    std::vector<int> res;
    int start = 0, end = 0;
    for(int i = 0; i < s.size(); i++)
    {
        end = std::max(end, lastPos[s[i] - 'a']);
        if(i == end)
        {
            res.push_back(end - start + 1);
            start = end + 1;
        }
    }
    return res;
}
```
