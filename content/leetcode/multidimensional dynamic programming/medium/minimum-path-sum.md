+++
slug = "minimum-path-sum"
title = "最小路径和"
problems = [64]
problem_id = 64
difficulty = "Medium"
weight = 64
summary = "最小路径和的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/gi8yqyu3poekg322"
+++

题目：[最小路径和](https://leetcode.cn/problems/minimum-path-sum/)

相关笔记：[不同路径]({{< relref "leetcode/multidimensional dynamic programming/medium/unique-paths.md" >}})


<a id="第六十四题最小路径和"></a>



和上面那题基本一样，只不过状态转移方程变成了**”dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]“**

```cpp
int minPathSum(vector<vector<int>>& grid)
{
    int r = grid.size(), c = grid[0].size();
    int dp[r][c];
    dp[0][0] = grid[0][0];
    for(int i = 1; i < r; i++) dp[i][0] = grid[i][0] + dp[i - 1][0];
    for(int i = 1; i < c; i++) dp[0][i] = grid[0][i] + dp[0][i - 1];

    for(int i = 1; i < r; i++)
    {
        for(int j = 1; j < c; j++)
        {
            dp[i][j] = std::min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j];
        }
    }
    return dp[r - 1][c - 1];
}
```




<a id="mXe6J"></a>

<strong>补充解法：一维滚动数组</strong>

```cpp
int minPathSum(vector<vector<int>>& grid)
    {
        if(grid.empty()) return 0;
        int m = grid.size(), n = grid[0].size();
        std::vector<int> dp(n, 0);

        // 初始化第一行
        dp[0] = grid[0][0];
        for(int i = 1; i < n; i++)
        {
            dp[i] = dp[i - 1] + grid[0][i];
        }

        // 填充其余行
        for(int i = 1; i < m; i++)
        {
            // 先更新每行第一个元素
            dp[0] += grid[i][0];
            for(int j = 1; j < n; j++)
            {
                dp[j] = std::min(dp[j], dp[j - 1]) + grid[i][j];
            }
        }
        return dp[n - 1];
    }
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/gi8yqyu3poekg322)
