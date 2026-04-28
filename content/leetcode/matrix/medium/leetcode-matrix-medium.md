\#### <font style="color:#DF2A3F;">第四十八题</font>：\[旋转图像](https://leetcode.cn/problems/rotate-image/)

以矩阵的\*\*四个对角点\*\*为例（左上A，右上B，右下C，左下D），从A开始，顺序是\*\*D->A, A->B, B->C, C->D\*\*



不过这会出现一个状况，就是当 D 执行旋转之后，A 的值就已经被覆盖了，所以需要额外使用一个\*\*临时变量\*\*用于存储 A 的值，在最后的时候再覆盖到原来 B 的位置



接下来就是需要得到\*\*元素的旋转公式\*\*



如图，可以总结出元素的旋转公式是：



\_\*\*<font style="background-color:#FBDE28;">matrix </font>\*\*\_\*\*<font style="background-color:#FBDE28;">\[ </font>\*\*\_\*\*<font style="background-color:#FBDE28;">i </font>\*\*\_\*\*<font style="background-color:#FBDE28;">]\[ </font>\*\*\_\*\*<font style="background-color:#FBDE28;">j </font>\*\*\_\*\*<font style="background-color:#FBDE28;">] 原索引位置→</font>\*\*\_\*\*<font style="background-color:#FBDE28;">matrix </font>\*\*\_\*\*<font style="background-color:#FBDE28;">\[ </font>\*\*\_\*\*<font style="background-color:#FBDE28;">j </font>\*\*\_\*\*<font style="background-color:#FBDE28;">]\[ </font>\*\*\_\*\*<font style="background-color:#FBDE28;">n </font>\*\*\_\*\*<font style="background-color:#FBDE28;">−1−</font>\*\*\_\*\*<font style="background-color:#FBDE28;">i </font>\*\*\_\*\*<font style="background-color:#FBDE28;">]→旋转后索引位置</font>\*\*



之后就是按照一开始的思路进行赋值就行



唯一要注意的是循环的边界条件：0 <= i < n / 2 , 0 <= j < (n + 1) / 2



至于为什么是这样的范围：因为对于矩阵中的单个元素来说，对他进行一次旋转就相当于挪动了四个元素的位置，所以我们只需要遍历矩阵的四分之一就行了，这也就是 i，j 右边界不为n的原因



而 j 的右边界之所以是 (n + 1) / 2，是因为要考虑奇数矩阵与偶数矩阵（前者有中心元素，后者没有）



因为这里的 “ /2 ”是整数除法，所以可以确保阶数为奇数时，中心元素不进行处理

 <img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1777093405710-64126fd1-145c-43fa-9068-b3ca024e00e8.png" width="1074" title="" crop="0,0,1,1" id="YfJh3" class="ne-image">



```cpp

void rotate(vector<vector<int>>\\\& matrix)

{

\&nbsp;   int n = matrix.size();

\&nbsp;   for(int i = 0; i < n / 2; i++)

\&nbsp;   {

\&nbsp;       for(int j = 0; j < (n + 1) / 2; j++)

\&nbsp;       {

\&nbsp;           int temp = matrix\\\[i]\\\[j];

\&nbsp;           matrix\\\[i]\\\[j] = matrix\\\[n - 1 - j]\\\[i];

\&nbsp;           matrix\\\[n - 1 - j]\\\[i] = matrix\\\[n - 1 - i]\\\[n - 1 - j];

\&nbsp;           matrix\\\[n - 1 - i]\\\[n - 1 - j] = matrix\\\[j]\\\[n - 1 - i];

\&nbsp;           matrix\\\[j]\\\[n - 1 - i] = temp;

\&nbsp;       }

\&nbsp;   }

}

```



\#### <font style="color:#DF2A3F;">第五十四题</font>：\[螺旋矩阵](https://leetcode.cn/problems/spiral-matrix/)

对res数组赋值的具体流程我放在注释里了



其实思路倒还是不难想到，就是代码实现可能需要动下脑子



这里是\*\*定义了原矩阵的上、下、左、右边界\*\*，而螺旋移动的情况有四种：



1.从左向右（在顶部）：相当于消去了一行，因此上边界需要收缩一行



2.从上到下（在右端）：相当于消去了一列，因此右边界收缩一列



