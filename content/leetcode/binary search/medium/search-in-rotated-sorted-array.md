+++
slug = "search-in-rotated-sorted-array"
title = "搜索旋转排序数组"
problems = [33]
problem_id = 33
difficulty = "Medium"
weight = 33
summary = "搜索旋转排序数组的解题思路与 C++ 实现。"
+++

题目：[搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/)


<a id="第三十三题搜索旋转排序数组"></a>



一开始的想法是：先遍历一遍旋转后的数组，分别找到两个各自单调的子数组，之后对这两个数组分别进行二分查找；但这会导致线性的时间复杂度，而不是题目要求的logn

而下面这种方法就是不通过遍历，**直接在二分查找中对有序的子数组进行判断**

具体实现：

仍然是先定义左右边界（左闭右开），之后进入循环

当mid对应的值恰好与target相等时，则mid就是我们要找的下标

若是不等，则根据当前中点值与最右值得比较结果，对左数组与右数组进行选择

之后再在这两个子数组中进行二分查找

```cpp
int search(vector<int>& nums, int target)
{
    int left = 0, right = nums.size() - 1;
    while(left <= right)
    {
        int mid = left + (right - left) / 2;
        if(nums[mid] == target)
            return mid;
        else if(nums[left] <= nums[mid])
        {
            // 进入左数组
            if(nums[left] <= target && target < nums[mid])
                right = mid;
            else
                left = mid + 1;
        }
        else
        {
            //进入右数组
            if(nums[mid] < target && target <= nums[right])
                left = mid + 1;
            else
                right = mid;
        }
    }
    return -1;
}
```
