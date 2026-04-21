+++
title = "20"
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


