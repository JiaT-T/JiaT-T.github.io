+++
title = "3、438"
problems = [3, 438]
+++

\#### <font style="color:#DF2A3F;">第三题</font>：\[无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)

用到的是滑动窗口和unorder\_map,



通过两个条件限制窗口范围：



1.当（left，right）存在重复字符时，那么（left，right+1.....right+n）都存在重复数值



2.当（left，right）不存在重复字符时，那么（left+1....left+n，right）都不存在重复字符



因此，（left，right+1.....right+n）与（left+1....left+n，right）都不需要再去进行遍历



\*\*核心：用unordered\_map记录每个字符的出现次数\*\*



```cpp

int lengthOfLongestSubstring(string s) 

{

&nbsp;   int maxStr = 0; // 用来记录出现过的“最长”无重复子串的长度。

&nbsp;   

&nbsp;   // 这里的 um (unordered\_map) 是核心工具。

&nbsp;   // Key (char): 窗口里的字符 

&nbsp;   // Value (int): 这个字符在当前窗口里出现了几次

&nbsp;   std::unordered\_map<char, int> um; 

&nbsp;   

&nbsp;   // 开始滑动窗口。一开始，左右边界都在最左边（索引 0）。

&nbsp;   // right++ 代表窗口的右边缘在不断向右扩展，吞进新的字符。

&nbsp;   for(int left = 0, right = 0; right < s.size(); right++)

&nbsp;   {

&nbsp;       // s\[right] 是刚刚进入窗口的新字符。

&nbsp;       // um\[s\[right]]++ 的意思是：让这个新字符的出现次数 +1。

&nbsp;       um\[s\[right]]++; 

&nbsp;   

&nbsp;       // 检查刚刚吞进来的字符，是不是导致窗口里有重复了？

&nbsp;       // 如果 > 1，说明这个字符之前已经在窗口里存在了。

&nbsp;       while(um\[s\[right]] > 1) 

&nbsp;       {

&nbsp;           // 既然有重复了，就缩小窗口：

&nbsp;           // 把最左边的字符 s\[left] 踢出窗口，所以它的出现次数 -1。

&nbsp;           um\[s\[left]]--; 

&nbsp;           // 左边界向右移动一格，窗口缩小。

&nbsp;           left++;        

&nbsp;       }

&nbsp;       

&nbsp;       // 此时认为窗口里已经没有重复字符了。

&nbsp;       // right - left + 1 就是当前窗口的长度。

&nbsp;       // 比如 left=0, right=2，长度就是 2 - 0 + 1 = 3。

&nbsp;       // 用 std::max 更新历史最大长度。

&nbsp;       maxStr = std::max(maxStr, right - left + 1); 

&nbsp;   }

&nbsp;   return maxStr; // 遍历完整个字符串，返回找到的最大值。

}

```







\#### <font style="color:#DF2A3F;">第四百三十八题</font>：\[找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)

思路：从左往右移动窗口，每次移动一格；移动的过程中不断\*\*对 left 与 right 指向的元素进行“是否存在于‘p’中“的判断\*\*——如果存在，那么对应字符的出现频率减一.....直到最后整个哈希表清零，就可以认为这个窗口中的元素满足条件，将其存入res中



```cpp

vector<int> findAnagrams(string s, string p)

{

&nbsp;   int ns = s.size(), np = p.size();

&nbsp;   if(ns < np) return {};

&nbsp;   std::vector<int> res;



&nbsp;   std::vector<int> count(26, 0);

&nbsp;   for(auto c : p) count\[c - 'a']++;



&nbsp;   int left = 0, right = 0, need = np;

&nbsp;   while(right < ns)

&nbsp;   {

&nbsp;       char c = s\[right];

&nbsp;       // 扩大窗口

&nbsp;       if(count\[c - 'a'] > 0) need--;

&nbsp;       count\[c - 'a']--;

&nbsp;       right++;



&nbsp;       // 缩小窗口

&nbsp;       if(right - left > np)

&nbsp;       {

&nbsp;           char d = s\[left];

&nbsp;           if(count\[d - 'a'] >= 0) need++;

&nbsp;           count\[d - 'a']++;

&nbsp;           left++;                

&nbsp;       }



&nbsp;       if(need == 0) res.push\_back(left);

&nbsp;   }

&nbsp;   return res;

}

```



