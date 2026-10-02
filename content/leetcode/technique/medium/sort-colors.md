+++
slug = "sort-colors"
title = "颜色分类"
problems = [75]
problem_id = 75
difficulty = "Medium"
weight = 75
summary = "颜色分类的解题思路与 C++ 实现。"
+++

题目：[颜色分类](https://leetcode.cn/problems/sort-colors/)


<a id="第七十五题颜色分类"></a>



<font style="background-color:#FBDE28;">解法一：</font>

先通过一次遍历得到红、白、蓝三个颜色各自的数量，之后再通过一次O(n)的遍历（三个循环的时间复杂度加起来是O(n) )把颜色进行排序

虽然O(2n) = O(n)，但这样还是遍历了两次，有没有只需要遍历一次的办法？

```cpp
void sortColors(vector<int>& nums)
{
    int r = 0, w = 0, b = 0;
    for(int num : nums)
    {
        switch(num)
        {
            case 0: r++; break;
            case 1: w++; break;
            case 2: b++; break;
        }
    }
    for(int i = 0; i < r; i++) nums[i] = 0;
    for(int j = r; j < r + w; j++) nums[j] = 1;
    for(int k = r + w; k < r + w + b; k++) nums[k] = 2;
}
```



解法二：
