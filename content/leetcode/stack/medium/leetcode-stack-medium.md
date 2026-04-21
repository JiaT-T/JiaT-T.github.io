+++
title = "155、394、739"
+++


#### <font style="color:#DF2A3F;">第一百五十五题</font>：[最小栈](https://leetcode.cn/problems/min-stack/)
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



#### <font style="color:#DF2A3F;">第三百九十四题</font>：[字符串解码](https://leetcode.cn/problems/decode-string/)
使用到的是栈和递归

关于为什么是遇到‘【’就继续入栈：这是为了处理前置的字母，可以将其直接拼接到res的尾部

```cpp
string decodeString(string s)
{
    std::stack<std::pair<string, int>> stk;
    string res;
    int k = 0;
    for(char c : s)
    {
        if(isalpha(c)) res += c;
        else if(isdigit(c)) k = k * 10 + (c - '0');
        else if(c == '[')
        {
            stk.emplace(std::move(res), k);
            k = 0;
        }
        else
        {
            auto [pre_res, pre_k] = stk.top();
            stk.pop();
            while(pre_k--)
            {
                pre_res += res;
            }
            res = std::move(pre_res);
        }
    }
    return res;
}
```



#### <font style="color:#DF2A3F;">第七百三十九题</font>：[每日温度](https://leetcode.cn/problems/daily-temperatures/)
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
