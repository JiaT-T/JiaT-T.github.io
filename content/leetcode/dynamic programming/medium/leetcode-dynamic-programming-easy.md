+++
title = "139、152、198、279、300、322、416"
+++

#### <font style="color:#DF2A3F;">第一百三十九题</font>：[单词拆分](https://leetcode.cn/problems/word-break/)
    1. 确定状态：dp[ i ] 代表前 i 个字符组成的字符串是否能够被拆分
    2. 状态转移：dp[ i ] = (**dp[ j ]** && **s.substr(j, i - j)**也能够被拆分)，其中 j 为区间 [ 0, i ] 的任意整数



具体实现：

首先将字典转换为无序集合，提高查找速度；原字符串拷贝至string_view类型，以实现零开销访问范围内的部分字符串；最后定义dp数组，用来记录前 i 个字符能否被拆分，注意这里的首位元素为真，因为空字符串肯定是能够被拆分的，其他位默认为假

进入循环——外层循环遍历原字符串，内层循环遍历字典；之后根据上述的 b 条件，确定字符串前i个元素是否能拆分

```cpp
bool wordBreak(string s, vector<string>& wordDict)
{
    std::unordered_set<string_view> dict(wordDict.begin(), wordDict.end());
    std::string_view sv = s;
    std::vector<bool> dp(s.size() + 1, false);
    dp[0] = true;

    for(int i = 1; i <= s.size(); i++)
    {
        for(int j = 0; j < i; j++)
        {
            if(dp[j] && dict.find(sv.substr(j, i - j)) != dict.end()) 
            {
                dp[i] = true;
                break;
            }
        }
    }
    return dp[s.size()];
}
```

#### <font style="color:#DF2A3F;">第一百九十八题</font>：[打家劫舍](https://leetcode.cn/problems/house-robber/)
1.状态定义：

dp[i]指的是”到达第i个房子时，目前为止能偷到的最大金额是多少“

2.转移方程：

用一个例子来解释——

假如当前已经偷完了前3栋房子，来到了第四栋房子（里面有num元）

那么现在就有两个选择：

1).不偷第四栋房子，那么金额就是dp[3]（也就是前三栋房子的最优结果）

2).偷第四栋房子，那么总金额就是dp[i-1] + num（前两栋房子的最优结果加上第四栋房子）

因此，前四栋房子的最大金额就是两者中的更大者

```cpp
int rob(vector<int>& nums)
{
    int pre = 0, curr = 0;
    int temp;
    for(int num : nums)
    {
        temp = curr;
        curr = std::max(pre + num, curr);
        pre = temp;
    }
    return curr;
}
```



#### <font style="color:#DF2A3F;">第二百七十九题</font>：[完全平方数](https://leetcode.cn/problems/perfect-squares/)
定义了一个数组，用来存储n之前每一个元素的完全平方数的最少数量，这样就得到了状态转移方程：

$ dp[i] = 1 + \min_{1 \le j^2 \le i} \{ dp[i - j^2] \} $

其中，i 是从1到 n 的所有数字，j^2是小于等于 i 的所有完全平方数 

每次当 n 减去 i 之后，都会以 i 为右边界进行一次遍历，此时就是对每一个 i 进行”局部穷举“，看看此时有哪些组成 j^2 的最少数字数量，我们会选取最小的作为当前的结果

```cpp
int numSquares(int n)
{
    std::vector<int> f(n + 1);
    for(int i = 1; i <= n; i++)
    {
        int minn = INT_MAX;
        for(int j = 1; j * j <= i; j++)
            minn = std::min(minn, f[i - j * j]);
        
        f[i] = minn + 1;
    }
    return f[n];
}
```



#### <font style="color:#DF2A3F;">第三百题</font>：[最长递增子序列](https://leetcode.cn/problems/longest-increasing-subsequence/)
<font style="background-color:#FBDE28;">解法一：动态规划</font>

状态定义：dp[ i ]指的是“以第 i 个元素结尾的子序列的最大长度”

状态转移：dp[ i ] = max( dp[ i ], dp[ j ] + 1 )，其中 j 是不大于 i 的正整数；

