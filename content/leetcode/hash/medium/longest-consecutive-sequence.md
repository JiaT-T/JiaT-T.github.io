+++
slug = "longest-consecutive-sequence"
title = "最长连续序列"
problems = [128]
problem_id = 128
difficulty = "Medium"
weight = 128
summary = "最长连续序列的解题思路与 C++ 实现。"
+++

题目：[最长连续序列](https://leetcode.cn/problems/longest-consecutive-sequence/)


<a id="第一百二十八题最长连续序列"></a>



使用到了unordered_set，它只存储key，逻辑意义是“这个元素是否存在于集合中？”

具体思路：对于一个元素，首先判断他的上一个元素（当前值减去1）是否在集合中，

    - 如果在，就意味着当前元素不是起始位置，不需要管他，直接进行下一次循环；
    - 如果不在，代表着当前元素是起始位置，然后从他开始向后遍历，直到下一个元素不存在于集合中，此时得到的长度即为连续序列的长度

每一层循环都对res进行一次比较，如果当前长度更大，就替换之前的res

```cpp
int longestConsecutive(vector<int>& nums)
{
    int res = 0;
    std::unordered_set<int> seqs(nums.begin(), nums.end());
    for(auto num : seqs)
    {
        int temp = 1;
        if(seqs.contains(num - 1))
            continue;
        while(seqs.contains(num + 1))
        {
            temp++;
            num++;
        }
        res = std::max(temp, res);
    }
    return res;
}
```
