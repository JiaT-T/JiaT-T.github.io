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
