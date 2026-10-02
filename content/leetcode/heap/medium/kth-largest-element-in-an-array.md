+++
slug = "kth-largest-element-in-an-array"
title = "数组中的第K个最大元素"
problems = [215]
problem_id = 215
difficulty = "Medium"
weight = 215
summary = "数组中的第K个最大元素的解题思路与 C++ 实现。"
+++

题目：[数组中的第K个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/)


<a id="第二百一十五题数组中的第k个最大元素"></a>



<font style="background-color:#FBDE28;">解法一：优先队列（堆）</font>

+ **时间复杂度**：O(n log k)<font style="color:rgb(249, 250, 251);">		</font>**空间复杂度**：O(k)

手动维护一个大小为 k 的最小堆（堆顶是堆中的最小元素），每当堆的大小超过 k 时，就将堆顶的元素弹出，这样最终留下来的堆顶元素就是 第k大的元素

```cpp
int findKthLargest(vector<int>& nums, int k)
{
    std::priority_queue<int, std::vector<int>, greater<int>> pq;
    for(const int& num : nums)
    {
        pq.emplace(num);
        if(k < pq.size())
            pq.pop();
    }
    return pq.top();
}
```



<font style="background-color:#FBDE28;">解法二：快速选择</font>

**平均时间复杂度**是 O(n)

常规情况下的快排的平均时间复杂度是nlogn，所以需要手写一个快排

具体实现：

定义三个数组，分别**存储大于、等于、小于基准值**的数，通过一轮循环将其填充

之后的判断存在三种情况：

<font style="color:#74B602;">1.k 小于等于 big 数组的大小</font>——也就是说，big数组中存在第一大、第二大.....**一直到第 k 大甚至更多元素**，此时第 k 大的元素一定存在于 big 数组中，那么接下来就只需要在 big 数组里寻找即可

<font style="color:#74B602;">2.k 大于原数组大小减去 small 数组大小</font>——nums.size() - small.size() 代表的是 big 数组加上 equal 数组的大小，也就是说**此时 big 与 equal 数组中的元素数量加起来都不足 k 个，那么第 k 大的元素就一定在 small数组里了**；注意 quickSeclet 的第二个参数从 k 变成了 k - nums.size() + small.size()，这是因为，相对于整个数组，需要寻找的是第 k 大的元素，而相对于 small 数组来说，这个元素是第

k - （nums.size() - small.size()）大的元素

<font style="color:#74B602;">3.第 k 大位于 equal里面</font>

此时直接返回基准值即可

```cpp
int findKthLargest(vector<int>& nums, int k)
{
    return quickSeclet(nums, k);
}

int quickSeclet(vector<int>& nums, int k)
{
    std::vector<int> big, equal, small;
    int pivot = nums[std::rand() % nums.size()];
    for(int num : nums)
    {
        if(num < pivot) small.push_back(num);
        else if(pivot < num) big.push_back(num);
        else equal.push_back(num);
    }

    if(k <= big.size())
        return quickSeclet(big, k);
    if(nums.size() - small.size() < k)
        return quickSeclet(small, k - nums.size() + small.size());
    return pivot;
}
```
