+++
slug = "spiral-matrix"
title = "螺旋矩阵"
problems = [54]
problem_id = 54
difficulty = "Medium"
weight = 54
summary = "螺旋矩阵的解题思路与 C++ 实现。"
+++

题目：[螺旋矩阵](https://leetcode.cn/problems/spiral-matrix/)


<a id="第五十四题螺旋矩阵"></a>



对res数组赋值的具体流程我放在注释里了



其实思路倒还是不难想到，就是代码实现可能需要动下脑子



这里是**定义了原矩阵的上、下、左、右边界**，而螺旋移动的情况有四种：



1.从左向右（在顶部）：相当于消去了一行，因此上边界需要收缩一行



2.从上到下（在右端）：相当于消去了一列，因此右边界收缩一列



3.从右到左（在底部）：同理，下边界向上收缩一行



4.从下到上（在左端）：同理，左边界向右收缩一列



具体的方向的控制是通过direction对4求模实现的，数字0、1、2、3对应的方向我也写在注释里了
```cpp

vector<int> spiralOrder(vector<vector<int>>& matrix)

{

    //  设一个 n * m 的矩阵

    // （第 0 行 -> 第 m - 1 列 -> 第 n - 1 行 -> 第 0 列） ->

    // （第 1 行 -> 第 m - 2 列 -> 第 n - 2 行 -> 第 1 列） ->

    // （第 2 行 -> 第 m - 3 列 -> 第 n - 3 行 -> 第 2 列） -> .....



    int rows = matrix.size();       // n

    int cols = matrix[0].size();    // m

    std::vector<int> res;

    res.reserve(rows * cols);



    int top = 0;

    int left = 0;

    int bottom = rows - 1;

    int right = cols - 1;



    int direction = 0;  // 0:右, 1:下, 2:左, 3:上



    // 只要围墙没有互相穿透，就继续走

    while(top <= bottom && left <= right)

    {

        switch(direction % 4)

        {

            case 0:

                for(int i = left; i <= right; i++)

                    res.push_back(matrix[top][i]);

                top++;

                break;



            case 1:

                for(int i = top; i <= bottom; i++)

                    res.push_back(matrix[i][right]);

                right--;

                break;



            case 2:

                for(int i = right; left <= i; i--)

                    res.push_back(matrix[bottom][i]);

                bottom--;

                break;



            case 3:

                for(int i = bottom; top <= i; i--)

                    res.push_back(matrix[i][left]);

                left++;

                break;

        }

        direction++;

    }

    return res;

}
```
