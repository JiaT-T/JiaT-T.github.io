+++
slug = "house-robber"
title = "打家劫舍"
problems = [198]
problem_id = 198
difficulty = "Medium"
weight = 198
summary = "打家劫舍的解题思路与 C++ 实现。"
+++

题目：[打家劫舍](https://leetcode.cn/problems/house-robber/)


<a id="第一百九十八题打家劫舍"></a>



1.状态定义：

dp[i]指的是”到达第i个房子时，目前为止能偷到的最大金额是多少“

2.转移方程：

用一个例子来解释——

假如当前已经偷完了前3栋房子，来到了第四栋房子（里面有num元）

那么现在就有两个选择：

1).不偷第四栋房子，那么金额就是dp[3]（也就是前三栋房子的最优结果）

2).偷第四栋房子，那么总金额就是dp[i-1] + num（前两栋房子的最优结果加上第四栋房子）

因此，前四栋房子的最大金额就是两者中的更大者

```cpp
int rob(vector<int>& nums)
{
    int pre = 0, curr = 0;
    int temp;
    for(int num : nums)
    {
        temp = curr;
        curr = std::max(pre + num, curr);
        pre = temp;
    }
    return curr;
}
```
