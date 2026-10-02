+++
slug = "word-search"
title = "单词搜索"
problems = [79]
problem_id = 79
difficulty = "Medium"
weight = 79
summary = "单词搜索的解题思路与 C++ 实现。"
+++

题目：[单词搜索](https://leetcode.cn/problems/word-search/)


<a id="第七十九题单词搜索"></a>



使用到了<font style="background-color:#FBDE28;">深搜</font>

具体实现：

首先<u>在双层循环中判断首元素是什么，之后以这个元素为起点进行深搜</u>

dfs函数核心的判断逻辑是“found”变量那里——**只有出现一条连续的、与word匹配的元素串，found才能为真**

要注意的是，因为同一元素不能重复使用，所以在进行深搜的时候要**提前将当前元素标记为“已使用”**，这里采用的是‘\0’（不属于任何字母）

```cpp
bool dfs(vector<vector<char>>& board, string word, int index, int r, int c)
{
    if(index == word.size()) return true;
    if(r < 0 || r >= board.size() || c < 0 || c >= board[0].size() || word[index] != board[r][c]) return false;

    char temp = board[r][c];
    board[r][c] = '\0';

    bool found = dfs(board, word, index + 1, r + 1, c    ) ||
                 dfs(board, word, index + 1, r,     c + 1) ||
                 dfs(board, word, index + 1, r - 1, c    ) ||
                 dfs(board, word, index + 1, r,     c - 1);

    board[r][c] = temp;

    return found;
}
bool exist(vector<vector<char>>& board, string word)
{
    for(int j = 0; j < board[0].size(); j++)
    {
        for(int i = 0; i < board.size(); i++)
        {
            if(dfs(board, word, 0, i, j)) return true;
        }
    }
    return false;
}
```
