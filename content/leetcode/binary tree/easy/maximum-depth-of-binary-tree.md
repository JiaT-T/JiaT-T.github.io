+++
slug = "maximum-depth-of-binary-tree"
title = "二叉树的最大深度"
problems = [104]
problem_id = 104
difficulty = "Easy"
weight = 104
summary = "二叉树的最大深度的解题思路与 C++ 实现。"
+++

题目：[二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)


<a id="第一百零四题二叉树的最大深度"></a>



求深度：用前序遍历；求高度：用后序遍历

而二叉树的最大深度，恰好就是root节点的高度，因此求root的高度即可

至于为什么不直接用后序遍历求深度，是因为代码量相对于求高度的方法更多



先沿着左右子树进行遍历，得到左右子树各自的最大深度，取最大值加1即可得到当前中间节点的深度

以此类推，可以逐步累加得到根节点（最上方的中间节点）的高度

```cpp
int maxDepth(TreeNode* root)
{
    if(root == NULL) return 0;
    int leftDepth = maxDepth(root->left);
    int rightDepth = maxDepth(root->right);
    int depth = 1 + std::max(leftDepth, rightDepth);
    return depth;
}

// 精简版
int maxDepth(TreeNode* root)
{
    if(root == NULL) return 0;
    return 1 + std::max(maxDepth(root->left), maxDepth(root->right));
}
```
