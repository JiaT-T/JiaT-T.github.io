+++
title = "49、128"
problems = [49, 128, 12, 13]
+++

#### <font style="color:#DF2A3F;">第四十九题</font>：[字母异位词分组](https://leetcode.cn/problems/group-anagrams/)
实现思路：记录每个字符串中单个字母的出现频率，并以字符串形式存储起来（如”0110200000....")，可以提前将字符串的空间预留26位（对应26个字母），然后将这个字符串作为哈希表的key，用来查找表中存储着异位词的vector值

```cpp
vector<vector<string>> groupAnagrams(vector<string>& strs)
{
    std::vector<vector<string>> res;
    std::unordered_map<string, std::vector<string>> um_pair;
    for(auto& str : strs)
    {
        string count(26, 0);
        for(auto& c : str)
        {
            count[c - 'a'] += 1;
        }
        um_pair[count].push_back(str);
    }
    for(auto& pair : um_pair)
    {
        res.push_back(pair.second);
    }
    return res;
}
```

#### <font style="color:#DF2A3F;">第一百二十八题</font>：[最长连续序列](https://leetcode.cn/problems/longest-consecutive-sequence/)
使用到了unordered_set，它只存储key，逻辑意义是“这个元素是否存在于集合中？”

具体思路：对于一个元素，首先判断他的上一个元素（当前值减去1）是否在集合中，

    - 如果在，就意味着当前元素不是起始位置，不需要管他，直接进行下一次循环；
    - 如果不在，代表着当前元素是起始位置，然后从他开始向后遍历，直到下一个元素不存在于集合中，此时得到的长度即为连续序列的长度

每一层循环都对res进行一次比较，如果当前长度更大，就替换之前的res

```cpp
int longestConsecutive(vector<int>& nums)
{
    int res = 0;
    std::unordered_set<int> seqs(nums.begin(), nums.end());
    for(auto num : seqs)
    {
        int temp = 1;
        if(seqs.contains(num - 1))
            continue;
        while(seqs.contains(num + 1))
        {
            temp++;
            num++;
        }
        res = std::max(temp, res);
    }
    return res;
}
```

<a id="QLYAs"></a>
#### 第十二题：[整数转罗马数字](<https://leetcode.cn/problems/integer-to-roman/>)

<a id="u3bee1bf5"></a>使用到的是类似哈希表的结构

<a id="ud635a40f"></a>当当前数字大于此时values中存储的值时，认为其满足“如果该值不是以 4 或 9 开头，请选择可以从输入中减去的最大值的符号，将该符号附加到结果，减去其值，然后将其余部分转换为罗马数字”的条件，需要找到此时value对应的key，拼接到res的末尾

<a id="u3597ff96"></a><strong>注意：</strong>在这里，我们将4，9，10等特殊值直接存储到哈希表结构中，因为可以原算法就是通过顺序遍历的方法进行对应值的筛选

<a id="lcPbj"></a>
intToRoman（）
```cpp
string intToRoman(int num)
    {
        std::array<int, 13> values = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
        std::array<std::string, 13> keys = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
        std::string res = "";
        for(int i = 0; i < 13; i++)
        {
            while(values[i] <= num)
            {
                num -= values[i];
                res += keys[i];
            }
        }
        return res;
    }
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/di3nplg5fg7crhpz)

<a id="AWZDC"></a>
#### 第十三题：[罗马数字转整数](<https://leetcode.cn/problems/roman-to-integer/>)

<a id="u739bd817"></a>同样使用到了哈希表

<a id="u33a92af3"></a>不同的是，这次并没有将4，9等特殊数字存储进来，而是选择在后面的分支中进行处理：如果下一个字符代表的数字大于当前字符，那么就减去当前字符代表的数字（如：此次读取到了I，而下一个字符为V，也就是说这两个字符本来是连在一起的（IV：4），这是就需要减去1，而5会在下一次循环中加上去）

<a id="lbAYc"></a>
romanToInt（）
```cpp
class Solution 
{
public:
    unordered_map<char, int> symbolValues = 
    {
        {'I', 1},
        {'V', 5},
        {'X', 10},
        {'L', 50},
        {'C', 100},
        {'D', 500},
        {'M', 1000},
    };

    int romanToInt(string s) 
    {
        int res = 0;
        int n = s.size();
        for(int i = 0; i < n; i++)
        {
            int currValue = symbolValues[s[i]];
            if (i < n - 1 && currValue < symbolValues[s[i + 1]]) 
                res -= currValue;
            else 
                res += currValue;
        }
        return res;
    }
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/di3nplg5fg7crhpz)

