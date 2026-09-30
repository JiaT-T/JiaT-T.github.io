+++
title = "39、46、78、79、131"
problems = [39, 46, 78, 79, 131, 17, 22]
+++

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




<a id="bk8XA"></a>

<strong>补充解法：used 数组回溯</strong>

```cpp
class Solution
{
public:
    std::vector<vector<int>> res;
    std::vector<int> path;
    void backTrack(vector<int>& nums, vector<bool> used)
    {
        // 终止条件
        if(path.size() == nums.size())
        {
            res.push_back(path);
            return;
        }
        
        for(int i = 0; i < nums.size(); i++)
        {
            // 如果当前元素已经被使用过了
            // 就直接跳过它
            if(used[i])
                continue;

            // 将当前元素标记为“已使用”
            used[i] = true;
            path.push_back(nums[i]);
            // 对下一个元素进行操作
            backTrack(nums, used);
            // 撤销所有操作
            path.pop_back();
            used[i] = false;
        }
    }

    vector<vector<int>> permute(vector<int>& nums)
    {
        // 用来标记已使用的元素
        std::vector<bool> used(nums.size(), false);
        backTrack(nums, used);
        return res;
    }
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/tvmshwlzcw3s2ta1)

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



#### <font style="color:#DF2A3F;">第一百三十一题</font>：[分割回文串](https://leetcode.cn/problems/palindrome-partitioning/)
思路：对于每一个字符，都先判断其是否能够被分割，即以start为首，以当前字符为尾的字符串是否为回文串；如果能够分割（**第一条路径**），就将当前元素压入path，组成子回文串，并从下一个字符开始进行新一轮的回文串判断；**第二条路径**为：不从当前字符进行分割，而是直接转向下一个字符，从下一个字符开始判断（为了找到更长的回文串）

```cpp
bool isPalindrome(const string& s, int left, int right)
{
    while(left < right)
    {
        if(s[left++] != s[right--])
            return false;
    }
    return true;
}
void dfs(string& s, int index, int start, vector<string>& path, vector<vector<string>>& res)
{
    const int sz = s.size();
    if(index == sz) 
    {
        res.emplace_back(path);
        return;
    }

    if(isPalindrome(s, start, index))
    {
        path.emplace_back(s.substr(start, index - start + 1));
        dfs(s, index + 1, index + 1, path, res);
        path.pop_back();
    }

    if(index < sz - 1)
        dfs(s, index + 1, start, path, res);
}

vector<vector<string>> partition(string s)
{
    vector<string> path;
    vector<vector<string>> res;

    dfs(s, 0, 0, path, res);
    return res;
}
```

<a id="ADPJG"></a>
#### 第十七题：[电话号码的字母组合](<https://leetcode.cn/problems/letter-combinations-of-a-phone-number/>)

<a id="u9a74a1cf"></a>使用到的知识点是 哈希表 和 回溯算法

<a id="u58e87fe6"></a>因为未知输入字符串的长度，所以不能手动的定义for循环去暴力求解

<a id="u7847db98"></a>联想到树的结构，从一个分支一直走到底，再返回上一个最近的分支；与此题类似，以前一个字符串为基点，向后遍历每一个出现的字符，组成新的字符串。

<a id="u224db552"></a>难点在于如何回溯：这里使用到的是递归函数

<a id="u1f04fbb9"></a>根据传入的index确定当前数字，然后再根据数字在map中得到对应的字符，以每一个字符为起点，进行函数的递归调用，直到index与输入字符串长度相同

<a id="wMmcg"></a>
letterCombinations（）
```cpp
class Solution 
{
public:
    void backTrack(const string& digits, int index, std::unordered_map<char, string>& phoneMap, string& combination, std::vector<string>& combinations)
    {
        if(index == digits.size()) 
            combinations.push_back(combination);
        else
        {
            char num = digits[index];
            const string& letters = phoneMap[num];
            for(const char& letter : letters)
            {
                combination.push_back(letter);
                backTrack(digits, index + 1, phoneMap, combination, combinations);
                combination.pop_back();
            }
        }
    }

    vector<string> letterCombinations(string digits) 
    {
        if(digits.empty()) return {};
        std::unordered_map<char, string> phoneMap
        {
            {'2', "abc"},
            {'3', "def"},
            {'4', "ghi"},
            {'5', "jkl"},
            {'6', "mno"},
            {'7', "pqrs"},
            {'8', "tuv"},
            {'9', "wxyz"}
        };
        std::vector<string> combinations;
        string combination;
        backTrack(digits, 0, phoneMap, combination, combinations);
        return combinations;
    }
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/tvmshwlzcw3s2ta1)

<a id="vfqUX"></a>
#### 第二十二题：[括号生成](<https://leetcode.cn/problems/generate-parentheses/>)

<a id="u1846bb00"></a>使用到的是回溯算法

<a id="u211e00ae"></a>对于输入的数字n，可以知道的是最终的元素为2n个括号，其中左括号和右括号都为n个

<a id="u0219feb5"></a>先经过一次分析得到规律：以n=2为例，每个元素分别有2个左右括号，第一个空必须是' （ ’，此时left的数量加一；而第二个空则有两种可能，当为‘（’时，left的数量已经达到了2，那么之后两个空就只能是‘）’；当为‘）’时，此时left = right，第三个空就只能是‘（’，从而得出第四个空是‘）’

<a id="u513cf301"></a>总结规律，可以得出：

<a id="u4a7149fc"></a>1.当<strong>left &lt; n时，应该添加‘（’</strong>

<a id="u20fd6ddb"></a>2.当<strong>right &lt; left时，应当有‘）’与其配对，故添加‘）’</strong>

<a id="u7a39a59e"></a>在此条件下进行递归，最后当left+right与n相同时终止最后一层递归，返回上一层的枝，继续下一个子节点的递归

<a id="O2k9P"></a>
generateParenthesis()
```cpp
class Solution
{
public:
    vector<string> generateParenthesis(int n)
    {
        std::vector<string> combinations;
        string combination;
        backTrace(0, 0, combination, combinations, n);
        return combinations;
    }

private :
    void backTrace(int left, int right, string& combination, std::vector<string>& combinations, int n)
    {
        if(left + right == 2 * n) 
        {
            combinations.push_back(combination);
            return;
        }
        else
        {
            if(left < n) 
            {
                combination.push_back('(');
                backTrace(left + 1, right, combination, combinations, n);
                combination.pop_back();
            }
            if(right < left)
            {
                combination.push_back(')');
                backTrace(left, right + 1, combination, combinations, n);
                combination.pop_back();
            }
        }
    }
};
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/tvmshwlzcw3s2ta1)

