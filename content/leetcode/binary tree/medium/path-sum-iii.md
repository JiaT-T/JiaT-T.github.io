+++
slug = "path-sum-iii"
title = "路径总和 III"
problems = [437]
problem_id = 437
difficulty = "Medium"
weight = 437
summary = "路径总和 III的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/gvwgx0lykh5yempx"
+++

题目：[路径总和 III](https://leetcode.cn/problems/path-sum-iii/)


<a id="第四百三十七题路径总和-iii"></a>



使用到了<font style="background-color:#FBDE28;">深搜和层序遍历</font>

注：此处并非最优解，但是我不想再看其他解法了....

更好的答案参见这里吧[437. 路径总和 III - 力扣（LeetCode）](https://leetcode.cn/problems/path-sum-iii/solutions/2784856/zuo-fa-he-560-ti-shi-yi-yang-de-pythonja-fmzo/?envType=study-plan-v2&envId=top-100-liked)

**思路：**

简单来说，就是通过层序遍历，从每一个节点出发，进行一次深度优先搜索，并在搜索过程中不断地将当前总和与目标和进行比较，若相等则将路径数量加一

**具体实现：**

dfs函数：从传入的节点出发，先将当前值加到当前总和上去，然后与目标值进行比较；接着递归深入左子树和右子树（需要传入当前总和），之后左右子树又会进行相同的判断

pathSum函数：定义队列，按照层序遍历的顺序每次访问一个节点，并调用dfs函数

```cpp
int pathSum(TreeNode* root, int targetSum)
{
    if(!root) return 0;
    std::queue<TreeNode*> q;
    q.push(root);
    int total = 0;
    while(!q.empty())
    {
        TreeNode* curr = q.front();
        q.pop();
        total += dfs(curr, 0, targetSum);

        if(curr)
        {
            q.push(curr->left);
            q.push(curr->right);
        }
    }
    return total;
}
int dfs(TreeNode* curr, long long curr_sum, int targetSum)
{
    if(!curr) return 0;
    curr_sum += curr->val;
    int count = 0;
    if(curr_sum == targetSum) count++;

    count += dfs(curr->left, curr_sum, targetSum);
    count += dfs(curr->right, curr_sum, targetSum);

    return count;
}
```

<a id="Lm8yG"></a>

<strong>补充解法：前缀和与哈希表</strong>

<a id="u76e63105"></a><a id="YJ1Rh"></a>[https://leetcode.cn/problems/path-sum-iii/solutions/2784856/zuo-fa-he-560-ti-shi-yi-yang-de-pythonja-fmzo/?envType=study-plan-v2&amp;envId=top-100-liked](<https://leetcode.cn/problems/path-sum-iii/solutions/2784856/zuo-fa-he-560-ti-shi-yi-yang-de-pythonja-fmzo/?envType=study-plan-v2&envId=top-100-liked>)

<a id="ub7be5587"></a>核心公式：

<a id="u5f5ae32d"></a><strong>当前前缀和 - 历史前缀和 = targetSum</strong>

<a id="u6c8e0705"></a>移项可得：

<a id="u1032b524"></a><strong>历史前缀和 = 当前前缀和 - targetSum</strong>

<a id="u3d989efd"></a>因此，只需要使用一个哈希表记录“从根节点到当前节点的路径上，以每个节点为终点的前缀和的出现次数”，然后通过判断当前前缀和减去targetSum的值是否存在于哈希表中：如果存在，就说明对应的历史前缀和的终点节点到当前节点的和就是 targetSum

<a id="WUY8z"></a>
pathSum（）

```cpp
int pathSum(TreeNode* root, int targetSum)
{
    std::unordered_map<long long, int> count = {{0, 1}};
    int res = 0;

    auto dfs = [&](this auto&& dfs, TreeNode* root, long long s)
    {
        if(root == nullptr) return;

        s += root->val;
        res += count[s - targetSum];

        count[s]++;
        dfs(root->left, s);
        dfs(root->right, s);
        count[s]--;
    };

    dfs(root, 0);
    return res;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/gvwgx0lykh5yempx)
