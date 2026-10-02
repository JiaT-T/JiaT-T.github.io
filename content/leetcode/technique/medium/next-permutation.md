+++
slug = "next-permutation"
title = "下一个排列"
problems = [31]
problem_id = 31
difficulty = "Medium"
weight = 31
summary = "下一个排列的解题思路与 C++ 实现。"
+++

题目：[下一个排列](https://leetcode.cn/problems/next-permutation/)


<a id="第三十一题"></a>



思路：<u>找到下一个排序，意思就是将当前数组视作一串数字，通过对元素的重新组合，找到</u><u><font style="background-color:#FBDE28;">第一个大于当前数字的数字</font></u>

具体实现：
	首先从后往前找到第一个逆序的数字，保存它的下标——如：123546718，这里会保存数字“4”的下标，也就是 4，之后再在 46718 这个范围内从后往前寻找第一个小于 5 的数字，并将其进行交换（123146758）；最后将46758进行降序·排序即可得到下一个排序

```cpp
void nextPermutation(vector<int>& nums)
{
    int sz = nums.size();
    if(sz <= 1) return;
    int i = sz - 1;
    while(0 < i && nums[i] <= nums[i - 1])
    {
        i--;
    }

    // 如果 i == 0，说明整个序列都是降序的（如 54321），已经是最大排列
    if(0 < i)
    {
        int j = sz - 1;
        while(nums[j] <= nums[i - 1])
        {
            j--;
        }

        std::swap(nums[i - 1], nums[j]);
    }
    std::sort(nums.begin() + i, nums.end());
}
```
