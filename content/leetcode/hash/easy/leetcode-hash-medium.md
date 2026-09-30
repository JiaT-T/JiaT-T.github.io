+++
title = "1"
problems = [1, 409]
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

<a id="IWZSs"></a>
#### 第四百零九题：[最长回文串](<https://leetcode.cn/problems/longest-palindrome/>)

<a id="ua2c36845"></a>思路：对于出现次数为偶数个的字符，可以直接将其添加至回文字符串两端；对于出现次数为奇数个的字符，最多取其中的 （ct - 1）个添加至两端，最后还可以从奇数字符中拿出一个放在最中间

<a id="C8IR9"></a>
longestPalindrome（）
```cpp
int longestPalindrome(string s)
{
    if(s.size() <= 1) return s.size();

    // 统计字符出现次数
    std::unordered_map<char, int> um;
    for(char c : s)
    {
        um[c]++;
    }

    int length = 0;
    bool has_odd = false;
    for(const auto& [ch, cnt] : um)
    {
        // 利用 int 的向下取整性质
        // 可以将奇偶的情况统一处理
        length += (cnt / 2) * 2;
        // 判断是否存在奇数出现次数
        if(cnt % 2 == 1)
        {
            has_odd = true;
        }
    }
    // 如果 s 中含有奇数出现次数的字符
    // 就在中间再加上这个字符（长度加一）
    return length + (has_odd ? 1 : 0);
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/iyctdall69ru0wes)

