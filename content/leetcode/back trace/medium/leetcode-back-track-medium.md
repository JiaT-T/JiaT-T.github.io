#### <font style="color:#DF2A3F;">第三十九题</font>：[组合总和](https://leetcode.cn/problems/combination-sum/)
核心思路：**每次添加元素之后都将target减少对应的值，直到等于或小于零**

具体实现：

在回溯函数中首先判断target是否已经等于零——代表着当前元素的组合已经满足要求，可以压入res数组中

否则继续进行遍历与递归，直到出现满足总和要求的数组为止

在循环中要注意的是，当总和已经超出target时，就不要在把当前元素存入temp中了，而是直接跳过他，从下一个元素继续进行

```cpp
void backTrack(vector<int>& candidates, int target, int index, vector<int>& temp, vector<vector<int>>& res)
{
    if(target == 0)
    {
        res.push_back(temp);
        return;
    }

    for(int i = index; i < candidates.size(); i++)
    {
        if(target - candidates[i] < 0) continue;
        temp.push_back(candidates[i]);
        backTrack(candidates, target - candidates[i], i, temp, res);
        temp.pop_back();
    }
}
vector<vector<int>> combinationSum(vector<int>& candidates, int target)
{
    vector<vector<int>> res;
    vector<int> temp;
    res.reserve(150);
    backTrack(candidates, target, 0, temp, res);
    return res;
}
```



#### <font style="color:#DF2A3F;">第四十六题</font>：[全排列](https://leetcode.cn/problems/permutations/)
核心在于“**交换**”的步骤

首先从第一个元素开始，既然首元素已经确定了，之后就是递归地对后面的元素进行全排列

本质上就是让所有元素都当一次第一个元素，再让此时的第一个元素之后的所有元素当一次第二个元素.....以此类推，从前往后每个位置分别有n、n-1、n-2个种选择，也就是n！种排列方式

```cpp
vector<vector<int>> permute(vector<int>& nums)
{
    vector<vector<int>> res;
    res.reserve(factorial(nums.size()));

    backTrack(nums, res, 0);
    return res;
}

void backTrack(vector<int>& nums, vector<vector<int>>& res, int first)
{
    if(first == nums.size())
        res.push_back(nums);

    for(int i = first; i < nums.size(); i++)
    {
        std::swap(nums[first], nums[i]);
        backTrack(nums, res, first + 1);
        std::swap(nums[first], nums[i]);
    }   
}

size_t factorial(size_t sz)
{
    size_t res;
    for(int i = 0; i < sz; i++) res *= i;
    return res;
}
```



#### <font style="color:#DF2A3F;">第七十八题</font>：[子集](https://leetcode.cn/problems/subsets/)
核心思路：<font style="background-color:#FBDE28;">枚举每一个位置，并通过递归调用进入下一个位置</font>

具体实现：

每次进入回溯函数时，都先将当前保存的数组存入结果数组中，之后再进入具体的回溯算法——通过循环遍历当前元素之后的每一个元素，然后再递归调用相同函数，对下一个元素进行相同操作

```cpp
void backTrack(vector<int>& nums, vector<vector<int>>& res, vector<int>& temp, int start)
{
    res.emplace_back(temp);
    for(int i = start; i < nums.size(); i++)
    {
        temp.push_back(nums[i]);
        backTrack(nums, res, temp, i + 1);
        temp.pop_back();
    }
}
vector<vector<int>> subsets(vector<int>& nums)
{
    vector<vector<int>> res;
    vector<int> temp;
    res.reserve(1 << nums.size());
    backTrack(nums, res, temp, 0);
    return res;
}
```



#### <font style="color:#DF2A3F;">第七十九题</font>：[单词搜索](https://leetcode.cn/problems/word-search/)
使用到了<font style="background-color:#FBDE28;">深搜</font>

具体实现：

首先<u>在双层循环中判断首元素是什么，之后以这个元素为起点进行深搜</u>

dfs函数核心的判断逻辑是“found”变量那里——**只有出现一条连续的、与word匹配的元素串，found才能为真**

要注意的是，因为同一元素不能重复使用，所以在进行深搜的时候要**提前将当前元素标记为“已使用”**，这里采用的是‘\0’（不属于任何字母）

```cpp
bool dfs(vector<vector<char>>& board, string word, int index, int r, int c)
{   
    if(index == word.size()) return true;
    if(r < 0 || r >= board.size() || c < 0 || c >= board[0].size() || word[index] != board[r][c]) return false;

    char temp = board[r][c];
    board[r][c] = '\0';

    bool found = dfs(board, word, index + 1, r + 1, c    ) || 
                 dfs(board, word, index + 1, r,     c + 1) ||
                 dfs(board, word, index + 1, r - 1, c    ) ||
                 dfs(board, word, index + 1, r,     c - 1);

    board[r][c] = temp;

    return found;
}
bool exist(vector<vector<char>>& board, string word)
{
    for(int j = 0; j < board[0].size(); j++)
    {
        for(int i = 0; i < board.size(); i++)
        {
            if(dfs(board, word, 0, i, j)) return true;
        }
    }
    return false;
}
```
