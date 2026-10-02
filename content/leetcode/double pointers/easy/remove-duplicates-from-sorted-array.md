+++
slug = "remove-duplicates-from-sorted-array"
title = "删除有序数组中的重复项"
problems = [26]
problem_id = 26
difficulty = "Easy"
weight = 26
summary = "删除有序数组中的重复项的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq"
+++

题目：[删除有序数组中的重复项](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/)


## 笔记 1 {#note-1}


<a id="第二十六题删除有序数组中的重复项"></a>

<a id="PZjti"></a>

<a id="uc2b2cb1d"></a>使用的是双指针

<a id="u3c384589"></a>这里如果使用最原始的方法：如果当前元素与上一个相同则删除(erase），会导致O(n^2)的时间复杂度——————erase（）会将删除元素后面的元素向前移动

<a id="u4fa07d21"></a>而这里，我们定义了两个指针，一个慢指针（k），一个快指针（i）；将两个指针对应的值进行比较，如果不同，就将慢指针后移，同时将慢指针所指元素覆盖为当前元素

<a id="u13339e5b"></a>在这个方法中，我们并没有真正执行“删除”操作，而是对数组进行了重新排列，将重复的元素放到数组末尾，因为最终的返回值是有效的数字个数，因此末尾的区域也就会变成垃圾数据，不需要再去关心它们

<a id="Iw5u9"></a>
removeDuplicates（）
同一份实现已收录于[第 26 题解法](#note-2)。

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq)

## 笔记 2 {#note-2}


<a id="第二十六题"></a>



使用的是双指针

这里如果使用最原始的方法：如果当前元素与上一个相同则删除(erase），会导致O(n^2)的时间复杂度——————erase（）会将删除元素后面的元素向前移动

而这里，我们定义了两个指针，一个慢指针（k），一个快指针（i）；将两个指针对应的值进行比较，如果不同，就将慢指针后移，同时将慢指针所指元素覆盖为当前元素

在这个方法中，我们并没有真正执行“删除”操作，而是对数组进行了重新排列，将重复的元素放到数组末尾，因为最终的返回值是有效的数字个数，因此末尾的区域也就会变成垃圾数据，不需要再去关心它们

```cpp
int removeDuplicates(vector<int>& nums)
    {
        if(nums.empty()) return 0;

        int k = 0;
        for(int i = 1; i < nums.size(); i++)
        {
            if(nums[i] != nums[k])
            {
                k++;
                nums[k] = nums[i];
            }
        }
        return k + 1;
    }
```
