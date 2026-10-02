+++
slug = "longest-common-subsequence"
title = "最长公共子序列"
problems = [1143]
problem_id = 1143
difficulty = "Medium"
weight = 1143
summary = "最长公共子序列的解题思路与 C++ 实现。"
+++

题目：[最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/)


<a id="第一千一百四十三题最长公共子序列"></a>



<font style="background-color:#FBDE28;">解法一：二维数组</font>

将**两个字符串分别作为行 列以矩阵形式表示**，同时将第一行、第一列填充为0，表示空字符串

之后从(1, 1)开始进行遍历（因为i和j不是从零开始，所以之后如果要使用对应下标的text1与text2，要将i、j减一），如果<u>两个字符串的第i-1与j-1个字符相同</u>，就在矩阵对应的位置填充“dp[i - 1][j - 1] + 1”，其中**dp[i - 1][j - 1]代表着“text1的前 i 个字符与text2的前 j 个字符的最长公共子序列”**

<u>如果不同</u>，就回滚到上一个字符，取**text1的前 i-1 个字符与text2的前 j 个字符 与 text1的前 i 个字符与text2的前 j - 1 个字符**中的最大值

```cpp
int longestCommonSubsequence(string text1, string text2)
{
    int res = 0;
    int n1 = text1.size(), n2 = text2.size();
    std::vector<std::vector<int>> dp(n1 + 1, std::vector<int>(n2 + 1, 0));

    for(int i = 1; i <= n1; i++)
    {
        for(int j = 1; j <= n2; j++)
        {
            if(text1[i - 1] == text2[j - 1])
            {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            }
            else
            {
                dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[n1][n2];
}
```



<font style="background-color:#FBDE28;">解法二：一维滚动数组</font>

因为判断时只需要用到左，上，左上的三个值，所以 **一维数组 + 一个额外变量** 同样可以完成任务

dp数组第一个元素同样是零，进入循环后，先将当前元素进行保存，以供下一次循环使用（这里之所以使用 i + 1 而不是 i ，是因为第一位已经被定义为了零，所以要从第二位开始），之后根据字符是否相同更新当前位置的值——_<u>如果相同</u>_，则在上一个元素的基础上加一（代表总长度加一）；_<u>如果不同</u>_，则取dp[i + 1]（舍弃text1的当前字符）与dp[i]（舍弃text2的当前字符）中的最大值

       t[0]  t[1]  t[2]

s[0]    ✓     ✓     ✓

s[1]    ✓     ?     ✓

s[2]    ✓     ✓     ✓

总之就是记住，**<u><font style="color:#74B602;">如果想要求 ？这个格子的值，当两个字符相同时，直接将左上角的值 + 1 赋过来；如果不同，就取左边与上方元素的更大者</font></u>**

```cpp
int longestCommonSubsequence(string text1, string text2)
{
    int n1 = text1.size(), n2 = text2.size();
    std::vector<int> dp(n2 + 1);

    for(auto c : text1)
    {
        for(int i = 0, pre = 0; i < n2; i++)
        {
            int temp = dp[i + 1];
            dp[i + 1] = (c == text2[i]) ? pre + 1 : std::max(dp[i + 1], dp[i]);
            pre = temp;
        }
    }
    return dp[n2];
}
```
