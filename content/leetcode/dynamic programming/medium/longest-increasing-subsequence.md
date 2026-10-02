+++
slug = "longest-increasing-subsequence"
title = "最长递增子序列"
problems = [300]
problem_id = 300
difficulty = "Medium"
weight = 300
summary = "最长递增子序列的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/ixw7uw6xa05tg08k"
+++

题目：[最长递增子序列](https://leetcode.cn/problems/longest-increasing-subsequence/)


<a id="第三百题最长递增子序列"></a>



<font style="background-color:#FBDE28;">解法一：动态规划</font>

状态定义：dp[ i ]指的是“以第 i 个元素结尾的子序列的最大长度”

状态转移：dp[ i ] = max( dp[ i ], dp[ j ] + 1 )，其中 j 是不大于 i 的正整数；

方程的意义是——假设正在处理 `nums[i]`，我们想把它接在一个现有的子序列后面。

为了保证“严格递增”，必须满足两个条件：

    1. **位置在前后**：那个数必须在 i 之前（即 j < i）。
    2. **数值从小到大**：那个数必须比 `nums[i]` 小（即 nums[j] < nums[i]）。

```cpp
int lengthOfLIS(vector<int>& nums)
{
    if(nums.empty()) return 0;
    std::vector<int> dp(nums.size(), 1);
    int res = 1;
    for(int i = 0; i < nums.size(); i++)
    {
        for(int j = 0; j < i; j++)
        {
            if(nums[j] < nums[i])
            {
                dp[i] = std::max(dp[i], dp[j] + 1);
            }
        }
        res = std::max(res, dp[i]);
    }
    return res;
}
```





<strong>补充解法：二分查找维护最小末尾</strong>

<a id="u169cc786"></a>维护一个数组 dp，dp【i】的含义是：<strong>长度为 i + 1 的子数组的末尾元素的最小值</strong>

<a id="u109d1d59"></a>然后遍历数组 nums，在 dp 中通过二分查找，看看 num 的位置在哪里

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="uef96fc8d">如果不存在任何一个数大于等于 num，也就是 it = num.end（），就将 num 接入 dp 的末尾，意味着子序列的长度可以加一</li><li id="u0e3c5291">如果当前数组中已经有一个数大于等于 num 了，就将这个数替换为 num（降低末尾元素的值，确保后续可以有更多元素加入）</li></ul>

- <a id="ucde1169c"></a><strong>时间复杂度</strong>：<strong>O(</strong><em><strong>n</strong></em> <strong>log</strong><em><strong>n</strong></em><strong>)</strong>，其中 <em>n</em> 为 <em>nums</em> 的长度
- <a id="u4d2ab594"></a><strong>空间复杂度</strong>：<strong>O(</strong><em><strong>n</strong></em><strong>)</strong>

<a id="yyLuB"></a>
```cpp
int lengthOfLIS(vector<int>& nums)
{
    std::vector<int> dp;

    for(int num : nums)
    {
        auto it = std::lower_bound(dp.begin(), dp.end(), num);
        if(it == dp.end())
        {
            dp.push_back(num);
        }
        else
        {
            *it = num;
        }
    }
    return dp.size();
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ixw7uw6xa05tg08k)


<a id="DMet3"></a>

<strong>补充解法：原地修改</strong>

<a id="u6dfd6846"></a>直接对传入的 nums 数组进行修改，避免再创建一个新数组

<a id="mtKVu"></a>
lengthOfLIS（）

```cpp
int lengthOfLIS(vector<int>& nums)
{
    // 从第一个元素开始
    auto end = nums.begin();

    for(int num : nums)
    {
        // 在区间内找到第一个大于等于 num 的位置
        auto it = lower_bound(nums.begin(), end, num);

        // 将原来 g[j] 的值（一个较大的数）替换成更小的 num
        // 为什么直接认为 num 一定小于之前的末尾元素？
        /* 因为 lower_bound(first, last, x) 返回的是第一个满足 元素 >= x 的位置。
        因此，当 it != end 时，*it >= x 恒成立。
        于是执行 *it = x 后：
        如果 *it > x，新值变小（这正是我们想要的，因为要降低该长度的最小末尾）。
        如果 *it == x，新值不变（没有影响）。
        没有可能出现 *it < x 的情况，所以不存在“当前元素大于原末尾”的问题*/
        *it = num;

        if(it == end)
        {
            // 此时将长度加一
            end++;
        }
    }
    return end - nums.begin();
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ixw7uw6xa05tg08k)
