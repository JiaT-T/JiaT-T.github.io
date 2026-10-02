+++
slug = "climbing-stairs"
title = "爬楼梯"
problems = [70]
problem_id = 70
difficulty = "Easy"
weight = 70
summary = "爬楼梯的解题思路与 C++ 实现。"
+++

题目：[爬楼梯](https://leetcode.cn/problems/climbing-stairs/)


<a id="第七十题爬楼梯"></a>



简单的斐波那契公式

要注意的是，这里使用递归会超时，然后最好不要使用数组（因为除了当前值的前两个，再往前的数据更本就用不到，应该使用临时变量，存储在栈上，用完就释放内存）

```cpp
int climbStairs(int n)
{
    if(n <= 2) return n;

    int prev1 = 1, prev2 = 2;
    int curr = 0;
    for(int i = 3; i <= n; i++)
    {
        curr = prev1 + prev2;
        prev1 = prev2;
        prev2 = curr;
    }
    return curr;
}
```
