+++
slug = "maximum-product-subarray"
title = "乘积最大子数组"
problems = [152]
problem_id = 152
difficulty = "Medium"
weight = 152
summary = "乘积最大子数组的解题思路与 C++ 实现。"
+++

题目：[乘积最大子数组](https://leetcode.cn/problems/maximum-product-subarray/)


<a id="第一百五十二题乘积最大子数组"></a>



<font style="background-color:#FBDE28;">确定状态</font>：dp[ i ] 代表“以当前元素为结尾的最大/最小乘积是多少”

<font style="background-color:#FBDE28;">状态转移</font>：（具体公式见下图）一开始的想法是——如果当前元素乘上dp数组的上一个元素之后，所得乘积比上一个还要小，那么就以当前元素为起点向后乘；反之，将所得乘积作为以当前元素（nums[ i ]）为结尾的连续乘积存入dp数组

但是这会导致一个问题——如果原数组是 [ -2, 3, -4 ] 这种类型的话，期望结果是24（因为负负得正），但是上一个方法却会直接抛弃-2 * 3的结果，转而从 -4 开始重新计数，又因为此时已经到达了末尾，此时dp数组为 [-2, -6, -4 ] 所以最后会返回-2

上一种方法相当于只记录了最大正乘积，没有考虑到最小负乘积可能会与负数相乘，因此**还需要定义一个dp数组，用于存放最小乘积**

```cpp
int maxProduct(vector<int>& nums)
{
    if(nums.size() == 1) return nums[0];
    std::vector<int> dp_max(nums.size(), 1), dp_min(nums.size(), 1);
    dp_max[0] = dp_min[0] = nums[0];

    int res = nums[0];
    for(int i = 1; i < nums.size(); i++)
    {
        int choice1 = dp_max[i -1] * nums[i];
        int choice2 = dp_min[i -1] * nums[i];

        dp_max[i] = std::max({nums[i], choice1, choice2});
        dp_min[i] = std::min({nums[i], choice1, choice2});

        res = res < dp_max[i] ? dp_max[i] : res;
    }
    return res;
}
```
