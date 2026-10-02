+++
slug = "diameter-of-binary-tree"
title = "二叉树的直径"
problems = [543]
problem_id = 543
difficulty = "Easy"
weight = 543
summary = "二叉树的直径的解题思路与 C++ 实现。"
+++

题目：[二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/)


<a id="第五百四十三题二叉树的直径"></a>



最开始的想法是：分别求左右子树的最大深度，之后再加上二就是二叉树的直径

但是这个方法仅仅只是”局部最优解“而非”全局最优解“，因为二叉树的直径也可能不会跨越根节点（比如当左子树为深度非常大的满二叉树，而右子树仅仅只有一个节点时，那么直径就会在左子树出现），因此需要判断直径的计算是否会跨越根节点

```cpp
int maxDepth(TreeNode* curr, int& max_dep)
{
    if(!curr) return 0;

    int left_dep = maxDepth(curr->left, max_dep);
    int right_dep = maxDepth(curr->right, max_dep);
    max_dep = std::max(max_dep, left_dep + right_dep);
    return std::max(left_dep, right_dep) + 1;
}

int diameterOfBinaryTree(TreeNode* root)
{
    int max_dep = 0;
    maxDepth(root, max_dep);
    return max_dep;
}
```
