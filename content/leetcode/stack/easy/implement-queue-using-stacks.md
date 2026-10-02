+++
slug = "implement-queue-using-stacks"
title = "用栈实现队列"
problems = [232]
problem_id = 232
difficulty = "Easy"
weight = 232
summary = "用栈实现队列的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/mz1u7y5haqw7i1ug"
+++

题目：[用栈实现队列](https://leetcode.cn/problems/implement-queue-using-stacks/)


<a id="第二百三十二题用栈实现队列"></a>

<a id="FausE"></a>

<a id="u1294e3e3"></a>解法一：

<a id="u197f0da9"></a>定义两个栈，一个正序记录输入的数字，另一个则倒序记录

<a id="u0630c5db"></a>对于 push，每次压入元素时，需要重新记录 sk2；

<a id="uc1b0888a"></a>对于 pop，每次弹出元素时，需要重新记录 sk1

<a id="Bq9pO"></a>
MyQueue
```cpp
class MyQueue
{
public:
    std::stack<int> sk1;
    std::stack<int> sk2;
    MyQueue()
    {
    }

    void push(int x)
    {
        sk1.push(x);
        std::stack<int> temp_sk1 = sk1;
        std::stack<int> temp_sk2;
        for(int i = 0; i < sk1.size(); i++)
        {
            temp_sk2.push(temp_sk1.top());
            temp_sk1.pop();
        }
        sk2 = std::move(temp_sk2);
    }

    int pop()
    {
        int res = sk2.top();
        sk2.pop();
        std::stack<int> temp_sk1, temp_sk2 = sk2;
        for(int i = 0; i < sk2.size(); i++)
        {
            temp_sk1.push(temp_sk2.top());
            temp_sk2.pop();
        }
        sk1 = std::move(temp_sk1);
        return res;
    }

    int peek()
    {
        return sk2.top();
    }

    bool empty()
    {
        return sk1.empty();
    }
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/mz1u7y5haqw7i1ug)
