+++
slug = "pascals-triangle"
title = "杨辉三角"
problems = [118]
problem_id = 118
difficulty = "Easy"
weight = 118
summary = "杨辉三角的解题思路与 C++ 实现。"
+++

题目：[杨辉三角](https://leetcode.cn/problems/pascals-triangle/)


<a id="第一百一十八题杨辉三角"></a>



[1]

[1,1]

[1,2,1]

[1,3,3,1]

[1,4,6,4,1]

把左端对齐，以符合二维数组的格式

根据杨辉三角的定义，可以知道，当前元素的值，等于左上方元素加正上方的元素，也就是

**v[i][j] = v[i-1][j-1] + v[i-1][j]**

又因为每一层的大小都比上一层多一个，所以每次循环都需要对数组向后扩容一位，并将所有元素初始化为1**
**

```cpp
vector<vector<int>> generate(int numRows)
    {
        std::vector<std::vector<int>> vec(numRows);
        for(int i = 0; i < numRows; i++)
        {
            vec[i].resize(i+1, 1);
            for(int j = 1; j < i; j++)
            {
                vec[i][j] = vec[i-1][j-1] + vec[i-1][j];
            }
        }
        return vec;
    }
```
