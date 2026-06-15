+++
title = "1"
problems = [1]
+++

#### <font style="color:#DF2A3F;">第一题</font>：[两数之和](https://leetcode.cn/problems/two-sum/)
最容易想到的方法就是两层for循环，时间复杂度为O(n^2)

但是可以利用哈希表O(1)的查找时间复杂度将其降至 O(n)

具体实现：

在循环中对”表内是否存在等于‘目标值减去当前值’的数进行判断“（因为需要进行配对），如果没有，就将当前的元素加入到哈希表，否则直接输出

注：这里的判断条件——it != um.end()  的意思是找到了匹配的数字，因为**如果哈希表没有找到对应的key时，会返回尾地址**

```cpp
vector<int> twoSum(vector<int>& nums, int target) 
{
    std::unordered_map<int,int> um;
    for(int i = 0; i < nums.size(); i++)
    {
        auto it = um.find(target - nums[i]);
        if(it != um.end()) return {it->second, i};
        um[nums[i]] = i;
    }
    return {};
}
```
