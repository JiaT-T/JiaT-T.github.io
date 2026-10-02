+++
slug = "3sum-closest"
title = "最接近的三数之和"
problems = [16]
problem_id = 16
difficulty = "Medium"
weight = 16
summary = "最接近的三数之和的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq"
+++

题目：[最接近的三数之和](https://leetcode.cn/problems/3sum-closest/)


<a id="第十六题最接近的三数之和"></a>

<a id="tb3Ir"></a>

<a id="u1cb8d51f"></a>与上一题（15题）一样，使用的是双指针与双循环，这样可以将O(n^3)的时间复杂度降低至O(n^2)

<a id="u4da54687"></a>首先对数组进行排序，方便后续左右指针的移动

<a id="u28ee7133"></a>如果当前的和恰好与目标值相同，就直接返回

<a id="u8b0c5c53"></a>接着与最接近的值进行比较，如果当前值更加接近，则替换

<a id="u5dc1cd9a"></a>最后判断当前的和与目标值的大小关系，如果更小，说明需要找到更大的数，因此将左指针右移，反之，将右指针左移

<a id="TDPjD"></a>
threeSumClosest（）
```cpp
int threeSumClosest(vector<int>& nums, int target)
    {
        int length = nums.size();
        std::sort(nums.begin(), nums.end());
        int closest_sum = nums[0] + nums[1] + nums[2];

        for(int i = 0; i < length - 2; i++)
        {
            int left = i + 1, right = length - 1;
            while(left < right)
            {
                int current_sum = nums[i] + nums[left] + nums[right];
                if(current_sum == target) return current_sum;
                if(std::abs(current_sum - target) < std::abs(closest_sum - target))
                    closest_sum = current_sum;
                if(current_sum < target)
                    left++;
                else
                    right--;
            }
        }
        return closest_sum;
    }
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq)
