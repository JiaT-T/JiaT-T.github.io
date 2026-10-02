+++
slug = "subsets"
title = "子集"
problems = [78]
problem_id = 78
difficulty = "Medium"
weight = 78
summary = "子集的解题思路与 C++ 实现。"
+++

题目：[子集](https://leetcode.cn/problems/subsets/)


<a id="第七十八题子集"></a>



核心思路：<font style="background-color:#FBDE28;">枚举每一个位置，并通过递归调用进入下一个位置</font>

具体实现：

每次进入回溯函数时，都先将当前保存的数组存入结果数组中，之后再进入具体的回溯算法——通过循环遍历当前元素之后的每一个元素，然后再递归调用相同函数，对下一个元素进行相同操作

```cpp
void backTrack(vector<int>& nums, vector<vector<int>>& res, vector<int>& temp, int start)
{
    res.emplace_back(temp);
    for(int i = start; i < nums.size(); i++)
    {
        temp.push_back(nums[i]);
        backTrack(nums, res, temp, i + 1);
        temp.pop_back();
    }
}
vector<vector<int>> subsets(vector<int>& nums)
{
    vector<vector<int>> res;
    vector<int> temp;
    res.reserve(1 << nums.size());
    backTrack(nums, res, temp, 0);
    return res;
}
```
