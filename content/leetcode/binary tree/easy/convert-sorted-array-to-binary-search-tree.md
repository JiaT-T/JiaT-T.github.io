+++
slug = "convert-sorted-array-to-binary-search-tree"
title = "将有序数组转换为二叉搜索树"
problems = [108]
problem_id = 108
difficulty = "Easy"
weight = 108
summary = "将有序数组转换为二叉搜索树的解题思路与 C++ 实现。"
+++

题目：[将有序数组转换为二叉搜索树](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/)


<a id="第一百零八题将有序数组转换为二叉搜索树"></a>



先回顾一下二叉搜索树的定义：<u>左子树的任一节点都小于根节点，右子树的任一节点都大于根节点</u>

现在拿到了一个有序数组，自然可以想到要从中间开始进行遍历，因此首先找到数组的中间节点，并以它作为根节点向左右进行遍历，因为数组已经有序，所以不需要再进行比较，只需要明确每一次构造的左右边界即可

至于为什么不需要考虑奇偶数组的情况，这是因为int的除法会自动向下取整，所以即使是偶数数组，也能够保证平衡（但不是对称）

```cpp
TreeNode* traversal(vector<int>& nums, int left, int right)
{
    if(left > right) return nullptr;
    int mid = (left + right) / 2;
    TreeNode* root = new TreeNode(nums[mid]);
    root->left = traversal(nums, left, mid - 1);
    root->right = traversal(nums, mid + 1, right);
    return root;
}

TreeNode* sortedArrayToBST(vector<int>& nums)
{
    return traversal(nums, 0, nums.size() - 1);
}
```
