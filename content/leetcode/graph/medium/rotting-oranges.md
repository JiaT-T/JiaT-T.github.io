+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "图论", "BFS", "DFS"]
date = "2026-04-12T04:30:04.000Z"
lastmod = "2026-04-13T13:02:02.000Z"
draft = false
yuque_slug = "hctg06pbe24l2mdq"
source = "https://www.yuque.com/u62694975/iaaa/hctg06pbe24l2mdq"
slug = "rotting-oranges"
title = "腐烂的橘子"
problems = [994]
problem_id = 994
difficulty = "Medium"
weight = 994
summary = "腐烂的橘子的解题思路与 C++ 实现。"
+++

题目：[腐烂的橘子](https://leetcode.cn/problems/rotting-oranges/)


<a id="第九百九十四题"></a>

<a id="ptUJw"></a>

<a id="u98fd49aa"></a>使用的是<span style="background-color: #FBDE28">广度优先搜索</span>

<a id="uef3d027b"></a>参考了这个解法：

<a id="aOiau"></a>[https://leetcode.cn/problems/rotting-oranges/solutions/2773461/duo-yuan-bfsfu-ti-dan-pythonjavacgojsrus-yfmh/?envType=study-plan-v2&amp;envId=top-100-liked](<https://leetcode.cn/problems/rotting-oranges/solutions/2773461/duo-yuan-bfsfu-ti-dan-pythonjavacgojsrus-yfmh/?envType=study-plan-v2&envId=top-100-liked>)

994. 腐烂的橘子 - 力扣（LeetCode）

994. 腐烂的橘子 - 在给定的&nbsp;m x n&nbsp;网格&nbsp;grid&nbsp;中，每个单元格可以有以下三个值之一： \* 值&nbsp;0&nbsp;代表空单元格； \* 值&nbsp;1&nbsp;代表新鲜橘子； \* 值&nbsp;2&nbsp;代表腐烂的橘子。 每分钟，腐烂的橘子&nbsp;周围&nbsp;4 个方向上相邻 的新鲜橘子都会腐烂。 返回 直到单元格中没有新鲜橘子为止所必须经过的最小分钟数。如果不可能，返回&nbsp;-1&nbsp;。 示例 1： &#91;https://assets.leetcode.cn/aliyun-lc-upload/uploads/2019/02/16/oranges.png&#93; 输入：grid = &#91;&#91;2,1,1&#93;,&#91;1,1,0&#93;,&#91;0,1,1&#93;&#93;
输出：4 示例 2： 输入：grid = &#91;&#91;2,1,1&#93;,&#91;0,1,1&#93;,&#91;1,0,1&#93;&#93;
输出：-1
解释：左下角的橘子（第 2 行， 第 0 列）永远不会腐烂，因为腐烂只会发生在 4 个方向上。 示例 3： 输入：grid = &#91;&#91;0,2&#93;&#93;
输出：0
解释：因为 0 分钟时已经没有新鲜橘子了，所以答案就是 0 。 提示： \* m == grid.length \* n == grid&#91;i&#93;.length \* 1 &lt;= m, n &lt;= 10 \* grid&#91;i&#93;&#91;j&#93; 仅为&nbsp;0、1&nbsp;或&nbsp;2

<a id="TDnDB"></a>
orangesRotting（）
```cpp
class Solution
{
public:
    int orangesRotting(vector<vector<int>>& grid)
    {
        int row = grid.size(), column = grid[0].size();
        int time = 0, fresh = 0;
        std::vector<std::pair<int, int>> oranges;

        for(int j = 0; j < column; j++)
        {
            for(int i = 0; i < row; i++)
            {
                if(grid[i][j] == 2)
                {
                    oranges.emplace_back(i, j);
                }
                else if(grid[i][j] == 1)
                {
                    fresh++;
                }
            }
        }

        while(fresh && !oranges.empty())
        {
            time++;
            std::vector<std::pair<int, int>> next;
            for(auto& [x, y] : oranges)
            {
                for(auto d : dir)
                {
                    int next_x = x + d[0], next_y = y + d[1];
                    if(0 <= next_x && next_x < row && 0 <= next_y && next_y < column && grid[next_x][next_y] == 1)
                    {
                        fresh--;
                        grid[next_x][next_y] = 2;
                        next.emplace_back(next_x, next_y);
                    }
                }
            }
            oranges = next;
        }
        return fresh ? -1 : time;
    }
private :
    int dir[4][2] = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
};
```

原文：[medium](<https://www.yuque.com/u62694975/iaaa/hctg06pbe24l2mdq>)
