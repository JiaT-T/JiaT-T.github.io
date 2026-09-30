---
title: "LeetCode 普通数组：中等题组"
slug: "leetcode-array-medium"
summary: "记录最大子数组和、合并区间、轮转数组及除自身以外数组乘积的思路与 C++ 实现。"
categories: ["LeetCode"]
tags: ["LeetCode", "C++", "数组"]
date: "2026-04-21T09:45:56.000Z"
lastmod: "2026-05-09T05:18:34.000Z"
draft: false
yuque_slug: "xt819i2tgf9y60tp"
source: "https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp"
problems: [53, 56, 189, 238]
---

<a id="Otsui"></a>
#### <span style="color: #DF2A3F">第五十三题</span>：[<span style="color: inherit">最大子数组和</span>](<https://leetcode.cn/problems/maximum-subarray/>)

<a id="u2f40c28a"></a>核心判断条件：

<a id="ubdb70aea"></a><strong>如果前一段子序列之和与当前元素相加之后，还没有当前元素本身大，那么就直接从当前元素开始重新计算</strong>

<a id="u053f6147"></a>具体实现：

<a id="uabdb2f4d"></a>首先定义两个和，一个用于记录目前为止的最大和（max\_val），一个用于在循环中进行判断（curr\_val）

<a id="udb81649a"></a>之后进入循环，通过上述判断条件对当前最大和进行更新，再用当前最大和与之前保持的最大和进行比较

<a id="w6FY6"></a>
maxSubArray（）
```cpp
int maxSubArray(vector<int>& nums)
{
    int curr_val = nums[0];
    int max_val = nums[0];

    for(int i = 1; i < nums.size(); i++)
    {
        if(curr_val + nums[i] < nums[i])
            curr_val = nums[i];
        else
            curr_val = curr_val + nums[i];
        
        if(curr_val > max_val)
            max_val = curr_val;
    }
    return max_val;
}
```

<a id="wKqUt"></a>
#### <span style="color: #DF2A3F">第五十六题</span>：[<span style="color: inherit">合并区间</span>](<https://leetcode.cn/problems/merge-intervals/>)

<a id="u3258046e"></a>思路：

<a id="u28d6402e"></a>难点在于“如何对重叠区间进行合并”，这里选用的判断条件是---如果当前区间左边界小于结果数组尾部区间的右边界，则选取两者中更大的右边界进行合并

<a id="ud472c054"></a>具体实现：

<a id="u98f74a5e"></a>首先以左边界为基准对原数组进行了排序，这样就能从左往右更好地判断是否重叠

<a id="u8621cd47"></a>这里使用到了<span style="background-color: #FBDE28">lambda表达式</span>，它的语法是：

<a id="u6346a97d"></a>// &#91;捕获列表&#93;(参数列表) -&gt;  返回值类型     { 函数体 }

<a id="ub8365dcb"></a>auto    my\_func = &#91; &#93;(int a, int b) { return a + b; };

<a id="uea2275aa"></a>但实际上，<strong>返回值类型</strong>通常可以省略，让编译器自己去猜。所以最常用的长这样：

<a id="u145689cb"></a>`[] (int a, int b) { return a + b; }`

<a id="uf057c0ee"></a>至于这里为什么是直接在res中进行修改，这是因为可以避免多次push\_back的开销

<a id="wti4B"></a>
merge（）
```cpp
vector<vector<int>> merge(vector<vector<int>>& intervals)
{
    if(intervals.empty()) return {};
    std::sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b){return a[0] < b[0];});

    vector<vector<int>> res{intervals[0]};

    for(int i = 1; i < intervals.size(); i++)
    {
        // 当前元素左边界小于等于上一个区间右边界 -->  发生重合！
        if(intervals[i][0] <= res.back()[1]) 
            // 取更大的有边界合并
            res.back()[1] = std::max(res.back()[1], intervals[i][1]);
        else
            res.push_back(intervals[i]);
    }
    return res;
}
```

<a id="lNKTO"></a>
#### <span style="color: #DF2A3F">第一百八十九题</span>：[<span style="color: inherit">轮转数组</span>](<https://leetcode.cn/problems/rotate-array/>)

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

<a id="wiZba"></a>
#### <span style="color: #DF2A3F">第二百三十八题</span>：[<span style="color: inherit">除了自身以外数组的乘积</span>](<https://leetcode.cn/problems/product-of-array-except-self/>)

<a id="uf0bff13e"></a>思路如下：

<a id="u05d775e0"></a>因为不能使用除法——通过一次遍历计算整个数组的乘积，之后再进行一次遍历，每次除以当前元素的值

<a id="u24d464c0"></a>同时要求时间复杂度是O(n)，空间复杂度要求是O(1)，但是输出的数组不计入额外空间，所以需要直接对输出数组进行操作；

<a id="ub1aa922e"></a>可以先通过一次遍历计算出左边的乘积，再从后往前进行一次遍历，将右边的乘积再乘到res的当前元素上去，这样最终得到的res数组就是除自身外的元素的乘积

<a id="ua419e9af"></a>注：这里需要提前预留好res的空间，而不是在循环中每次都调用push\_back

<a id="GsEGy"></a>
productExceptSelf（）
```cpp
vector<int> productExceptSelf(vector<int>& nums)
{
    const int sz = nums.size();
    std::vector<int> res(sz);
    res[0] = 1;

    int temp = 1;
    for(int i = 0; i < sz; i++)
    {
        res[i] = temp;
        temp *= nums[i];
    }

    temp = 1;
    for(int j = sz - 1; 0 <= j; j--)
    {
        res[j] *= temp;
        temp *= nums[j];
    }

    return res;
}
```

原文：[medium](<https://www.yuque.com/u62694975/iaaa/xt819i2tgf9y60tp>)
