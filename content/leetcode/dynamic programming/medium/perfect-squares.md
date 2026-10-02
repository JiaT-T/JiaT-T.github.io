+++
slug = "perfect-squares"
title = "完全平方数"
problems = [279]
problem_id = 279
difficulty = "Medium"
weight = 279
summary = "完全平方数的解题思路与 C++ 实现。"
+++

题目：[完全平方数](https://leetcode.cn/problems/perfect-squares/)


<a id="第二百七十九题完全平方数"></a>



定义了一个数组，用来存储n之前每一个元素的完全平方数的最少数量，这样就得到了状态转移方程：

$ dp[i] = 1 + \min_{1 \le j^2 \le i} \{ dp[i - j^2] \} $

其中，i 是从1到 n 的所有数字，j^2是小于等于 i 的所有完全平方数

每次当 n 减去 i 之后，都会以 i 为右边界进行一次遍历，此时就是对每一个 i 进行”局部穷举“，看看此时有哪些组成 j^2 的最少数字数量，我们会选取最小的作为当前的结果

```cpp
int numSquares(int n)
{
    std::vector<int> f(n + 1);
    for(int i = 1; i <= n; i++)
    {
        int minn = INT_MAX;
        for(int j = 1; j * j <= i; j++)
            minn = std::min(minn, f[i - j * j]);

        f[i] = minn + 1;
    }
    return f[n];
}
```
