+++
slug = "best-time-to-buy-and-sell-stock-ii"
title = "买卖股票的最佳时机 II"
problems = [122]
problem_id = 122
difficulty = "Medium"
weight = 122
summary = "买卖股票的最佳时机 II的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/hak76l9s3kallgv4"
+++

题目：[买卖股票的最佳时机 II](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/)


<a id="第一百二十二题买卖股票的最佳时机-ii"></a>

<a id="ExiUo"></a>

<a id="u7800f54b"></a>参考：<a id="mnH4W"></a>[https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/solutions/12625/best-time-to-buy-and-sell-stock-ii-zhuan-hua-fa-ji/?envType=problem-list-v2&amp;envId=91oI3WTD](<https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/solutions/12625/best-time-to-buy-and-sell-stock-ii-zhuan-hua-fa-ji/?envType=problem-list-v2&envId=91oI3WTD>)

<a id="u1ac055c4"></a>对于连续上涨的情况，第一天买，最后一天卖，可以使得利润最大化，此时利润 profit 等于 p\_n - p\_1，等价于（p\_n - p\_n-1) + (p\_n-1 - p\_n-2) + .... + (p\_2 - p\_1)，也就是说，可以将其分解为前一天买，下一天买，即每天都进行交易

<a id="ufcb53823"></a>对于连续下跌的情况，不进行任何交易（即利润为零）可以使得利润最大；

<a id="VOZLv"></a>
maxProfit（）
```cpp
int maxProfit(vector<int>& prices)
{
    int res = 0;
    // 只遍历一遍数组
    for(int i = 1; i < prices.size(); i++)
    {
        // 计算两天之间的利润
        int temp = prices[i] - prices[i - 1];
        // 只有当利润大于零时才记入总利润
        if(0 < temp) res += temp;
    }
    return res;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/hak76l9s3kallgv4)
