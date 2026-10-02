+++
slug = "palindrome-partitioning"
title = "分割回文串"
problems = [131]
problem_id = 131
difficulty = "Medium"
weight = 131
summary = "分割回文串的解题思路与 C++ 实现。"
+++

题目：[分割回文串](https://leetcode.cn/problems/palindrome-partitioning/)


<a id="第一百三十一题分割回文串"></a>



思路：对于每一个字符，都先判断其是否能够被分割，即以start为首，以当前字符为尾的字符串是否为回文串；如果能够分割（**第一条路径**），就将当前元素压入path，组成子回文串，并从下一个字符开始进行新一轮的回文串判断；**第二条路径**为：不从当前字符进行分割，而是直接转向下一个字符，从下一个字符开始判断（为了找到更长的回文串）

```cpp
bool isPalindrome(const string& s, int left, int right)
{
    while(left < right)
    {
        if(s[left++] != s[right--])
            return false;
    }
    return true;
}
void dfs(string& s, int index, int start, vector<string>& path, vector<vector<string>>& res)
{
    const int sz = s.size();
    if(index == sz)
    {
        res.emplace_back(path);
        return;
    }

    if(isPalindrome(s, start, index))
    {
        path.emplace_back(s.substr(start, index - start + 1));
        dfs(s, index + 1, index + 1, path, res);
        path.pop_back();
    }

    if(index < sz - 1)
        dfs(s, index + 1, start, path, res);
}

vector<vector<string>> partition(string s)
{
    vector<string> path;
    vector<vector<string>> res;

    dfs(s, 0, 0, path, res);
    return res;
}
```
