+++
slug = "jump-game"
title = "跳跃游戏"
problems = [55]
problem_id = 55
difficulty = "Medium"
weight = 55
summary = "跳跃游戏的解题思路与 C++ 实现。"
+++

题目：[跳跃游戏](https://leetcode.cn/problems/jump-game/)


<a id="第五十五题跳跃游戏"></a>



思路：

从第一个元素开始进行遍历，并记录截止当前元素可以到达的最大位置（far）

如果当前位置的下标（i）比最远位置还要大，就说明 i 是无法到达的，也就更不可能到达终点

而如果 i 在 far 的范围之内，就说明 i 是可以到达的，此时就需要根据 i 对应的值来更新 far 的位置

当整个数组都被遍历完成，就说明最后一个元素是位于 far 之内的，也就代表着终点可以到达

```cpp
bool canJump(vector<int>& nums)
{
    int far = 0;
    for(int i = 0; i < nums.size(); i++)
    {
        if(far < i) return false;
        else
            far = std::max(far, i + nums[i]);
    }
    return true;
}
```
