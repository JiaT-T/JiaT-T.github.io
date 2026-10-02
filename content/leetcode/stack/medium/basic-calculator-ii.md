+++
slug = "basic-calculator-ii"
title = "基本计算器 II"
problems = [227]
problem_id = 227
difficulty = "Medium"
weight = 227
summary = "基本计算器 II的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/ycrbu8cmk9hdwiae"
+++

题目：[基本计算器 II](https://leetcode.cn/problems/basic-calculator-ii/)


<a id="第二百二十七题基本计算器-ii"></a>

<a id="U4Yqt"></a>

<a id="u1732a50f"></a><a id="BqUFm"></a>[https://leetcode.cn/problems/basic-calculator-ii/solutions/648647/ji-ben-ji-suan-qi-ii-by-leetcode-solutio-cm28/](<https://leetcode.cn/problems/basic-calculator-ii/solutions/648647/ji-ben-ji-suan-qi-ii-by-leetcode-solutio-cm28/>)

<a id="lEogU"></a>
```cpp
int calculate(string s)
{
    // 对于字符串中的第一个数字默认符号是'+'
    char preSign = '+';
    // 维护一个栈用于存储数字
    std::vector<int> st;
    int num = 0, n = s.length();

    for(int i = 0 ; i < n; i++)
    {
        // 如果是数字，就进行累加
        if(isdigit(s[i]))
        {
            num = num * 10 + (s[i] - '0');
        }
        // 如果不是数字，同时也不是空格
        if(!isdigit(s[i]) && s[i] != ' ' || i == n - 1)
        {
            // 根据符号对之前累加得到的 num 进行处理
            switch(preSign)
            {
                case '+' :
                    st.push_back(num);
                    break;
                // 如果是减号，就将负数形式保存进栈中
                case '-' :
                    st.push_back(-num);
                    break;
                // 如果是乘除，就直接对栈顶的数字与当前保存的 num 进行对应运算
                case '*' :
                    st.back() *= num;
                    break;
                default :
                    st.back() /= num;
            }
            // 将 num 置为零，不用存入栈中，因为已经与栈顶元素进行过处理了
            num = 0;
            // 把当前符号传递给下一个数字使用
            preSign = s[i];
        }
    }
    // 最后栈里只剩下被处理过正负号的数字，全部加起来就是结果
    return accumulate(st.begin(), st.end(), 0);
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ycrbu8cmk9hdwiae)
