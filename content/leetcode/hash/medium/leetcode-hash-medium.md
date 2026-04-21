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
