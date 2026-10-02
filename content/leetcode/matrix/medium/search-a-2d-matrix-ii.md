+++
slug = "search-a-2d-matrix-ii"
title = "搜索二维矩阵 II"
problems = [240]
problem_id = 240
difficulty = "Medium"
weight = 240
summary = "搜索二维矩阵 II的解题思路与 C++ 实现。"
+++

题目：[搜索二维矩阵 II](https://leetcode.cn/problems/search-a-2d-matrix-ii/)


<a id="第二百四十题搜索二维矩阵-ii"></a>



如图，不妨将矩阵旋转45度，将其视作一个图，此时它的形式类似于一颗_**“ 二叉搜索树 ”**_（左边节点都小于当前节点，右边节点都大于当前节点），所以可以采用在二叉搜索树中使用的查找算法



具体实现：



以右上方节点为根节点，如果目标值小于当前节点，就**向左移动（列数减一）**；如果目标值大于当前节点，就**向右移动（行数加一）**。如果直到最后，也就是超出行列的边界之后都没有找到对应值，就返回false，即矩阵中不存在目标值



<img src="/images/leetcode-matrix-medium/leetcode-matrix-medium-02.png" width="670" title="" crop="0,0,1,1" id="u3701ace6" class="ne-image" alt="有序矩阵与搜索图的对应关系，以及从右上角向较小或较大元素移动的方向" loading="lazy" decoding="async" height="495">
```cpp

bool searchMatrix(vector<vector<int>>& matrix, int target)

{

    int rows = matrix.size();

    int cols = matrix[0].size();



    int row = 0, col = cols - 1;

    while(row < rows && 0 <= col)

    {

        if(target < matrix[row][col]) col--;

        else if(matrix[row][col] < target) row++;

        else return true;

    }

    return false;

}
```
