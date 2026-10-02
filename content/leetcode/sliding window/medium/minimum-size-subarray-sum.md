+++
slug = "minimum-size-subarray-sum"
title = "长度最小的子数组"
problems = [209]
problem_id = 209
difficulty = "Medium"
weight = 209
summary = "长度最小的子数组的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/yg57x00m0sytet7u"
+++

题目：[长度最小的子数组](https://leetcode.cn/problems/minimum-size-subarray-sum/)


<a id="第二百零九题长度最小的子数组"></a>

<a id="A5ODj"></a>

<a id="ue4eb73e4"></a>使用到的是滑动窗口

<a id="tcFqA"></a>
minSubArrayLen（）
```cpp
int minSubArrayLen(int target, vector<int>& nums)
{
    int n = nums.size(), sum = 0, left = 0;
    // 因为最后的结果输出的是子数组长度
    // 所以最大长度肯定不会超过原数组长度 n
    int res = n + 1;
    // 遍历右边的节点
    for(int right = 0; right < n; right++)
    {
        // 首先将右指针指向的节点加到 sum 中
        sum += nums[right];
        // 不断缩小窗口
        while(target <= sum - nums[left])
        {
            sum -= nums[left];
            // 左端点右移
            left++;
        }
        // 此时经过缩小之后，如果 sum 仍然大于等于 target
        // 就记录一次答案
        if(target <= sum)
        {
            res = std::min(res, right - left + 1);
        }
    }
    return res == n + 1 ? 0 : res;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/yg57x00m0sytet7u)
