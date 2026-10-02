+++
slug = "top-k-frequent-elements"
title = "前 K 个高频元素"
problems = [347]
problem_id = 347
difficulty = "Medium"
weight = 347
summary = "前 K 个高频元素的解题思路与 C++ 实现。"
+++

题目：[前 K 个高频元素](https://leetcode.cn/problems/top-k-frequent-elements/)


<a id="第三百四十七题前-k-个高频元素"></a>



思路：先使用**<u>哈希表</u>**将每个数字与出现频率对应，再通过频率大小在**<u>最小堆</u>**中筛选出前 k 个高频元素，最后将堆中的频率对应的数字存入**<u>数组</u>**并输出

唯一要注意的是 pq 中存储的元素，**不能只存储频率，而是要将频率与对应的数字绑定**，不然最后会导致只知道”前 k 大的频率“，而不是”前 k 个高频元素“；这里使用的是 pair，比较器只会比较频率的大小，这样我们就能找到频率所对应的元素，并将其存入 res 数组

```cpp
vector<int> topKFrequent(vector<int>& nums, int k)
{
    std::unordered_map<int, int> um;
    for(int num : nums)
    {
        um[num]++;
    }

    auto cmp = [](const std::pair<int, int>& a, const std::pair<int, int>& b)
    {
        return b.first < a.first;
    };
    std::priority_queue<std::pair<int, int>, vector<std::pair<int, int>>, decltype(cmp)> pq;
    for(const auto& pair : um)
    {
        pq.emplace(pair.second, pair.first);
        if(k < pq.size())
            pq.pop();
    }

    std::vector<int> res;
    res.reserve(k);
    while(!pq.empty())
    {
        res.push_back(pq.top().second);
        pq.pop();
    }
    return res;
}
```
