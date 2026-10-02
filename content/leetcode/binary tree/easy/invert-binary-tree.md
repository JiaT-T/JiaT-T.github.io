+++
slug = "invert-binary-tree"
title = "翻转二叉树"
problems = [226]
problem_id = 226
difficulty = "Easy"
weight = 226
summary = "翻转二叉树的解题思路与 C++ 实现。"
+++

题目：[翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/)


<a id="第二百二十六题翻转二叉树"></a>



以**前序遍历**为例，从根节点开始，逐步交换左右子树（先交换左子树，后交换右子树），直到所有叶子节点都交换完毕；**后序遍历**同理，先把左子树的所有节点交换完毕，再处理右子树，最后在root节点处将整个左右子树交换

而**中序遍历**是个特例，它会先交换左子树的所有节点，然后逐层返回到最顶部的root节点，将左子树和右子树交换，此时如果按照之前的逻辑，继续对右子树进行交换的话，相当于是对一开始的左子树又进行了一次交换，所有此时需要改变一下代码，进行对左子树）也就是一开始的右子树）进行交换，这样才能得到正确的结果

```cpp
// 前序
TreeNode* invertTree(TreeNode* root)
{
    if(root == nullptr) return nullptr;
    std::swap(root->left, root->right);
    invertTree(root->left);
    invertTree(root->right);

    return root;
}

// 中序
TreeNode* invertTree(TreeNode* root)
{
    if(root == nullptr) return nullptr;
    invertTree(root->left);
    std::swap(root->left, root->right);
    invertTree(root->left);

    return root;
}

// 后序
TreeNode* invertTree(TreeNode* root)
{
    if(root == nullptr) return nullptr;
    invertTree(root->left);
    invertTree(root->right);
    std::swap(root->left, root->right);

    return root;
}
```
