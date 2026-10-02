+++
slug = "longest-palindromic-substring"
title = "最长回文子串"
problems = [5]
problem_id = 5
difficulty = "Medium"
weight = 5
summary = "最长回文子串的解题思路与 C++ 实现。"
sources = ["https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq", "https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi"]
+++

题目：[最长回文子串](https://leetcode.cn/problems/longest-palindromic-substring/)


## 笔记 1 {#note-1}


<a id="第五题最长回文子串"></a>

<a id="T4KX3"></a>

<a id="u533c851a"></a>使用的是“<strong>中心扩散法</strong>”

<a id="u13dfc938"></a>参考了这里的解法：<a id="VJdpF"></a>[https://leetcode.cn/problems/longest-palindromic-substring/solutions/2958179/mo-ban-on-manacher-suan-fa-pythonjavacgo-t6cx/](<https://leetcode.cn/problems/longest-palindromic-substring/solutions/2958179/mo-ban-on-manacher-suan-fa-pythonjavacgo-t6cx/>)

<a id="uab0df562"></a>对于奇回文串，我们从最中间的一个元素开始向两边扩散，比如“bab”，第一次判断时 left = right，条件符合，所以 left--， right++；然后进入第二次判断，此时两者指向的字符都是‘b'，条件依然满足....直到左右指针指向的字符不同时，计算当前字符串长度

<a id="u0cd1f00d"></a>对于偶回文串，还是从中间开始扩散，只不过这次需要选取两个元素

<a id="ud9861e3c"></a>为了将两种情况合并处理，可以将 i 的最大范围改为 2n - 1，因为

- <a id="ue42e5f85"></a><strong>奇数长度回文中心</strong>：每个字符本身就是一个中心 → `n` 个
- <a id="uab6b0129"></a><strong>偶数长度回文中心</strong>：每两个相邻字符之间是一个中心 → `n - 1` 个

<a id="u9a4e8d28"></a>两者相加，所有回文中心的数量就是 <strong>2n - 1</strong> 个

<a id="y3ZCb"></a>
longestPalindrome（）
```cpp
string longestPalindrome(string s)
{
    int left = 0, right = 0;
    int n = s.size();
    for(int i = 0; i < 2 * n - 1; i++)
    {
        int l = i / 2, r = (i + 1) / 2;
        while(0 <= l && r < n && s[l] == s[r])
        {
            l--;
            r++;
        }
        if(r - l - 1 > right - left)
        {
            right = r;
            left = l + 1;
        }
    }
    return s.substr(left, right - left);
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq)

## 笔记 2 {#note-2}


<a id="第五题"></a>

<a id="LbCzn"></a>


<a id="zoPCj"></a>

<a id="u7f3591e3"></a>以一个字符（奇数回文串）或两个字符中间的空隙（偶数回文串）为中心，向左右两端扩散，如果两端字符相同，则继续扩展，并记录当前字符串的起始点

<a id="FuIsX"></a>
longestPalindrome(）
```cpp
std::pair<int, int> ExpandAroundCenter(const string& s, int left, int right)
{
    while(left >= 0 && right < s.size() && s[left] == s[right])
    {
        --left;
        ++right;
    }
    return {left+1, right-1};
}
string longestPalindrome(string s)
{
    int left = 0, right = 0;
    // 如果输入字符串总长为1，则直接返回该字符串
    if(s.size() < 2)
        return s;
    for(int i = 0; i < s.size(); ++i)
    {
        // 奇数回文串
        auto [left1, right1] = ExpandAroundCenter(s, i, i);
        // 偶数回文串
        auto [left2, right2] = ExpandAroundCenter(s, i, i+1);
        // 判断是奇数还是偶数
        if(right1 - left1 > right - left)
        {
            left = left1;
            right = right1;
        }
        if(right2 - left2 > right - left)
        {
            left = left2;
            right = right2;
        }
    }
    // substr（start，length）：提取特定字符串
    return s.substr(left, right-left+1);
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi)
