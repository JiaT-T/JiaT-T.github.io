+++
slug = "house-robber-ii"
title = "打家劫舍 II"
problems = [213]
problem_id = 213
difficulty = "Medium"
weight = 213
summary = "打家劫舍 II的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/ixw7uw6xa05tg08k"
+++

题目：[打家劫舍 II](https://leetcode.cn/problems/house-robber-ii/)


<a id="第二百一十三题打家劫舍-ii"></a>

<a id="cKKTl"></a>

<a id="u1e5b4ff2"></a>核心是<strong>将“环”拆解为“两个线性表”</strong>

<a id="ue2edefbb"></a>对于环形的 n 间房屋，可以将其拆解为两个场景：

- <a id="u4ab58ddb"></a><strong>场景 A</strong>：<strong>不偷最后一间房</strong>。此时可以偷的范围是 `nums[0]` 到 `nums[n-2]`
- <a id="u06559b45"></a><strong>场景 B</strong>：<strong>不偷第一间房</strong>。此时可以偷的范围是 `nums[1]` 到 `nums[n-1]`

<a id="u7a9c499f"></a>最后的结果一定是<strong>两者中的更大值</strong>

<a id="ZfOxO"></a>
rob ()
```cpp
// 这里的辅助函数与上题一样
int robRange(std::vector<int>& nums, int start, int end)
{
    int prev1 = 0, prev2 = 0;
    for(int i = start; i < end; i++)
    {
        int temp = prev2;
        prev2 = std::max(prev2, prev1 + nums[i]);
        prev1 = temp;
    }
    return prev2;
}
int rob(vector<int>& nums)
{
    int n = nums.size();
    if(n == 1) return nums[0];
    if(n == 2) return std::max(nums[0], nums[1]);

    int res1 = robRange(nums, 0, n - 1);
    int res2 = robRange(nums, 1, n);

    return std::max(res1, res2);
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ixw7uw6xa05tg08k)
