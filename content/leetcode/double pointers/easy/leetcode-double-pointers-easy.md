---
title: "LeetCode 双指针：简单题组"
slug: "leetcode-double-pointers-easy"
summary: "记录移除元素、验证回文串和移动零的双指针思路与 C++ 实现。"
categories: ["LeetCode"]
tags: ["LeetCode", "C++", "双指针"]
date: "2026-04-11T05:23:52.000Z"
lastmod: "2026-06-30T04:18:45.000Z"
draft: false
yuque_slug: "ilsg74kn6vu4qdhw"
source: "https://www.yuque.com/u62694975/iaaa/ilsg74kn6vu4qdhw"
problems: [27, 125, 283]
---

<a id="yz2me"></a>
#### <span style="color: #DF2A3F">第二十七题</span>：[<span style="color: inherit">移除元素</span>](<https://leetcode.cn/problems/remove-element/>)

<a id="u52742daf"></a>解法一：

<ol data-yuque-indent="1" style="margin-left: 2em"><li id="u579eacb1"><span id="u9ff48d23">先对整个数组进行排序，将相同元素堆到一起</span></li><li id="u75357cb9"><span id="ueabdace5">然后通过两次遍历找到重复元素的起始、终止下标</span></li><li id="u4f0e98c4"><span id="uec0f0271">最后一键清除</span></li></ol>

<a id="j1OWQ"></a>
removeElement（）
```cpp
int removeElement(vector<int>& nums, int val) 
{
    std::sort(nums.begin(), nums.end());
    int start = 0;
    while(start < nums.size() && nums[start] != val)
    {
        start++;
    }
    if(start == nums.size()) return nums.size();
    int end = start;
    while(end < nums.size() && nums[end] == val)
    {
        end++;
    }

    nums.erase(nums.begin() + start, nums.begin() + end);
    return nums.size();
}
```

<a id="u631fc81b"></a>解法二：  
       使用到的是<strong>快慢指针</strong>

<a id="u98d76299"></a>快指针负责遍历整个数组，慢指针负责指向下一个“不等于 val”的元素的位置

<a id="u57a36819"></a>如果 fast 指向的不是 val，就将这个元素放到前面去，最后 slow 前面的元素代表的就全是“不等于 val”的数字

<a id="bGeZo"></a>
removeElement（）
```cpp
int removeElement(vector<int>& nums, int val) 
{
    int slow = 0, fast = 0;
    for(; fast < nums.size(); fast++)
    {
        if(nums[fast] != val)
        {
            nums[slow] = nums[fast];
            slow++;
        }
    }
    return slow;
}
```

<a id="pwggh"></a>
#### <span style="color: #DF2A3F">第一百二十五题</span>：[<span style="color: inherit">验证回文串</span>](<https://leetcode.cn/problems/valid-palindrome/>)

<a id="qZpKX"></a>
isPalindrome（）
```cpp
bool isPalindrome(string s)
{
    if(s.size() == 1) return true;
    // 定义左右指针
    int left = 0, right = s.size() - 1;
    // 不需要考虑 left = right 的情况
    // 因为中间多一个字符的情况可以直接当作偶数串处理
    while(left < right)
    {
        // 拿到左边的数字或字符
        while(left < right && !isalnum(s[left]))
        {
            left++;
        }

        // 拿到右边的数字或字符
        while(left < right && !isalnum(s[right]))
        {
            right--;
        }

        // 如果是大写就将其转换为小写
        // 如果已经是小写或数字就原样返回
        if(std::tolower(s[left]) != std::tolower(s[right])) return false;
        // 移动指针
        left++;right--;
    }
    return true;
}
```

<a id="GlvDn"></a>
#### <span style="color: #DF2A3F">第二百八十三题</span>：[<span style="color: inherit">移动零</span>](<https://leetcode.cn/problems/move-zeroes/>)

<a id="uf68262a9"></a>思路：使用两个指针，一个从前往后对数组进行遍历，另一个始终指向前端的非零元素；只要指针 i 指向的元素非零，就将指针 k 当前指向的元素赋值为 num&#91;i&#93; ，最后再将指针 k 后面的元素全部置为零即可

<a id="QKl0t"></a>
moveZeroes（）
```cpp
void moveZeroes(vector<int>& nums) 
{
    int k = 0;
    for(int i = 0; i < nums.size(); i++)
    {
        if(nums[i] != 0)
        {
            nums[k] = nums[i];
            k++;
        }
    }
    for(int j = k; j < nums.size(); j++)
    {
        nums[j] = 0;
    }
}
```

原文：[easy](<https://www.yuque.com/u62694975/iaaa/ilsg74kn6vu4qdhw>)
