+++
slug = "daily-temperatures"
title = "每日温度"
problems = [739]
problem_id = 739
difficulty = "Medium"
weight = 739
summary = "每日温度的解题思路与 C++ 实现。"
+++

题目：[每日温度](https://leetcode.cn/problems/daily-temperatures/)


<a id="第七百三十九题每日温度"></a>



使用到的是<font style="background-color:#FBDE28;">单调栈</font>

首先想到的是双重循环遍历😅........但这会导致n方的复杂度，所以这个方法不好

我们想要的是，通过一次遍历就可以找到所有符合条件的结果，这就意味着需要使用一种数据结构来存储遍历过的元素，再在之后的循环中进行比较

单调栈就是指，在入栈过程中，通过不断剔除不符合条件的元素，以保持栈内的元素按照某种单调性排列，即有序性，这与此题的要求高度吻合

所以在代码中，我们定义了一个stack，用于存储需要进行比较的数组的下标（至于为什么不存元素，这是因为后面我们需要用这个下标找到输出结果中对应的位置，并且距离计算使用的也是下标）

具体的运作原理是：栈顶元素是上一次循环留下来的结果，将栈顶元素与当前元素进行比较，如果当前元素更大，就认为栈顶元素找到了第一个更高温度，此时让栈顶元素出栈，因为他已经比较完毕了；由于while循环，若此时栈不为空，那么就会再次进行比较，如果当前元素更小，就入栈，这也就是选择单调栈的原因（保持了大小的有序性）

注意：这里可以进行优化，主要是把多次调用的函数提前保存，避免调用函数的开销（因为这是在循环中，所以开销会很大）

```cpp
//
// 优化前（33ms）
//
vector<int> dailyTemperatures(vector<int>& temperatures)
{
    std::stack<int> st;
    st.push(0);
    int sz = temperatures.size();
    std::vector<int> res(sz, 0);

    for(int j = 1; j < sz; j++)
    {
        while(!st.empty() && temperatures[st.top()] < temperatures[j])
        {
            res[st.top()] = j - st.top();
            st.pop();
        }
        st.push(j);
    }
    return res;
}

//
// 优化后（28ms）
//
vector<int> dailyTemperatures(vector<int>& temperatures)
{
    std::stack<int> st;
    int sz = temperatures.size();
    std::vector<int> res(sz, 0);

    for(int j = 0; j < sz; j++)
    {
        int t = temperatures[j];
        while(!st.empty() && temperatures[st.top()] < t)
        {
            int k = st.top();
            res[k] = j - k;
            st.pop();
        }
        st.push(j);
    }
    return res;
}
```
