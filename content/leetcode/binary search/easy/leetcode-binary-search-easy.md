+++
title = "搜索插入位置"
problems = [35]
problem_id = 35
difficulty = "Easy"
weight = 35
summary = "搜索插入位置的解题思路与 C++ 实现。"
+++

题目：[搜索插入位置](https://leetcode.cn/problems/search-insert-position/)


<a id="第三十五题搜索插入位置"></a>



定义左闭右开区间

当left = right时，意味着值被找到了

```cpp
int searchInsert(vector<int>& nums, int target)
{
    int left = 0, right = nums.size();
    while(left < right)
    {
        int mid = left + (right - left) / 2;
        if(nums[mid] < target)
            left = mid + 1;
        else
            right = mid;
    }
    return left;
}
```
