+++
slug = "edit-distance"
title = "编辑距离"
problems = [72]
problem_id = 72
difficulty = "Medium"
weight = 72
summary = "编辑距离的解题思路与 C++ 实现。"
+++

题目：[编辑距离](https://leetcode.cn/problems/edit-distance/)


<a id="第七十二题编辑距离"></a>



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