3.从右到左（在底部）：同理，下边界向上收缩一行



4.从下到上（在左端）：同理，左边界向右收缩一列



具体的方向的控制是通过direction对4求模实现的，数字0、1、2、3对应的方向我也写在注释里了



```cpp

vector<int> spiralOrder(vector<vector<int>>\\\& matrix)

{

\&nbsp;   //  设一个 n \\\* m 的矩阵

\&nbsp;   // （第 0 行 -> 第 m - 1 列 -> 第 n - 1 行 -> 第 0 列） -> 

\&nbsp;   // （第 1 行 -> 第 m - 2 列 -> 第 n - 2 行 -> 第 1 列） ->

\&nbsp;   // （第 2 行 -> 第 m - 3 列 -> 第 n - 3 行 -> 第 2 列） -> .....



\&nbsp;   int rows = matrix.size();       // n

\&nbsp;   int cols = matrix\\\[0].size();    // m

\&nbsp;   std::vector<int> res;

\&nbsp;   res.reserve(rows \\\* cols);



\&nbsp;   int top = 0;

\&nbsp;   int left = 0;

\&nbsp;   int bottom = rows - 1;

\&nbsp;   int right = cols - 1;



\&nbsp;   int direction = 0;  // 0:右, 1:下, 2:左, 3:上



\&nbsp;   // 只要围墙没有互相穿透，就继续走

\&nbsp;   while(top <= bottom \\\&\\\& left <= right)

\&nbsp;   {

\&nbsp;       switch(direction % 4)

\&nbsp;       {

\&nbsp;           case 0:

\&nbsp;               for(int i = left; i <= right; i++)

\&nbsp;                   res.push\\\_back(matrix\\\[top]\\\[i]);

\&nbsp;               top++;

\&nbsp;               break;



\&nbsp;           case 1:

\&nbsp;               for(int i = top; i <= bottom; i++)

\&nbsp;                   res.push\\\_back(matrix\\\[i]\\\[right]);

\&nbsp;               right--;

\&nbsp;               break;



\&nbsp;           case 2:

\&nbsp;               for(int i = right; left <= i; i--)

\&nbsp;                   res.push\\\_back(matrix\\\[bottom]\\\[i]);

\&nbsp;               bottom--;

\&nbsp;               break;



\&nbsp;           case 3:

\&nbsp;               for(int i = bottom; top <= i; i--)

\&nbsp;                   res.push\\\_back(matrix\\\[i]\\\[left]);

\&nbsp;               left++;

\&nbsp;               break;   

\&nbsp;       }

\&nbsp;       direction++;

\&nbsp;   }

\&nbsp;   return res;

}

```







\#### <font style="color:#DF2A3F;">第七十三题</font>：\[矩阵置零](https://leetcode.cn/problems/set-matrix-zeroes/)

比较暴力的方法就是：额外使用一个m\*n的矩阵，接着对原矩阵进行遍历，每次遇到零都将额外的矩阵中对应的行列置为零——时间和空间复杂度都为O(n^2)



不过我们可以使用更简单的方法



思路如下：



将第一行和第一列作为我们判断的标准，如果 \_martix\[i]\[j] \_为零，那么就相应地将\_ matrix\[i]\[0]\_ 和 \_matrix\[0]\[j]\_ 置为零。之后再通过一次遍历，如果 \_matrix\[i]\[0]\_ 和 \_matrix\[0]\[j]\_ 其中有一者为零，那么 \_martix\[i]\[j] \_也等于零



\*\*但是这样会导致一个错误\*\*，比如说，当第一行全为1，第一列全为0（除了matrix\[0]\[0])时，matrix\[0]\[0]会因为所在列存在零，而被置为零，从而导致第二次遍历时，第一行的元素因为所在行存在零而全被置为0，进而导致整个矩阵全部都为零



为了解决这个问题，我们需要提前知道第一行和第一列的情况，并单独对他们进行处理；



    - 所以先遍历第一行和第一列，看看他们是否含有零；

    - 之后再处理除了一行一列的其他行列；

    - 最后单独为一行一列赋值



