+++
slug = "set-matrix-zeroes"
title = "矩阵置零"
problems = [73]
problem_id = 73
difficulty = "Medium"
weight = 73
summary = "矩阵置零的解题思路与 C++ 实现。"
+++

题目：[矩阵置零](https://leetcode.cn/problems/set-matrix-zeroes/)


<a id="第七十三题矩阵置零"></a>



比较暴力的方法就是：额外使用一个m*n的矩阵，接着对原矩阵进行遍历，每次遇到零都将额外的矩阵中对应的行列置为零——时间和空间复杂度都为O(n^2)



不过我们可以使用更简单的方法



思路如下：



将第一行和第一列作为我们判断的标准，如果 _martix[i][j] _为零，那么就相应地将_ matrix[i][0]_ 和 _matrix[0][j]_ 置为零。之后再通过一次遍历，如果 _matrix[i][0]_ 和 _matrix[0][j]_ 其中有一者为零，那么 _martix[i][j] _也等于零



**但是这样会导致一个错误**，比如说，当第一行全为1，第一列全为0（除了matrix[0][0])时，matrix[0][0]会因为所在列存在零，而被置为零，从而导致第二次遍历时，第一行的元素因为所在行存在零而全被置为0，进而导致整个矩阵全部都为零



为了解决这个问题，我们需要提前知道第一行和第一列的情况，并单独对他们进行处理；



    - 所以先遍历第一行和第一列，看看他们是否含有零；

    - 之后再处理除了一行一列的其他行列；

    - 最后单独为一行一列赋值
```cpp

void setZeroes(vector<vector<int>>& matrix)

    {

        const int rows = matrix.size();

        const int cols = matrix[0].size();

        bool row_has_zero = false, col_has_zero = false;



        ///////////////////////////////////////////////////////////////////////////

        // 先遍历第一行和第一列

        ///////////////////////////////////////////////////////////////////////////

        for(int i = 0; i < cols; i++)

        {

            if(matrix[0][i] == 0) row_has_zero = true;

        }



        for(int i = 0; i < rows; i++)

        {

            if(matrix[i][0] == 0) col_has_zero = true;

        }



        ///////////////////////////////////////////////////////////////////////////

        // 再处理除了一行一列的其他行列（注意是从1开始）

        ///////////////////////////////////////////////////////////////////////////

        for(int i = 1; i < rows; i++)

        {

            for(int j = 1; j < cols; j++)

            {

                if(matrix[i][j] == 0)

                    matrix[0][j] = matrix[i][0] = 0;

            }

        }



        for(int i = 1; i < rows; i++)

        {

            for(int j = 1; j < cols; j++)

            {

                if(matrix[0][j] == 0 || matrix[i][0] == 0)

                    matrix[i][j] = 0;

            }

        }



        ///////////////////////////////////////////////////////////////////////////

        // 最后为一行一列赋值

        ///////////////////////////////////////////////////////////////////////////

        if(row_has_zero)

        {

            for(int i = 0; i < cols; i++)

                matrix[0][i] = 0;

        }

        if(col_has_zero)

        {

            for(int i = 0; i < rows; i++)

                matrix[i][0] = 0;

        }

    }
```
