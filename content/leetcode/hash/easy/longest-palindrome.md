+++
slug = "longest-palindrome"
title = "最长回文串"
problems = [409]
problem_id = 409
difficulty = "Easy"
weight = 409
summary = "最长回文串的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/iyctdall69ru0wes"
+++

题目：[最长回文串](https://leetcode.cn/problems/longest-palindrome/)


<a id="第四百零九题最长回文串"></a>

<a id="IWZSs"></a>

<a id="ua2c36845"></a>思路：对于出现次数为偶数个的字符，可以直接将其添加至回文字符串两端；对于出现次数为奇数个的字符，最多取其中的 （ct - 1）个添加至两端，最后还可以从奇数字符中拿出一个放在最中间

<a id="C8IR9"></a>
longestPalindrome（）
```cpp
int longestPalindrome(string s)
{
    if(s.size() <= 1) return s.size();

    // 统计字符出现次数
    std::unordered_map<char, int> um;
    for(char c : s)
    {
        um[c]++;
    }

    int length = 0;
    bool has_odd = false;
    for(const auto& [ch, cnt] : um)
    {
        // 利用 int 的向下取整性质
        // 可以将奇偶的情况统一处理
        length += (cnt / 2) * 2;
        // 判断是否存在奇数出现次数
        if(cnt % 2 == 1)
        {
            has_odd = true;
        }
    }
    // 如果 s 中含有奇数出现次数的字符
    // 就在中间再加上这个字符（长度加一）
    return length + (has_odd ? 1 : 0);
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/iyctdall69ru0wes)
