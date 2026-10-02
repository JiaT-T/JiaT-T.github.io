+++
slug = "single-number"
title = "只出现一次的数字"
problems = [136]
problem_id = 136
difficulty = "Easy"
weight = 136
summary = "只出现一次的数字的解题思路与 C++ 实现。"
+++

题目：[只出现一次的数字](https://leetcode.cn/problems/single-number/)


<a id="第一百三十六题只出现一次的数字"></a>



题目要求的是线性时间复杂度以及常量额外空间，所以像哈希表之类的解法都不能使用

这里使用到的是**<font style="background-color:#FBDE28;">异或（XOR）</font>**，它的性质是：

1.任何数与0异或得到这个数本身

2.任何数与自身异或得到0

3.异或运算满足结合律，即_**a**_**⊕**_**b**_**⊕**_**a**_**=**_**b**_**⊕**_**a**_**⊕**_**a**_**=**_**b**_**⊕(**_**a**_**⊕**_**a**_**)=**_**b**_**⊕0=**_**b**_

通过以上性质，只需要将数组内的所有元素放在同一个异或运算式中，就可以将所有相同的数字进行组合（结果为零），又因为性质一，所以最后得到的结果一定就是落单的数字

```cpp
int singleNumber(vector<int>& nums)
{
    int res = 0;
    for(auto num : nums) res ^= num;
    return res;
}
```
