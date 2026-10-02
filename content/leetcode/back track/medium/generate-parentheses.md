+++
slug = "generate-parentheses"
title = "括号生成"
problems = [22]
problem_id = 22
difficulty = "Medium"
weight = 22
summary = "括号生成的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/tvmshwlzcw3s2ta1"
+++

题目：[括号生成](https://leetcode.cn/problems/generate-parentheses/)


<a id="第二十二题括号生成"></a>

<a id="vfqUX"></a>

<a id="u1846bb00"></a>使用到的是回溯算法

<a id="u211e00ae"></a>对于输入的数字n，可以知道的是最终的元素为2n个括号，其中左括号和右括号都为n个

<a id="u0219feb5"></a>先经过一次分析得到规律：以n=2为例，每个元素分别有2个左右括号，第一个空必须是' （ ’，此时left的数量加一；而第二个空则有两种可能，当为‘（’时，left的数量已经达到了2，那么之后两个空就只能是‘）’；当为‘）’时，此时left = right，第三个空就只能是‘（’，从而得出第四个空是‘）’

<a id="u513cf301"></a>总结规律，可以得出：

<a id="u4a7149fc"></a>1.当<strong>left &lt; n时，应该添加‘（’</strong>

<a id="u20fd6ddb"></a>2.当<strong>right &lt; left时，应当有‘）’与其配对，故添加‘）’</strong>

<a id="u7a39a59e"></a>在此条件下进行递归，最后当left+right与n相同时终止最后一层递归，返回上一层的枝，继续下一个子节点的递归

<a id="O2k9P"></a>
generateParenthesis()
```cpp
class Solution
{
public:
    vector<string> generateParenthesis(int n)
    {
        std::vector<string> combinations;
        string combination;
        backTrace(0, 0, combination, combinations, n);
        return combinations;
    }

private :
    void backTrace(int left, int right, string& combination, std::vector<string>& combinations, int n)
    {
        if(left + right == 2 * n)
        {
            combinations.push_back(combination);
            return;
        }
        else
        {
            if(left < n)
            {
                combination.push_back('(');
                backTrace(left + 1, right, combination, combinations, n);
                combination.pop_back();
            }
            if(right < left)
            {
                combination.push_back(')');
                backTrace(left, right + 1, combination, combinations, n);
                combination.pop_back();
            }
        }
    }
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/tvmshwlzcw3s2ta1)
