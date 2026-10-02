+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "图论", "BFS", "DFS"]
date = "2026-04-12T04:30:04.000Z"
lastmod = "2026-04-13T13:02:02.000Z"
draft = false
yuque_slug = "hctg06pbe24l2mdq"
source = "https://www.yuque.com/u62694975/iaaa/hctg06pbe24l2mdq"
slug = "number-of-islands"
title = "岛屿数量"
problems = [200]
problem_id = 200
difficulty = "Medium"
weight = 200
summary = "岛屿数量的解题思路与 C++ 实现。"
+++

题目：[岛屿数量](https://leetcode.cn/problems/number-of-islands/)


<a id="第二百题"></a>

<a id="kjiXc"></a>

<a id="uea8ea19c"></a>使用的是<span style="background-color: #FBDE28">深度优先搜素</span>

<a id="u527e94a3"></a>主要思路：对输入的二维数组进行遍历，如果遇到一，则认为遇到了一个新的岛屿，然后对这个1周围上下左右四个元素进行搜索；如果周围元素仍然是1，就可以认为它与上一个区域位于同一个岛屿，并再次以当前这个一为起点，调用DFS函数递归搜索

<a id="u12008625"></a>DFS函数的终止条件是遇到零，因此每当遍历完成一个‘1’时，都要将其设置为‘0’，避免重复搜索导致栈溢出

<a id="DqTbJ"></a>
numIslands（）
```cpp
class Solution
{
public:
    void DFS(vector<vector<char>>& grid, int x, int y)
    {
        for(int k = 0; k < 4; k++)
        {
            int next_x = x + dir[k][0];
            int next_y = y + dir[k][1];

            if(next_x < 0 || next_x >= grid.size()) continue;
            if(next_y < 0 || next_y >= grid[0].size()) continue;
            if(grid[next_x][next_y] == '1')
            {
                grid[next_x][next_y] = '0';
                DFS(grid, next_x, next_y);
            }
        }
    }

    int numIslands(vector<vector<char>>& grid)
    {
        int   m = grid.size();     // row
        int   n = grid[0].size();  // column
        int res = 0;

        for(int i = 0; i < m; i++)
        {
            for(int j = 0; j < n; j++)
            {
                if(grid[i][j] == '1')
                {
                    res++;
                    grid[i][j] = '0';
                    DFS(grid, i, j);
                }
            }
        }
        return res;
    }
private :
    int dir[4][2] = {0, 1, 1, 0, -1, 0, 0, -1};
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/hctg06pbe24l2mdq)
