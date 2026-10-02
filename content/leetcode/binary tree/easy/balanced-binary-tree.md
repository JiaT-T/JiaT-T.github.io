+++
slug = "balanced-binary-tree"
title = "平衡二叉树"
problems = [110]
problem_id = 110
difficulty = "Easy"
weight = 110
summary = "平衡二叉树的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/ra46ilsmcmakspvr"
+++

题目：[平衡二叉树](https://leetcode.cn/problems/balanced-binary-tree/)


<a id="第一百一十题平衡二叉树"></a>

<a id="VVHAR"></a>

<a id="U5AjY"></a>
```cpp
int depth(TreeNode* curr, bool& res)
{
    if(curr == nullptr) return 0;

    int left = depth(curr->left, res);
    int right = depth(curr->right, res);

    if(!res) return 0;

    if(std::abs(left - right) > 1)
        res = false;

    return std::max(left, right) + 1;
}
bool isBalanced(TreeNode* root)
{
    bool res = true;
    depth(root, res);
    return res;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ra46ilsmcmakspvr)
