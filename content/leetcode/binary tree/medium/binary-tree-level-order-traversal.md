+++
slug = "binary-tree-level-order-traversal"
title = "二叉树的层序遍历"
problems = [102]
problem_id = 102
difficulty = "Medium"
weight = 102
summary = "二叉树的层序遍历的解题思路与 C++ 实现。"
+++

题目：[二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/)


<a id="第一百零二题-二叉树的层序遍历"></a>



使用的是<font style="background-color:#FBDE28;">队列与深度优先搜索</font>

函数返回值为二维数组，因此需要使用多个一维数组将每一层的值存起来，而使用队列可以实现单独存储每一层的效果（FIFO）

首先判断根节点是否为空，不为空则直接入队

定义两个循环，外层循环用于记录每一层所有的值（相对于整棵树进行），内层循环用于将单层内的所有值一个一个的压入用于临时存储的vec中（相对于单层进行）

通过size，可以知道每一层需要弹出的元素的数量，从而得知哪些元素是同一层的



注：<font style="background-color:#FBDE28;">性能优化</font>：

1.提前将队列的首元素存储起来，避免后续对.front()函数的多次调用

2.使用std::move()可以避免不必要的拷贝（因为vec被来就是外层循环的局部变量，当res的push操作被执行时，也就意味着这一层的循环终止了）

```cpp
vector<vector<int>> levelOrder(TreeNode* root)
{
    std::queue<TreeNode*> que;
    std::vector<std::vector<int>> res;
    if(root) que.push(root);
    while(!que.empty())
    {
        int size = que.size();
        std::vector<int> vec;
        vec.reserve(size);
        while(size)
        {
            TreeNode* curr = que.front();
            que.pop();

            vec.push_back(curr->val);
            if(curr->left) que.push(curr->left);
            if(curr->right) que.push(curr->right);
            size--;
        }
        res.push_back(std::move(vec));
    }
    return res;
}
```
