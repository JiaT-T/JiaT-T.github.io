---
title: "LeetCode 入门题组笔记"
slug: "leetcode-overview"
summary: "记录最长回文子串、整数反转、字符串转整数、回文数和最长公共前缀的思路与 C++ 实现。"
categories: ["LeetCode"]
tags: ["LeetCode", "C++", "字符串", "基础算法"]
date: "2026-03-17T07:29:04.000Z"
lastmod: "2026-05-27T03:48:13.000Z"
draft: false
yuque_slug: "trgf9fggzg79cepi"
source: "https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi"
problems: [5, 7, 8, 9, 14]
---

<a id="LbCzn"></a>
#### 

<a id="zoPCj"></a>
#### <span style="color: #DF2A3F">第五题</span>：[<span style="color: inherit">最长回文子串</span>](<https://leetcode.cn/problems/longest-palindromic-substring/>)

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

<a id="vjwgC"></a>
#### <span style="color: #DF2A3F">第七题</span>：[<span style="color: inherit">整数反转</span>](<https://leetcode.cn/problems/reverse-integer/>)

<a id="u80f4573e"></a><span style="color: inherit">通过对输入数字模10得到最低位的数字，然后将输入数字除10，减少输入数字的一位位数，使用此数字进行下一轮循环，直到输入数字最终等于零</span>

<a id="u006283f7"></a><span style="color: inherit">注意：在循环过程中，可能出现溢出的情况，因此需要在每一次循环开始前对已经反转的数字进行范围判断，如果已经溢出，则返回零</span>

<a id="OtMzj"></a>
reverse() 
```cpp
int reverse(int x) 
    {
        int rev = 0;
        while(x != 0)
        {
            if(rev < INT_MIN/10 || rev > INT_MAX/10) return 0;
            int d = x % 10;
            x /= 10;
            rev = rev * 10 + d;
        }
        return rev;
    }
```

<a id="MoKD1"></a>
#### <span style="color: #DF2A3F">第八题</span>：[<span style="color: rgb(10, 132, 255)">字符串转换整数 (atoi)</span>](<https://leetcode.cn/problems/string-to-integer-atoi/>)

<a id="uff3cbf62"></a>根据题目的要求逐步实现函数功能：

<a id="u0f40be6c"></a>1.空格：读入字符串并丢弃前导空格--在循环外定义字符串下标，通过while循环判断前面的字符是否为“ ”，如果是，则i加一并进入下一次是否为空格的判断

<a id="u6481a35b"></a>2.符号：检查下一个字符为“-”还是“+”--通过if判断之后的字符有无符号，有则将sign标记为-1或1（在得出了最后的数字之后乘上），没有则默认为1

<a id="uc3171c76"></a>3.转换：跳过前置零，直至最后一个字符--这里的零不用单独写一条if语句来判断，可以通过与上一题相同的方法来解决（rev = rev \*10 + d）。要注意的是，string使用【】得出的是char类型的字符，而不是整数，需要减去‘0’才能变为int类型

<a id="ucec30b32"></a>4.舍入：范围 `[−231,  231 − 1]`--在进行转换之前需要先对上一次的计算结果进行范围判断，如果大于INT\_MAX/10或等于INT\_MAX/10但是下一位大于7，则直接返回上一次的值（原因：如果上一次的值已经大于了INT\_MAX/10，那么经过这次的循环之后，必然会超出范围；又因为最大值是`231 − 1`，因此在等于INT\_MAX的情况下，个位最大值只能是7）

<a id="jNhK5"></a>
myAtoi() 
```cpp
int myAtoi(string s) 
    {
        int i = 0, result = 0, sign = 1;
        while(i < s.size() && s[i] == ' ') i++;
        if(i == s.size()) return 0;
        if(s[i] == '-' || s[i] == '+')
        {
            sign = s[i] == '-' ? -1 : 1;
            i++;
        }
        while(i < s.size() && s[i] >= '0' && s[i] <= '9')
        {
            int digit = s[i] - '0';
            if(result > INT_MAX / 10 || (result == INT_MAX / 10 && digit > 7))
                return sign == 1 ? INT_MAX : INT_MIN;
            result = result * 10 + digit;
            i++;
        }
        return result * sign;
    }
```

<a id="yRBbC"></a>
#### <span style="color: #DF2A3F">第九题</span>：[<span style="color: inherit">回文数</span>](<https://leetcode.cn/problems/palindrome-number/>)

<a id="u71bbcfa6"></a><span style="color: inherit">因为负数不可能为回文数，所以直接排除</span>

<a id="u74988073"></a><span style="color: inherit">之后就和之前的题目一样，把反转后的数字再与原数字比较就行</span>

<a id="ub8e73afd"></a><span style="color: inherit">（注意：这里使用int会报错--超出了类型范围，所以改用了unsigned int，因为负数在第一关就被筛掉了）</span>

<a id="kIIqv"></a>
isPalindrome() 
```cpp
bool isPalindrome(int x) 
    {
        if(x < 0) return false;
        unsigned int result = 0, x_copy = x;
        while(x != 0)
        {
            unsigned int a = x % 10;
            x /= 10;
            result = result * 10 + a;
        }
        if(result == x_copy)
            return true;
        return false;
    }
```

<a id="cujuE"></a>
#### 

<a id="QLYAs"></a>
#### 

<a id="AWZDC"></a>
#### 

<a id="kXHuc"></a>
#### <span style="color: #DF2A3F">第十四题</span>：[<span style="color: rgb(10, 132, 255)">最长公共前缀</span>](<https://leetcode.cn/problems/longest-common-prefix/>)

<a id="uf0a9421e"></a>思路：从第一个元素的第一个字符开始，先逐渐向后遍历，检查第一个字符是否都相同，然后再进行第二个字符的遍历.....直到出现不同的字符，然后返回公共前缀

<a id="u9f81048b"></a>结尾的“return strs【0】”代表着：如果循环正常结束，就说明第一个元素就是公共的前缀

<a id="f2gA1"></a>
longestCommonPrefix（）
```cpp
string longestCommonPrefix(vector<string>& strs)
    {
        if(strs.empty()) return "";

        for(int i = 0; i < strs[0].length(); i++)
        {
            for(int j = 0; j < strs.size(); j++)
            {
                if(i == strs[j].length() || strs[j][i] != strs[0][i])
                    return std::string(strs[0].substr(0, i));
            }
        }
        return strs[0];
    }
```

<a id="tb3Ir"></a>
#### 

<a id="ADPJG"></a>
#### 

<a id="rlJ4S"></a>
#### 

<a id="Xp1bE"></a>
#### 

<a id="n55JW"></a>
#### 

<a id="vfqUX"></a>
#### 

<a id="Acr0E"></a>
#### 

<a id="PZjti"></a>
#### 

<a id="FluPn"></a>
####

原文：[LeetCode](<https://www.yuque.com/u62694975/iaaa/trgf9fggzg79cepi>)
