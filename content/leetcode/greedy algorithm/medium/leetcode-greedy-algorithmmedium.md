#### <font style="color:#DF2A3F;">第四十五题</font>：[跳跃游戏 II](https://leetcode.cn/problems/jump-game-ii/)
这里直接引用一下别人的讲解：

//把该问题比喻为入职，数组下标是公司级别(入职门槛)，对应的值是公司级别之上的级别成长空间。你想用最少的跳槽次数入职最高级的公司

//数组[2,3,1,2,4,2,3]

//下标 0 1 2 3 4 5 6

//最开始你没有工作，你的水平是2级，可以在2级及以下的公司里随便挑，此时候选公司有下标1和2

//注意：如果你想进入更高级别的公司，应该选择能够帮助你提升级别最多的公司。例如，公司1能够将你的级别提升到1+3=4级，而公司2只能提升到2+1=3级。显然，你应该选择公司1，然后升到4级。接下来，你可以跳槽到4级及以下的公司，每次都选择能够帮助你提升最多级别的公司，如此循环……直到水平级别足够入职梦中情司

//只有每次跳槽都选择能够帮助你升级最多的公司，才能以最少的跳槽次数到达最高级别的公司

```cpp
int jump(vector<int>& nums)
{
    int res = 0;
    int curr = 0, max_pos = 0;

    for(int i = 0; i < nums.size() - 1; i++)
    {
        max_pos = std::max(max_pos, i + nums[i]);
        if(i == curr)
        {
            curr = max_pos;
            res++;
        }
    }
    return res;
}
```

#### <font style="color:#DF2A3F;">第五十五题</font>：[跳跃游戏](https://leetcode.cn/problems/jump-game/)
思路：

从第一个元素开始进行遍历，并记录截止当前元素可以到达的最大位置（far）

如果当前位置的下标（i）比最远位置还要大，就说明 i 是无法到达的，也就更不可能到达终点

而如果 i 在 far 的范围之内，就说明 i 是可以到达的，此时就需要根据 i 对应的值来更新 far 的位置

当整个数组都被遍历完成，就说明最后一个元素是位于 far 之内的，也就代表着终点可以到达

```cpp
bool canJump(vector<int>& nums)
{
    int far = 0;
    for(int i = 0; i < nums.size(); i++)
    {
        if(far < i) return false;
        else
            far = std::max(far, i + nums[i]);
    }
    return true;
}
```



#### <font style="color:#DF2A3F;">第七百六十三题</font>：[划分字母区间](https://leetcode.cn/problems/partition-labels/)
<font style="background-color:#FBDE28;">思路：</font>

记录每个字母最后出现的位置，从第一个元素开始不断进行划分，（除第一次外）每一次的起始位置都是上一次结束位置的下一个位置

之所以这么做，是因为每个相同的字母都必须出现在同一区间，也就是说划分出来的子区间至少要包含这个字母第一次出现到最后一次出现的区间；同时区间也可能出现覆盖的情况（比如 a 的区间是 [0, 8]，而 b 的区间是 [1, 7]，那么此时就要以 a 的区间为最终划分的依据，这也就是为什么记录每个元素最后一次出现的位置的原因

<font style="background-color:#FBDE28;">具体实现：</font>

首先使用一个数组得到每个字母各自的区间末端（注意不要使用哈希表或者map，这两个数据结构对链式结构很不友好，实测array的时间复杂度超过100%， map超过54%，unordered_map超过11%）

之后再通过一个循环，不断对end进行更新，直到下标走到end的位置，此时也就意味着第一个区间被划分出来了，那么就更新start，从当前end的下一个下标开始新一个区间的划分

```cpp
vector<int> partitionLabels(string s)
{
    std::array<int, 26> lastPos;
    for(int i = 0; i < s.size(); i++)
    {
        lastPos[s[i] - 'a'] = i;
    }

    std::vector<int> res;
    int start = 0, end = 0;
    for(int i = 0; i < s.size(); i++)
    {
        end = std::max(end, lastPos[s[i] - 'a']);
        if(i == end)
        {
            res.push_back(end - start + 1);
            start = end + 1;
        }
    }
    return res;
}
```