方程的意义是——假设正在处理 `nums[i]`，我们想把它接在一个现有的子序列后面。

为了保证“严格递增”，必须满足两个条件：

    1. **位置在前后**：那个数必须在 i 之前（即 j < i）。
    2. **数值从小到大**：那个数必须比 `nums[i]` 小（即 nums[j] < nums[i]）。

```cpp
int lengthOfLIS(vector<int>& nums)
{
    if(nums.empty()) return 0;
    std::vector<int> dp(nums.size(), 1);
    int res = 1;
    for(int i = 0; i < nums.size(); i++)
    {
        for(int j = 0; j < i; j++)
        {
            if(nums[j] < nums[i]) 
            {
                dp[i] = std::max(dp[i], dp[j] + 1);
            }
        }
        res = std::max(res, dp[i]);
    }
    return res;
}
```



#### <font style="color:#DF2A3F;">第三百二十二题</font>：[零钱兑换](https://leetcode.cn/problems/coin-change/)
确定状态：dp[ i ]代表 为了凑出 i 元，所需要的硬币数量

状态转移：dp[ i ] = min(dp[ i ], dp[ i - coin ] + 1)，即金额 i 的最优解，必然是由某个较小的金额** i - coin**转移而来的。

```cpp
int coinChange(vector<int>& coins, int amount)
{
    std::vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;

    for(int i = 1; i <= amount; i++)
    {
        for(auto coin :coins)
        {
            if(coin <= i)
                dp[i] = std::min(dp[i], dp[i - coin] + 1);
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```



#### <font style="color:#DF2A3F;">第一百五十二题</font>：[乘积最大子数组](https://leetcode.cn/problems/maximum-product-subarray/)
<font style="background-color:#FBDE28;">确定状态</font>：dp[ i ] 代表“以当前元素为结尾的最大/最小乘积是多少”

<font style="background-color:#FBDE28;">状态转移</font>：（具体公式见下图）一开始的想法是——如果当前元素乘上dp数组的上一个元素之后，所得乘积比上一个还要小，那么就以当前元素为起点向后乘；反之，将所得乘积作为以当前元素（nums[ i ]）为结尾的连续乘积存入dp数组

但是这会导致一个问题——如果原数组是 [ -2, 3, -4 ] 这种类型的话，期望结果是24（因为负负得正），但是上一个方法却会直接抛弃-2 * 3的结果，转而从 -4 开始重新计数，又因为此时已经到达了末尾，此时dp数组为 [-2, -6, -4 ] 所以最后会返回-2

上一种方法相当于只记录了最大正乘积，没有考虑到最小负乘积可能会与负数相乘，因此**还需要定义一个dp数组，用于存放最小乘积**

```cpp
int maxProduct(vector<int>& nums)
{
    if(nums.size() == 1) return nums[0];
    std::vector<int> dp_max(nums.size(), 1), dp_min(nums.size(), 1);
    dp_max[0] = dp_min[0] = nums[0];

    int res = nums[0];
    for(int i = 1; i < nums.size(); i++)
    {
        int choice1 = dp_max[i -1] * nums[i];
        int choice2 = dp_min[i -1] * nums[i];
        
        dp_max[i] = std::max({nums[i], choice1, choice2});
        dp_min[i] = std::min({nums[i], choice1, choice2});

        res = res < dp_max[i] ? dp_max[i] : res;
    }
    return res;
}
```



#### <font style="color:#DF2A3F;">第四百一十六题</font>：[分割等和子集](https://leetcode.cn/problems/partition-equal-subset-sum/)


```cpp
bool canPartition(vector<int>& nums)
{
    int sum = reduce(nums.begin(), nums.end());
    if(sum % 2 != 0) return false;
    sum /= 2;

    int n = nums.size();
    std::vector<bool> dp(sum + 1, false);
    dp[0] = true;
    for(int num : nums)
    {
        for(int i = sum; num <= i; i--)
        {
            if(dp[i - num]) dp[i] = true;
        }
        if(dp[sum]) return true;
    }
    return dp[sum];
}
```
