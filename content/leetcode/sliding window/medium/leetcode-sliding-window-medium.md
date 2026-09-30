+++
title = "3、438"
problems = [3, 438, 209, 1493]
+++

#### <font style="color:#DF2A3F;">第三题</font>：[无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)

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
#### <font style="color:#DF2A3F;">第四百三十八题</font>：[找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)

思路：从左往右移动窗口，每次移动一格；移动的过程中不断**对 left 与 right 指向的元素进行“是否存在于‘p’中“的判断**——如果存在，那么对应字符的出现频率减一.....直到最后整个哈希表清零，就可以认为这个窗口中的元素满足条件，将其存入res中
```cpp

vector<int> findAnagrams(string s, string p)

{

    int ns = s.size(), np = p.size();

    if(ns < np) return {};

    std::vector<int> res;



    std::vector<int> count(26, 0);

    for(auto c : p) count[c - 'a']++;



    int left = 0, right = 0, need = np;

    while(right < ns)

    {

        char c = s[right];

        // 扩大窗口

        if(count[c - 'a'] > 0) need--;

        count[c - 'a']--;

        right++;



        // 缩小窗口

        if(right - left > np)

        {

            char d = s[left];

            if(count[d - 'a'] >= 0) need++;

            count[d - 'a']++;

            left++;                

        }



        if(need == 0) res.push_back(left);

    }

    return res;

}
```

<a id="A5ODj"></a>
#### 第二百零九题：[长度最小的子数组](<https://leetcode.cn/problems/minimum-size-subarray-sum/>)

<a id="ue4eb73e4"></a>使用到的是滑动窗口

<a id="tcFqA"></a>
minSubArrayLen（）
```cpp
int minSubArrayLen(int target, vector<int>& nums)
{
    int n = nums.size(), sum = 0, left = 0;
    // 因为最后的结果输出的是子数组长度
    // 所以最大长度肯定不会超过原数组长度 n
    int res = n + 1;
    // 遍历右边的节点
    for(int right = 0; right < n; right++)
    {
        // 首先将右指针指向的节点加到 sum 中
        sum += nums[right];
        // 不断缩小窗口
        while(target <= sum - nums[left])
        {
            sum -= nums[left];
            // 左端点右移
            left++;
        }
        // 此时经过缩小之后，如果 sum 仍然大于等于 target
        // 就记录一次答案
        if(target <= sum)
        {
            res = std::min(res, right - left + 1);
        }
    }
    return res == n + 1 ? 0 : res;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/yg57x00m0sytet7u)

<a id="eN0b2"></a>
#### 第一千四百九十三题：[删掉一个元素以后全为 1 的最长子数组](<https://leetcode.cn/problems/longest-subarray-of-1s-after-deleting-one-element/>)

<strong>原笔记（代码待复核）</strong>



<a id="uffe18c70"></a>维护一个滑动窗口，窗口内只能存在一个零，同时每一步都动态更新最长子数组的长度

<a id="u6312f1b2"></a>当窗口内零的数量大于一时，将左边界右移，直到零的数量变为一

<a id="on0TP"></a>
longestSubarray（）
```cpp
int longestSubarray(vector<int>& nums)
{
    int left = 0, zero_count = 0, res = 0;

    for(int right = 0; right < nums.size(); right++)
    {
        if(nums[right] == 0)
            zero_count++;

        while(1 < zero_count)
        {
            if(nums[left] == 0)
                zero_count--;

            left++;
        }

        res = std::max(right - left + 1 - 1,);
    }
    return res;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/yg57x00m0sytet7u)

