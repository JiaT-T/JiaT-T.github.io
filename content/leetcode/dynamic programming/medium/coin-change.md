+++
slug = "coin-change"
title = "零钱兑换"
problems = [322]
problem_id = 322
difficulty = "Medium"
weight = 322
summary = "零钱兑换的解题思路与 C++ 实现。"
+++

题目：[零钱兑换](https://leetcode.cn/problems/coin-change/)


<a id="第三百二十二题零钱兑换"></a>



确定状态：dp[ i ]代表 为了凑出 i 元，所需要的硬币数量

状态转移：dp[ i ] = min(dp[ i ], dp[ i - coin ] + 1)，即金额 i 的最优解，必然是由某个较小的金额 **i - coin** 转移而来的。

```cpp
int coinChange(vector<int>& coins, int amount)
{
    std::vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;

    for(int i = 1; i <= amount; i++)
    {
        for(auto coin :coins)
        {
            if(coin <= i)
                dp[i] = std::min(dp[i], dp[i - coin] + 1);
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```
