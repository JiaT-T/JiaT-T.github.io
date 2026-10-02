+++
slug = "largest-perimeter-triangle"
title = "三角形的最大周长"
problems = [976]
problem_id = 976
difficulty = "Easy"
weight = 976
summary = "三角形的最大周长的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/ne188hgk5rxky939"
+++

题目：[三角形的最大周长](https://leetcode.cn/problems/largest-perimeter-triangle/)


<a id="第九百七十六题三角形的最大周长"></a>

<a id="kgIWj"></a>

<a id="u8be6cfe1"></a>先将数组进行排序，之后从后往前进行遍历，每次判断上一个元素与上上个元素之和是否大于当前元素（三角形两边之和大于第三边）

<a id="uea478a54"></a>如果条件满足，直接计算周长并返回；否则，进入下一次循环

<a id="DhRqC"></a>
largestPerimeter（）
```cpp
int largestPerimeter(vector<int>& nums)
{
    std::sort(nums.begin(), nums.end());
    int res = 1;
    for(int i = nums.size() - 1; 2 <= i; --i)
    {
        if(nums[i - 1] + nums[i - 2] > nums[i])
            return nums[i] + nums[i - 1] + nums[i - 2];
        else
            continue;
    }
    return 0;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ne188hgk5rxky939)
