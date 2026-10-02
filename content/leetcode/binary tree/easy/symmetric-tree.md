+++
slug = "symmetric-tree"
title = "对称二叉树"
problems = [101]
problem_id = 101
difficulty = "Easy"
weight = 101
summary = "对称二叉树的解题思路与 C++ 实现。"
+++

题目：[对称二叉树](https://leetcode.cn/problems/symmetric-tree/)


<a id="第一百零一题对称二叉树"></a>



要判断一个二叉树是否对称，就是判断这个树<font style="background-color:#FBDE28;">根节点的左右子树是否能够翻转</font>，而判断能否翻转，则需要判断这棵二叉树的内外侧节点是否相同

因为需要拿到左右子树各自的信息，所以使用后序遍历

首先对特殊情况进行判断：

1.传入的左节点不为空，右节点为空，那么无法翻转

2.左空右不空同理

3.两边都为空时，可以翻转

4.两遍都不为空，但是值不同，不能翻转

5.只有当两者都不为空且值相等时，才进入递归逻辑，判断左子树的左节点与右子树的右节点能否翻转（外侧），以及左子树的右节点与右子树的左节点能否翻转（内侧）

最后，只有当左右节点都能反转时，才可以认为这棵树 / 子树能翻转

```cpp
bool Compare(TreeNode* left, TreeNode* right)
    {
        if(!left && right) return false;
        else if(left && !right) return false;
        else if(!left && !right) return true;
        else if(left->val != right->val) return false;
        else
        {
            bool outside = Compare(left->left, right->right);
            bool inside = Compare(left->right, right->left);
            return outside && inside;
        }
    }
    bool isSymmetric(TreeNode* root)
    {
        return Compare(root->left, root->right);
    }
```
