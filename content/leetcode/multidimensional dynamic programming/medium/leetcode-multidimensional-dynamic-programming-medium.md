+++
title = "62、64、72、1143"
problems = [62, 64, 72, 1143]
+++

#### <font style="color:#DF2A3F;">第六十二题</font>：[不同路径](https://leetcode.cn/problems/unique-paths/)
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



#### <font style="color:#DF2A3F;">第六十四题</font>：[最小路径和](https://leetcode.cn/problems/minimum-path-sum/)
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



#### <font style="color:#DF2A3F;">第七十二题</font>：[编辑距离](https://leetcode.cn/problems/edit-distance/)
和下面一题差不多，需要处理的只有两种情况——字符相同与不相同

1.<u>相同</u>：此时不需要进行任何处理，**直接与上一次的结果保持相同即可（dp[i][j] = dp[i - 1][j - 1]）**

2.<u>不相同</u>：这是问题最核心的地方，此时对于两个字符串中的两个字符，**有三种处理方法——插入，删除，替换**；其中，

**插入**代表“在当前长度下的word1的末尾插入word2的当前字符”，对应代码为 dp[i][j-1] + 1；

**删除**代表“删除当前长度下的word1的最后一个字符”，对应代码为 dp[i-1][j] + 1；

**替换**代表“将当前长度下的word1的最后一个字符替换为当前长度下的word2的尾字符”对应代码为dp[i - 1][j] + 1

在执行完三个操作后，会分别产生三个不同规模的子问题，我们需要**选取其中规模最小的子问题 : std::min()**

+ **左上** = 替换
+ **上** = 删除（word1 少一个）
+ **左** = 插入（word2 少一个）

        j-1 	  j

i-1   左上   上

i      左   	 ?

```cpp
int minDistance(string word1, string word2)
{
    int n1 = word1.size(), n2 = word2.size();
    std::vector<std::vector<int>> dp(n1 + 1, vector<int>(n2 + 1));
    for(int i = 0; i <= n1; i++) dp[i][0] = i;
    for(int j = 0; j <= n2; j++) dp[0][j] = j;

    for(int i = 1; i <= n1; i++)
    {
        for(int j = 1; j <= n2; j++)
        {
            if(word1[i - 1] == word2[j - 1])
            {
                dp[i][j] = dp[i - 1][j - 1];
            }
            else
            {
                dp[i][j] = std::min(dp[i - 1][j], std::min(dp[i - 1][j - 1], dp[i][j - 1])) + 1;
            }
        }
    }
    return dp[n1][n2];
}
```



#### <font style="color:#DF2A3F;">第一千一百四十三题</font>：[最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/)
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




