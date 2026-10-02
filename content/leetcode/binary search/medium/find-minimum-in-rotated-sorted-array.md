+++
slug = "find-minimum-in-rotated-sorted-array"
title = "寻找旋转排序数组中的最小值"
problems = [153]
problem_id = 153
difficulty = "Medium"
weight = 153
summary = "寻找旋转排序数组中的最小值的解题思路与 C++ 实现。"
+++

题目：[寻找旋转排序数组中的最小值](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/)


<a id="第一百五十三题寻找旋转排序数组中的最小值"></a>



可以将旋转后的数组视为两个并排的上升台阶，前一部分是“**高位台阶**”，后一部分是“**低位台阶**”（只有当旋转nums.size()的整数倍时才会出现前低后高的情况）

高位台阶中的每一级都大于低位台阶的最大级，也就是数组的最后一位；因此，如果<u> nums.back() < nums[mid]</u> 的话，就可以认为最小值一定在 **mid 右边**；反之，<u>nums[mid]  <= nums.back()</u> 的话，最小值就在 **mid 左边** 或 **nums[mid] 自身就是最小值**

根据这一特性，只需要比较 _x_ 和 _nums_[_n_−1] 的大小关系，就**间接地**知道了 _x_ 和数组最小值的位置关系，从而不断地缩小数组最小值所在位置的范围，二分找到数组最小值

```cpp
int findMin(vector<int>& nums)
{
    int left = 0, right = nums.size();
    while(left < right)
    {
        int mid = left + (right - left) / 2;
        if(nums[mid] <= nums.back())
            right = mid;
        else
            left = mid + 1;
    }
    return nums[left];
}
```
