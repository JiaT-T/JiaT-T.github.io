+++
slug = "longest-substring-without-repeating-characters"
title = "无重复字符的最长子串"
problems = [3]
problem_id = 3
difficulty = "Medium"
weight = 3
summary = "无重复字符的最长子串的解题思路与 C++ 实现。"
+++

题目：[无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)


<a id="第三题无重复字符的最长子串"></a>



用到的是滑动窗口和unorder_map,



通过两个条件限制窗口范围：



1.当（left，right）存在重复字符时，那么（left，right+1.....right+n）都存在重复数值



2.当（left，right）不存在重复字符时，那么（left+1....left+n，right）都不存在重复字符



因此，（left，right+1.....right+n）与（left+1....left+n，right）都不需要再去进行遍历



**核心：用unordered_map记录每个字符的出现次数**
```cpp

int lengthOfLongestSubstring(string s)

{

    int maxStr = 0; // 用来记录出现过的“最长”无重复子串的长度。



    // 这里的 um (unordered_map) 是核心工具。

    // Key (char): 窗口里的字符

    // Value (int): 这个字符在当前窗口里出现了几次

    std::unordered_map<char, int> um;



    // 开始滑动窗口。一开始，左右边界都在最左边（索引 0）。

    // right++ 代表窗口的右边缘在不断向右扩展，吞进新的字符。

    for(int left = 0, right = 0; right < s.size(); right++)

    {

        // s[right] 是刚刚进入窗口的新字符。

        // um[s[right]]++ 的意思是：让这个新字符的出现次数 +1。

        um[s[right]]++;



        // 检查刚刚吞进来的字符，是不是导致窗口里有重复了？

        // 如果 > 1，说明这个字符之前已经在窗口里存在了。

        while(um[s[right]] > 1)

        {

            // 既然有重复了，就缩小窗口：

            // 把最左边的字符 s[left] 踢出窗口，所以它的出现次数 -1。

            um[s[left]]--;

            // 左边界向右移动一格，窗口缩小。

            left++;

        }



        // 此时认为窗口里已经没有重复字符了。

        // right - left + 1 就是当前窗口的长度。

        // 比如 left=0, right=2，长度就是 2 - 0 + 1 = 3。

        // 用 std::max 更新历史最大长度。

        maxStr = std::max(maxStr, right - left + 1);

    }

    return maxStr; // 遍历完整个字符串，返回找到的最大值。

}
```
