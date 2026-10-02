+++
categories = ["LeetCode"]
tags = ["LeetCode", "C++", "数组"]
date = "2026-04-21T09:45:56.000Z"
lastmod = "2026-05-09T05:18:34.000Z"
draft = false
yuque_slug = "xt819i2tgf9y60tp"
source = "https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp"
slug = "rotate-array"
title = "轮转数组"
problems = [189]
problem_id = 189
difficulty = "Medium"
weight = 189
summary = "轮转数组的解题思路与 C++ 实现。"
+++

题目：[轮转数组](https://leetcode.cn/problems/rotate-array/)


<a id="第一百八十九题"></a>

<a id="lNKTO"></a>

<a id="u12d73c81"></a><span style="background-color: #FBDE28">解法一：</span>

<a id="u53438d50"></a>思路比较简单，仅仅是将移动后的元素存放到另一个数组

<a id="u09456f75"></a>具体实现：

<a id="ub5828545"></a>因为轮转的特性，每当移动的次数是数组大小的整数倍时，就相当于完全没有变化，使所以直接返回

<a id="u3da61a99"></a>之后再通过一轮遍历，将原数组中的元素进行移动即可

<a id="vMC3H"></a>
rotate（）
```cpp
// 解法一：
void rotate(vector<int>& nums, int k)
{
    int sz = nums.size();
    if(k % sz == 0) return;

    std::vector<int> vec(sz, 0);
    for(int i = 0; i < sz; i++)
    {
        int index = (i + k) % sz;
        vec[index] = nums[i];
    }
    nums = vec;
}
```

<a id="u0ab2ba35"></a><span style="background-color: #FBDE28">解法二：</span>

<a id="u676df0a0"></a>PS：突然发现我可能是个傻逼😅😅😅😅😅😅😅😅😅😅😅😅😅😅

<a id="u4f312c3e"></a>参考了这里的解法：[189. 轮转数组 - 力扣（LeetCode）](<https://leetcode.cn/problems/rotate-array/solutions/2784427/tu-jie-yuan-di-zuo-fa-yi-tu-miao-dong-py-ryfv/?envType=study-plan-v2&envId=top-100-liked>)

<a id="u4820c476"></a>思路如下：

<a id="uef41c79d"></a>假设现在有一个数组&#91;1,2,3,4,5,6,7&#93;，需要变换成&#91;5,6,7,1,2,3,4&#93;

<a id="ud395b83c"></a>可以将转换后的数组视为：&#91;5,6,7&#93; + &#91;1,2,3,4&#93;

<a id="ua39b61ea"></a>首先要确保的是&#91;5,6,7&#93;在&#91;1,2,3,4&#93;前面，这可以通过翻转整个数组得到——&gt; &#91;7,6,5,4,3,2,1&#93;

<a id="u70be4db9"></a>之后就只需要对&#91;7,6,5&#93; 和 &#91;4,3,2,1&#93;两个子数组进行翻转就可以得到最终的结果

<a id="u354dc14e"></a>如此，即可将复杂的移动操作转换为反转操作

<a id="uyW8d"></a>
rotate（）
```cpp
// 解法二：
void rotate(vector<int>& nums, int k)
{
    k %= nums.size();
    ranges::reverse(nums);
    std::reverse(nums.begin(), nums.begin() + k);
    std::reverse(nums.begin() + k, nums.end());
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp)
