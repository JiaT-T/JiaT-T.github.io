+++
slug = "unique-paths"
title = "不同路径"
problems = [62]
problem_id = 62
difficulty = "Medium"
weight = 62
summary = "不同路径的解题思路与 C++ 实现。"
+++

题目：[不同路径](https://leetcode.cn/problems/unique-paths/)


<a id="第六十二题不同路径"></a>



<font style="background-color:#FBDE28;">解法一：</font>

定义状态：dp[ i ][ j ] 指的是”走到点（i，j）的不同路径数量

状态转移：dp[ i ][ j ] = dp[ i - 1 ][ j ] + dp[ i ][ j - 1]，即“要想走到点(i, j)，只有两个选择——从（i-1，j）向下走，或者从（i，j-1）向右走

```cpp
int uniquePaths(int m, int n)
{
    int dp[m][n];
    for(int i = 0; i < m; i++) dp[i][0] = 1;
    for(int i = 0; i < n; i++) dp[0][i] = 1;
    for(int i = 1; i < m; i++)
    {
        for(int j = 1; j < n; j++)
        {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }
    return dp[m - 1][n - 1];
}
```

<font style="background-color:#FBDE28;">解法二：</font>

第一个方法的空间复杂度是m*n，然而在每一次的计算中，实<font style="background-color:#FBDE28;"></font>际只用到了两个元素，所以可以进行优化

只需要维护一个一维数组，dp[j]代表着当前元素，使用dp[j]自加dp[j-1]（左边的元素），等价于 dp[i][j] = dp[i - 1][j] + dp[i][j - 1]，因为**旧的dp[j]就是当前元素的上面一个元素**

```cpp
int uniquePaths(int m, int n)
{
    std::vector<int> dp(n, 1);
    for(int i = 1; i < m; i++)
    {
        for(int j = 1; j < n; j++)
        {
            dp[j] += dp[j - 1];
        }
    }
    return dp[n - 1];
}
```
