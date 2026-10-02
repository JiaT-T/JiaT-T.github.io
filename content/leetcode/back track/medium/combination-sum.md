+++
slug = "combination-sum"
title = "组合总和"
problems = [39]
problem_id = 39
difficulty = "Medium"
weight = 39
summary = "组合总和的解题思路与 C++ 实现。"
+++

题目：[组合总和](https://leetcode.cn/problems/combination-sum/)


<a id="第三十九题组合总和"></a>



核心思路：**每次添加元素之后都将target减少对应的值，直到等于或小于零**

具体实现：

在回溯函数中首先判断target是否已经等于零——代表着当前元素的组合已经满足要求，可以压入res数组中

否则继续进行遍历与递归，直到出现满足总和要求的数组为止

在循环中要注意的是，当总和已经超出target时，就不要在把当前元素存入temp中了，而是直接跳过他，从下一个元素继续进行

```cpp
void backTrack(vector<int>& candidates, int target, int index, vector<int>& temp, vector<vector<int>>& res)
{
    if(target == 0)
    {
        res.push_back(temp);
        return;
    }

    for(int i = index; i < candidates.size(); i++)
    {
        if(target - candidates[i] < 0) continue;
        temp.push_back(candidates[i]);
        backTrack(candidates, target - candidates[i], i, temp, res);
        temp.pop_back();
    }
}
vector<vector<int>> combinationSum(vector<int>& candidates, int target)
{
    vector<vector<int>> res;
    vector<int> temp;
    res.reserve(150);
    backTrack(candidates, target, 0, temp, res);
    return res;
}
```
