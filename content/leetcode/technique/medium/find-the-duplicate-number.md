+++
slug = "find-the-duplicate-number"
title = "寻找重复数"
problems = [287]
problem_id = 287
difficulty = "Medium"
weight = 287
summary = "寻找重复数的解题思路与 C++ 实现。"
+++

题目：[寻找重复数](https://leetcode.cn/problems/find-the-duplicate-number/)


<a id="第二百八十七题寻找重复数"></a>



用到了**”环形链表”**的思想

对于含有唯一 一个重复元素的数组，使用快慢指针进行遍历，fast每次两步（nums[nums[fast]]），slow每次一步（nums[slow]），那么之后一定会产生一个环，而入口就是那个重复的元素

之后只需要再指定一个从起点出发的指针，与slow一起再次进行遍历，最终相遇的位置就是重复数字的位置

（关于环形更具体的解释参见“链表 -> Medium”）

```cpp
int findDuplicate(vector<int>& nums)
{
    int fast = nums[nums[0]], slow = nums[0];
    while(fast != slow)
    {
        fast = nums[nums[fast]];
        slow = nums[slow];
    }

    int finder = 0;
    while(finder != slow)
    {
        finder = nums[finder];
        slow = nums[slow];
    }
    return slow;
}
```
