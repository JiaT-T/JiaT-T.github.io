+++
slug = "lowest-common-ancestor-of-a-binary-tree"
title = "二叉树的最近公共祖先"
problems = [236]
problem_id = 236
difficulty = "Medium"
weight = 236
summary = "二叉树的最近公共祖先的解题思路与 C++ 实现。"
+++

题目：[二叉树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/)


<a id="第二百三十六题"></a>



**思路：**

因为需要从下往上进行遍历，所以采用的是后序遍历（左右中），这样就可以让中间节点拿到左右子树的信息，从而**判断自身是否为公共祖先**——如果子树没有搜索到目标节点，会返回空指针；只有<u>当左右子树的返回值都不为空时，才可以判断当前节点为公共祖先</u>

**具体实现：**

首先定义递归结束的条件——当前节点为空，或当前节点就是需要进行查找的节点

之后就开始对左右子树进行递归遍历，当目标节点存在于左右子树中时，就直接返回当前节点（理由如上）；当只有左子树找到目标节点而右子树没有搜索到时，就返回左节点（因为此时两个目标值都位于左子树中）；只有右子树搜索到时同理

```cpp
TreeNode* traversal(TreeNode* root, TreeNode* p, TreeNode* q)
{
    if(!root) return nullptr;
    if(root == p || root == q) return root;

    TreeNode* left = traversal(root->left, p, q);
    TreeNode* right = traversal(root->right, p, q);

    if(left && right) return root;
    else if(left && !right) return left;
    else if(!left && right) return right;
    else return nullptr;
}

TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q)
{
    return traversal(root, p, q);
}
```
