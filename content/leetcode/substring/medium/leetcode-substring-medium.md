+++
title = "和为 K 的子数组"
slug = "leetcode-substring-medium"
summary = "和为 K 的子数组的解题思路与 C++ 实现。"
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "子串", "前缀和", "哈希表"]
date = "2026-05-04T04:06:55.000Z"
lastmod = "2026-05-26T01:41:00.000Z"
draft = false
yuque_slug = "hhhgyq3wipki294y"
source = "https://www.yuque.com/u62694975/iaaa/hhhgyq3wipki294y"
problems = [560]
problem_id = 560
difficulty = "Medium"
weight = 560
+++

题目：[和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/)


<a id="第五百六十题"></a>

<a id="cAdBv"></a>

<a id="u04780ee9"></a><span style="background-color: #FBDE28">解法一：暴力解法</span>

<a id="u49ace54c"></a>使用双层循环，每次从当前位置向后遍历，直到总和等于目标值（res加一）

<a id="PiARQ"></a>
subarraySum（）
```cpp
int subarraySum(vector<int>& nums, int k)
{
    int n = nums.size();
    int res = 0;
    for(int i = 0; i < n; i++)
    {
        int sum = 0;
        for(int j = i; j < n; j++)
        {
            sum += nums[j];
            if(sum == k)
            {
                res++;
                continue;
            }
        }
    }
    return res;
}
```

<a id="u1dfeb752"></a><span style="background-color: #FBDE28">解法二：前缀和</span>

<a id="ua2b17c86"></a>思路：使用一张哈希表记录之前出现的和以及对应的次数，当前连续子序列长度为sum（从头一直加到尾），<strong><u>如果能够在第 j 个元素的位置，找到在前 j 个元素中，和为 sum - k 的连续子数组，那么从 j 到 i 的这段子数组的和就一定等于 k （k = sum - （sum - k））</u></strong>

<a id="u8c06763b"></a><strong><u>更简单的理解是：使用哈希表记录每个元素的前缀和，并统计所有相同前缀和的出现次数；当我们遍历到第 j 个元素时，此时需要查找在【0，j】范围内，是否存在子数组之和为 k——等价于在【0，j - 1】范围内，是否存在子数组之和为 sum - k，因为我们已经直到以 j 为结尾的前缀和为 sum，只需要减去 （sum - k），所得到的子数组之和就为 k</u></strong>

<a id="SIeDT"></a>
subarraySum（）
```cpp
int subarraySum(vector<int>& nums, int k)
{
    std::unordered_map<int, int> prefixCount;
    prefixCount[0] = 1;

    int res = 0, sum = 0;
    for(auto num : nums)
    {
        sum += num;
        if(prefixCount.count(sum - k))
        {
            res += prefixCount[sum - k];
        }
        prefixCount[sum]++;
    }
    return res;
}
```

原文：[medium](<https://www.yuque.com/u62694975/iaaa/hhhgyq3wipki294y>)
