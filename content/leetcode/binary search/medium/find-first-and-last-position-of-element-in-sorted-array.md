+++
slug = "find-first-and-last-position-of-element-in-sorted-array"
title = "在排序数组中查找元素的第一个和最后一个位置"
problems = [34]
problem_id = 34
difficulty = "Medium"
weight = 34
summary = "在排序数组中查找元素的第一个和最后一个位置的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/kovh86nqrne4grtx"
+++

题目：[在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)


<a id="第三十四题在排序数组中查找元素的第一个和最后一个位置"></a>



**lowerBound函数**：返回第一个 >= target的数的下标

<u>实现原理</u>：内部是一个while循环，当循环结束时，应当恰好有 left = right 成立，此时right代表					的就是“第一个 >= target的数的下标”————

                - **左阵营 (**`**left**`**)**：在这个索引左边的数，我们确定**全部**都 < target
                - **右阵营 (**`**right**`**)**：在这个索引（包含自身）右边的数，我们确定**全部**都  >= target

又因为target的第一个数恰好满足这个条件，使用**lowerBound**返回的实际上是target的右边界

之后在主函数中如法炮制，通过**求得target+1的首位，再减去1**，所得到的就是target的右边界

```cpp
vector<int> searchRange(vector<int>& nums, int target)
{
    int start = lowerBound(nums, target);
    if(start == nums.size() || nums[start] != target)
        return {-1, -1};
    int end = lowerBound(nums, target + 1) - 1;
    return {start, end};
}

// 返回第一个 >= target的数的下标
int lowerBound(vector<int>& nums, int target)
{
    int left = 0, right = nums.size();
    while(left < right)
    {
        int mid = left + (right - left) / 2;

        if(target <= nums[mid])
            right = mid;
        else
            left = mid + 1;
    }
    return right;
}
```




<a id="G8dlB"></a>

<strong>补充解法：标准库 lower_bound</strong>

<a id="IhRiH"></a>
```cpp
vector<int> searchRange(vector<int>& nums, int target)
{
    if(nums.empty()) return{-1,-1};

    int start = lower_bound(nums.begin(), nums.end(), target) - nums.begin();

    if(start == nums.size() || nums[start] != target)
        return {-1, -1};

    // 因为这里得到的是第一个 target + 1 的元素的下标
    // 所以需要减一得到的才是 target 最后一个元素的下标
    int end = lower_bound(nums.begin(), nums.end(), target + 1) - nums.begin() - 1;
    return {start, end};
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/kovh86nqrne4grtx)
