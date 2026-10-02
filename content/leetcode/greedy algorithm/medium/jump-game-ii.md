+++
slug = "jump-game-ii"
title = "跳跃游戏 II"
problems = [45]
problem_id = 45
difficulty = "Medium"
weight = 45
summary = "跳跃游戏 II的解题思路与 C++ 实现。"
+++

题目：[跳跃游戏 II](https://leetcode.cn/problems/jump-game-ii/)


<a id="第四十五题跳跃游戏-ii"></a>



这里直接引用一下别人的讲解：

//把该问题比喻为入职，数组下标是公司级别(入职门槛)，对应的值是公司级别之上的级别成长空间。你想用最少的跳槽次数入职最高级的公司

//数组[2,3,1,2,4,2,3]

//下标 0 1 2 3 4 5 6

//最开始你没有工作，你的水平是2级，可以在2级及以下的公司里随便挑，此时候选公司有下标1和2

//注意：如果你想进入更高级别的公司，应该选择能够帮助你提升级别最多的公司。例如，公司1能够将你的级别提升到1+3=4级，而公司2只能提升到2+1=3级。显然，你应该选择公司1，然后升到4级。接下来，你可以跳槽到4级及以下的公司，每次都选择能够帮助你提升最多级别的公司，如此循环……直到水平级别足够入职梦中情司

//只有每次跳槽都选择能够帮助你升级最多的公司，才能以最少的跳槽次数到达最高级别的公司

```cpp
int jump(vector<int>& nums)
{
    int res = 0;
    int curr = 0, max_pos = 0;

    for(int i = 0; i < nums.size() - 1; i++)
    {
        max_pos = std::max(max_pos, i + nums[i]);
        if(i == curr)
        {
            curr = max_pos;
            res++;
        }
    }
    return res;
}
```
