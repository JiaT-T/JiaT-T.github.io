+++
title = "121"
problems = [121, 976]
+++

#### <font style="color:#DF2A3F;">第一百二十一题</font>：[买卖股票的最佳时机](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/)
思路：

所谓贪心算法，就是每个步骤都挑选局部最优解，从而最终达到全局最优解的效果

在这题中，”贪心“体现在——**在遍历过程中，每次都只将当前价格与之前遇到的最低价格进行利润计算**

这样就可以避免不必要的计算

具体实现如下：

```cpp
int maxProfit(vector<int>& prices) 
{
    if(prices.empty()) return 0;
    int max_profit = 0, min_price = prices[0];
    for(int price : prices)
    {
        if(price < min_price)
            min_price = price;
        else
        {
            int curr_profit = price - min_price;
            max_profit = curr_profit < max_profit ? max_profit : curr_profit;
        }
    }
    return max_profit;
}
```

<a id="kgIWj"></a>
#### 第九百七十六题：[三角形的最大周长](<https://leetcode.cn/problems/largest-perimeter-triangle/>)

<a id="u8be6cfe1"></a>先将数组进行排序，之后从后往前进行遍历，每次判断上一个元素与上上个元素之和是否大于当前元素（三角形两边之和大于第三边）

<a id="uea478a54"></a>如果条件满足，直接计算周长并返回；否则，进入下一次循环

<a id="DhRqC"></a>
largestPerimeter（）
```cpp
int largestPerimeter(vector<int>& nums)
{
    std::sort(nums.begin(), nums.end());
    int res = 1;
    for(int i = nums.size() - 1; 2 <= i; --i)
    {
        if(nums[i - 1] + nums[i - 2] > nums[i])
            return nums[i] + nums[i - 1] + nums[i - 2];
        else
            continue;
    }
    return 0;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ne188hgk5rxky939)

