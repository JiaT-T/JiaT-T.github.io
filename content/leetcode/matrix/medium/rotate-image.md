+++
slug = "rotate-image"
title = "旋转图像"
problems = [48]
problem_id = 48
difficulty = "Medium"
weight = 48
summary = "旋转图像的解题思路与 C++ 实现。"
+++

题目：[旋转图像](https://leetcode.cn/problems/rotate-image/)


<a id="第四十八题旋转图像"></a>



以矩阵的**四个对角点**为例（左上A，右上B，右下C，左下D），从A开始，顺序是**D->A, A->B, B->C, C->D**



不过这会出现一个状况，就是当 D 执行旋转之后，A 的值就已经被覆盖了，所以需要额外使用一个**临时变量**用于存储 A 的值，在最后的时候再覆盖到原来 B 的位置



接下来就是需要得到**元素的旋转公式**



如图，可以总结出元素的旋转公式是：



_**<font style="background-color:#FBDE28;">matrix </font>**_**<font style="background-color:#FBDE28;">[ </font>**_**<font style="background-color:#FBDE28;">i </font>**_**<font style="background-color:#FBDE28;">][ </font>**_**<font style="background-color:#FBDE28;">j </font>**_**<font style="background-color:#FBDE28;">] 原索引位置→</font>**_**<font style="background-color:#FBDE28;">matrix </font>**_**<font style="background-color:#FBDE28;">[ </font>**_**<font style="background-color:#FBDE28;">j </font>**_**<font style="background-color:#FBDE28;">][ </font>**_**<font style="background-color:#FBDE28;">n </font>**_**<font style="background-color:#FBDE28;">−1−</font>**_**<font style="background-color:#FBDE28;">i </font>**_**<font style="background-color:#FBDE28;">]→旋转后索引位置</font>**



之后就是按照一开始的思路进行赋值就行



唯一要注意的是循环的边界条件：0 <= i < n / 2 , 0 <= j < (n + 1) / 2



至于为什么是这样的范围：因为对于矩阵中的单个元素来说，对他进行一次旋转就相当于挪动了四个元素的位置，所以我们只需要遍历矩阵的四分之一就行了，这也就是 i，j 右边界不为n的原因



而 j 的右边界之所以是 (n + 1) / 2，是因为要考虑奇数矩阵与偶数矩阵（前者有中心元素，后者没有）



因为这里的 “ /2 ”是整数除法，所以可以确保阶数为奇数时，中心元素不进行处理

 <img src="/images/leetcode-matrix-medium/leetcode-matrix-medium-01.png" width="1074" title="" crop="0,0,1,1" id="YfJh3" class="ne-image" alt="矩阵顺时针旋转 90 度时，元素位置从 [i][j] 映射到 [j][n-1-i]" loading="lazy" decoding="async" height="649">
```cpp

void rotate(vector<vector<int>>& matrix)

{

    int n = matrix.size();

    for(int i = 0; i < n / 2; i++)

    {

        for(int j = 0; j < (n + 1) / 2; j++)

        {

            int temp = matrix[i][j];

            matrix[i][j] = matrix[n - 1 - j][i];

            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j];

            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i];

            matrix[j][n - 1 - i] = temp;

        }

    }

}
```
