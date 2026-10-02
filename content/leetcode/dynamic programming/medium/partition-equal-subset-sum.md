+++
slug = "partition-equal-subset-sum"
title = "分割等和子集"
problems = [416]
problem_id = 416
difficulty = "Medium"
weight = 416
summary = "分割等和子集的解题思路与 C++ 实现。"
+++

题目：[分割等和子集](https://leetcode.cn/problems/partition-equal-subset-sum/)


<a id="第四百一十六题分割等和子集"></a>



```cpp
bool canPartition(vector<int>& nums)
{
    int sum = reduce(nums.begin(), nums.end());
    if(sum % 2 != 0) return false;
    sum /= 2;

    int n = nums.size();
    std::vector<bool> dp(sum + 1, false);
    dp[0] = true;
    for(int num : nums)
    {
        for(int i = sum; num <= i; i--)
        {
            if(dp[i - num]) dp[i] = true;
        }
        if(dp[sum]) return true;
    }
    return dp[sum];
}
```
