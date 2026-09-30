+++
title = "20"
problems = [20, 232]
+++

#### <font style="color:#DF2A3F;">第二十题</font>：[<font style="color:rgb(10, 132, 255);">有效的括号</font>](https://leetcode.cn/problems/valid-parentheses/)
使用到的知识点是栈

利用栈的FILO的特性，可以很好的对相应的括号进行匹配

比如"{ [ ( ) ] } "

第一次先压入{，接着判断下一个括号的类型，如果为左括号，则继续压入；如果为相匹配的右括号，则弹出；如果为不匹配的右括号，则直接返回false

最后如果整个栈都为空，就意味着所有的括号都得到了匹配，那么就返回true

注意：在一开始的时候，要判断一下特殊情况------

<font style="background-color:#FBDE28;">元素个数为奇数，就意味着总会有一个括号无法被匹配，直接返回false</font>

```cpp
bool isValid(string s)
    {
        std::vector<char> stack;
        if(s.size() % 2 == 1) return false;
        for(int n = 0; n < s.size(); n++)
        {   
            if(s[n] == '(' || s[n] == '[' || s[n] == '{') stack.push_back(s[n]);
            else
            {           
                if (stack.empty()) return false;
                if(s[n] == ')' && stack.back() == '(') stack.pop_back();
                else if(s[n] == ']' && stack.back() == '[') stack.pop_back();
                else if(s[n] == '}' && stack.back() == '{') stack.pop_back();
                else return false;
            }
        }
        if(stack.empty()) return true;
        return false;
    }
```

<a id="FausE"></a>
#### 第二百三十二题：[用栈实现队列](<https://leetcode.cn/problems/implement-queue-using-stacks/>)

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

