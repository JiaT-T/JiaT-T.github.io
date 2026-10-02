+++
slug = "search-a-2d-matrix"
title = "搜索二维矩阵"
problems = [74]
problem_id = 74
difficulty = "Medium"
weight = 74
summary = "搜索二维矩阵的解题思路与 C++ 实现。"
+++

题目：[搜索二维矩阵](https://leetcode.cn/problems/search-a-2d-matrix/)


<a id="第七十四题搜索二维矩阵"></a>



<font style="background-color:#FBDE28;">解法一：</font>

把二维矩阵转入一维数组，再对这个数组进行二分查找

空间、时间复杂度都为O(M * N)

```cpp
bool searchMatrix(vector<vector<int>>& matrix, int target)
{
    std::vector<int> vec;
    vec.reserve(matrix.size() * matrix[0].size());
    for(auto row : matrix)
    {
        for(auto element : row)
        {
            vec.push_back(element);
        }
    }
    return std::binary_search(vec.begin(), vec.end(), target);
}
```


 	<font style="background-color:#FBDE28;">解法二：</font>

核心公式：_<font style="color:#117CEE;">a</font>_<font style="color:#117CEE;">[ </font>_<font style="color:#117CEE;">i </font>_<font style="color:#117CEE;">]=</font>_<font style="color:#117CEE;">matrix </font>_<font style="color:#117CEE;">[ </font>_<font style="color:#117CEE;">i </font>_<font style="color:#117CEE;">/ </font>_<font style="color:#117CEE;">n </font>_<font style="color:#117CEE;">][ </font>_<font style="color:#117CEE;">i </font>_<font style="color:#117CEE;">mod </font>_<font style="color:#117CEE;">n </font>_<font style="color:#117CEE;">]</font>

实际上并不需要再开辟一个M*N的空间用于存储二维矩阵，可以直接根据一维数组下标与行列的关系找到对应元素

```cpp
bool searchMatrix(vector<vector<int>>& matrix, int target)
{
    int rows = matrix.size(), cols = matrix[0].size();
    int left = 0, right = rows * cols;
    while(left < right)
    {
        int mid = left + (right - left) / 2;
        int x = matrix[mid / cols][mid % cols];
        if(target == x)
            return true;
        else if(x < target)
            left = mid + 1;
        else if(target < x)
            right = mid;
    }
    return false;
}
```