```cpp

void setZeroes(vector<vector<int>>\\\& matrix)

\&nbsp;   {

\&nbsp;       const int rows = matrix.size();

\&nbsp;       const int cols = matrix\\\[0].size();

\&nbsp;       bool row\\\_has\\\_zero = false, col\\\_has\\\_zero = false;



\&nbsp;       ///////////////////////////////////////////////////////////////////////////

\&nbsp;       // 先遍历第一行和第一列

\&nbsp;       ///////////////////////////////////////////////////////////////////////////

\&nbsp;       for(int i = 0; i < cols; i++)

\&nbsp;       {

\&nbsp;           if(matrix\\\[0]\\\[i] == 0) row\\\_has\\\_zero = true;

\&nbsp;       }



\&nbsp;       for(int i = 0; i < rows; i++)

\&nbsp;       {

\&nbsp;           if(matrix\\\[i]\\\[0] == 0) col\\\_has\\\_zero = true;

\&nbsp;       }



\&nbsp;       ///////////////////////////////////////////////////////////////////////////

\&nbsp;       // 再处理除了一行一列的其他行列（注意是从1开始）

\&nbsp;       ///////////////////////////////////////////////////////////////////////////

\&nbsp;       for(int i = 1; i < rows; i++)

\&nbsp;       {

\&nbsp;           for(int j = 1; j < cols; j++)

\&nbsp;           {

\&nbsp;               if(matrix\\\[i]\\\[j] == 0)

\&nbsp;                   matrix\\\[0]\\\[j] = matrix\\\[i]\\\[0] = 0;

\&nbsp;           }

\&nbsp;       }



\&nbsp;       for(int i = 1; i < rows; i++)

\&nbsp;       {

\&nbsp;           for(int j = 1; j < cols; j++)

\&nbsp;           {

\&nbsp;               if(matrix\\\[0]\\\[j] == 0 || matrix\\\[i]\\\[0] == 0)

\&nbsp;                   matrix\\\[i]\\\[j] = 0;

\&nbsp;           }

\&nbsp;       }



\&nbsp;       ///////////////////////////////////////////////////////////////////////////

\&nbsp;       // 最后为一行一列赋值

\&nbsp;       ///////////////////////////////////////////////////////////////////////////

\&nbsp;       if(row\\\_has\\\_zero) 

\&nbsp;       {

\&nbsp;           for(int i = 0; i < cols; i++)

\&nbsp;               matrix\\\[0]\\\[i] = 0;

\&nbsp;       }

\&nbsp;       if(col\\\_has\\\_zero) 

\&nbsp;       {

\&nbsp;           for(int i = 0; i < rows; i++)

\&nbsp;               matrix\\\[i]\\\[0] = 0;

\&nbsp;       }

\&nbsp;   }

```







\#### <font style="color:#DF2A3F;">第二百四十题</font>：\[搜索二维矩阵 II](https://leetcode.cn/problems/search-a-2d-matrix-ii/)

如图，不妨将矩阵旋转45度，将其视作一个图，此时它的形式类似于一颗\_\*\*“ 二叉搜索树 ”\*\*\_（左边节点都小于当前节点，右边节点都大于当前节点），所以可以采用在二叉搜索树中使用的查找算法



具体实现：



以右上方节点为根节点，如果目标值小于当前节点，就\*\*向左移动（列数减一）\*\*；如果目标值大于当前节点，就\*\*向右移动（行数加一）\*\*。如果直到最后，也就是超出行列的边界之后都没有找到对应值，就返回false，即矩阵中不存在目标值



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1777095983585-59fd1378-3b38-4fc2-8674-cfca09005365.png" width="670" title="" crop="0,0,1,1" id="u3701ace6" class="ne-image">



```cpp

bool searchMatrix(vector<vector<int>>\\\& matrix, int target)

{

\&nbsp;   int rows = matrix.size();

\&nbsp;   int cols = matrix\\\[0].size();



\&nbsp;   int row = 0, col = cols - 1;

\&nbsp;   while(row < rows \\\&\\\& 0 <= col)

\&nbsp;   {

\&nbsp;       if(target < matrix\\\[row]\\\[col]) col--;

\&nbsp;       else if(matrix\\\[row]\\\[col] < target) row++;

\&nbsp;       else return true;

\&nbsp;   }

\&nbsp;   return false;

}

```

