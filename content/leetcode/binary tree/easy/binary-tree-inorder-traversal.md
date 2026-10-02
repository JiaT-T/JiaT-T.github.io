+++
slug = "binary-tree-inorder-traversal"
title = "二叉树的中序遍历"
problems = [94]
problem_id = 94
difficulty = "Easy"
weight = 94
summary = "二叉树的中序遍历的解题思路与 C++ 实现。"
+++

题目：[二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/)


<a id="第九十四题二叉树的中序遍历"></a>



非常基础的一个遍历，感觉没什么好说的....

首先确定递归函数的参数和返回值：void--因为这里直接传入了一个vector的引用

然后明确递归终止的条件：<font style="background-color:#FBDE28;">当前节点为空</font>

这也就意味着当前分支上的所有节点都已经遍历完了，所以应该进入下一个分支

比如中序遍历，顺序是“左中右”，所以inorder函数中就是先递归左分支，再将中间节点压入vector，最后遍历右分支

其他两个遍历以此类推

```cpp
void inorder(TreeNode* root, std::vector<int>& traversal)
{
    if(root == NULL) return;
    inorder(root->left, traversal);
    traversal.push_back(root->val);
    inorder(root->right, traversal);
}

vector<int> inorderTraversal(TreeNode* root)
{
    std::vector<int> traversal;

    inorder(root, traversal);
    return traversal;
}
```
