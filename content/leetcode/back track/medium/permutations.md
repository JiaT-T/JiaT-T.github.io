+++
slug = "permutations"
title = "全排列"
problems = [46]
problem_id = 46
difficulty = "Medium"
weight = 46
summary = "全排列的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/tvmshwlzcw3s2ta1"
+++

题目：[全排列](https://leetcode.cn/problems/permutations/)


<a id="第四十六题全排列"></a>



核心在于“**交换**”的步骤

首先从第一个元素开始，既然首元素已经确定了，之后就是递归地对后面的元素进行全排列

本质上就是让所有元素都当一次第一个元素，再让此时的第一个元素之后的所有元素当一次第二个元素.....以此类推，从前往后每个位置分别有n、n-1、n-2个种选择，也就是n！种排列方式

```cpp
vector<vector<int>> permute(vector<int>& nums)
{
    vector<vector<int>> res;
    res.reserve(factorial(nums.size()));

    backTrack(nums, res, 0);
    return res;
}

void backTrack(vector<int>& nums, vector<vector<int>>& res, int first)
{
    if(first == nums.size())
        res.push_back(nums);

    for(int i = first; i < nums.size(); i++)
    {
        std::swap(nums[first], nums[i]);
        backTrack(nums, res, first + 1);
        std::swap(nums[first], nums[i]);
    }
}

size_t factorial(size_t sz)
{
    size_t res;
    for(int i = 0; i < sz; i++) res *= i;
    return res;
}
```




<a id="bk8XA"></a>

<strong>补充解法：used 数组回溯</strong>

```cpp
class Solution
{
public:
    std::vector<vector<int>> res;
    std::vector<int> path;
    void backTrack(vector<int>& nums, vector<bool> used)
    {
        // 终止条件
        if(path.size() == nums.size())
        {
            res.push_back(path);
            return;
        }

        for(int i = 0; i < nums.size(); i++)
        {
            // 如果当前元素已经被使用过了
            // 就直接跳过它
            if(used[i])
                continue;

            // 将当前元素标记为“已使用”
            used[i] = true;
            path.push_back(nums[i]);
            // 对下一个元素进行操作
            backTrack(nums, used);
            // 撤销所有操作
            path.pop_back();
            used[i] = false;
        }
    }

    vector<vector<int>> permute(vector<int>& nums)
    {
        // 用来标记已使用的元素
        std::vector<bool> used(nums.size(), false);
        backTrack(nums, used);
        return res;
    }
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/tvmshwlzcw3s2ta1)
