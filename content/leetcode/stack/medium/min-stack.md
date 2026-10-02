+++
slug = "min-stack"
title = "最小栈"
problems = [155]
problem_id = 155
difficulty = "Medium"
weight = 155
summary = "最小栈的解题思路与 C++ 实现。"
+++

题目：[最小栈](https://leetcode.cn/problems/min-stack/)


<a id="第一百五十五题最小栈"></a>



对这个类需要完成的任务有五个：

1.初始化	2.入栈	3.出栈	 4.获取栈顶元素	5.获取最小值

因为初始的时候没有元素需要初始化，所以这个类的构造函数不需要去管他

通过在这个类中构建一个STL自带的stack，就可以实现234的操作，而5则需要再使用一个辅助栈，这题的难点也是在5

题目要求在常数时间内检索到最小值，所以一个一个去遍历肯定是不行的，这也是引入辅助栈的原因，我们可以通过不断地将更小的元素压入这个辅助栈（minst），来达到”栈顶的元素肯定是最小“的条件；之后如果需要取出最小元素的话，只需要对minst进行一次出栈操作即可

<font style="background-color:#FBDE28;">具体实现</font>：

1.当有元素传入时，如果此时minst为空，就直接入栈，此后入栈的元素都是当前栈顶元素与传入元素的更小值

2.出栈操作也应该是两者同时进行的，因为最小值需要根据st的元素动态更新（假如此时st的栈顶就是最小元素，而下一步操作就是出栈，那么之后栈中的最小元素也应该发生变化）

```cpp
class MinStack
{
public:
    std::stack<int> minst;
    std::stack<int> st;

    MinStack()
    {
    }

    void push(int val)
    {
        st.push(val);
        if(minst.empty()) minst.push(val);
        else minst.push(std::min(val, minst.top()));
    }

    void pop()
    {
        minst.pop();
        st.pop();
    }

    int top()
    {
        return st.top();
    }

    int getMin()
    {
        return minst.top();
    }
};
```
