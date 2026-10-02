+++
slug = "kth-smallest-element-in-a-bst"
title = "二叉搜索树中第 K 小的元素"
problems = [230]
problem_id = 230
difficulty = "Medium"
weight = 230
summary = "二叉搜索树中第 K 小的元素的解题思路与 C++ 实现。"
+++

题目：[二叉搜索树中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/)


<a id="第二百三十题二叉搜索树中第-k-小的元素"></a>



第一次的解法是通过中序遍历将树存入vector，再通过下标k直接访问元素，但是超时了......应该是vector每次扩容的开销太大了

下面直接分析代码：

对于这段程序，只需要执行到第k个元素就可以停止了，后面的没必要去遍历，所以这里通过k来决定退出条件。

首先遍历左子树（这里使用的还是中序遍历）， 一直到叶子节点的下一个空节点，如果在这个过程中，k已经被减为了零，那么当前节点就是我们需要找的节点；反之，如果左子树已经遍历完毕，而k不为零，就回到父节点，再在父节点处执行一次--k的判断。最后，如果根节点和它的左子树的遍历完毕后，k还是没有为零，就开始遍历整颗右子树

```cpp
int kthSmallest(TreeNode* root, int& k)
{
    if(!root) return -1;

    int res_left = kthSmallest(root->left, k);
    if(res_left != -1) return res_left;

    if(--k == 0) return root->val;

    return kthSmallest(root->right, k);
}
```
