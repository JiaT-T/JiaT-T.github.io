#### <font style="color:#DF2A3F;">第一百三十六题</font>：[只出现一次的数字](https://leetcode.cn/problems/single-number/)
题目要求的是线性时间复杂度以及常量额外空间，所以像哈希表之类的解法都不能使用

这里使用到的是**<font style="background-color:#FBDE28;">异或（XOR）</font>**，它的性质是：

1.任何数与0异或得到这个数本身

2.任何数与自身异或得到0

3.异或运算满足结合律，即_**a**_**⊕**_**b**_**⊕**_**a**_**=**_**b**_**⊕**_**a**_**⊕**_**a**_**=**_**b**_**⊕(**_**a**_**⊕**_**a**_**)=**_**b**_**⊕0=**_**b**_

通过以上性质，只需要将数组内的所有元素放在同一个异或运算式中，就可以将所有相同的数字进行组合（结果为零），又因为性质一，所以最后得到的结果一定就是落单的数字

```cpp
int singleNumber(vector<int>& nums)
{
    int res = 0;
    for(auto num : nums) res ^= num;
    return res;
}
```



#### <font style="color:#DF2A3F;">第一百六十九题</font>：[多数元素](https://leetcode.cn/problems/majority-element/)
<font style="background-color:#FBDE28;">解法一（哈希表）：</font>

第一次遍历将数组中的元素存入哈希表，nums自身的数值作为键，出现次数作为值

之后再通过一次遍历找出表中值大于n/2对应的键，作为 _多数元素 _返回

```cpp
int majorityElement(vector<int>& nums)
    {
        int sz = nums.size();
        int res;
        std::unordered_map<int, int> um;
        for(int i = 0; i < sz; i++)
        {
            if(um.find(nums[i]) == um.end()) 
                um[nums[i]] = 1;
            else
                um[nums[i]]++;
        }
        for(auto num : nums)
        {
            if(um[num] > static_cast<float>(sz / 2))
                res = num;
        }
        return res;
    }
```



<font style="background-color:#FBDE28;">解法二：</font>

这里借用一下灵神的比喻：[169. 多数元素 - 力扣（LeetCode）](https://leetcode.cn/problems/majority-element/solutions/3744717/on-mo-er-tou-piao-fa-yan-jin-zheng-ming-ww1zv/?envType=study-plan-v2&envId=top-100-liked)

_用「擂台赛」打比方：_

_想象一众武林高手比武，谁会笑到最后？_

_擂主登场：nums[0] 成为初始擂主，生命值为 1。_

_挑战者出现：遍历后续元素，作为挑战者。_

_比武：如果挑战者与擂主属于同一门派（值相同），那么擂主生命值加 1，否则擂主生命值减 1。_

_擂主更迭：如果比武后，擂主生命值降为 0（同归于尽），那么下一个挑战者成为新的擂主，生命值为 1。_

_最后在擂台上的那人，便是武林盟主（绝对众数）。_

```cpp
int majorityElement(vector<int>& nums)
{
    int res = 0, hp = 0;
    for(int x : nums)
    {
        if(hp == 0)
        {
            res = x;
            hp = 1;
        }
        else
            hp += res == x ? 1 : -1;
    }
    return res;
}
```
