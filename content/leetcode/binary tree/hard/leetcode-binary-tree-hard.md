---
title: "LeetCode 二叉树：困难题组"
slug: "leetcode-binary-tree-hard"
summary: "记录二叉树中的最大路径和的递归思路与 C++ 实现。"
categories: ["LeetCode"]
tags: ["LeetCode", "C++", "二叉树", "递归"]
date: "2026-06-02T14:00:22.000Z"
lastmod: "2026-06-02T14:08:09.000Z"
draft: false
yuque_slug: "et78lki3tfprbiwg"
source: "https://www.yuque.com/u62694975/iaaa/et78lki3tfprbiwg"
problems: [124]
---

<a id="vropZ"></a>
#### <span style="color: #DF2A3F">第一百二十四题</span>：[<span style="color: inherit">二叉树中的最大路径和</span>](<https://leetcode.cn/problems/binary-tree-maximum-path-sum/>)

<a id="u1c771ee6"></a>思路：对于任意一个节点，有两件不同的事要做：

<ol data-yuque-indent="2" style="margin-left: 4em"><li id="u95744007"><span id="ued066e1a">作为贡献值（向上传递）：此时，它只能选择【当前节点值】与【当前节点值 + 左子树贡献值 + 右子树贡献值】中的更大者</span></li><li id="u16c700f7"><span id="u837361f8">作为拐点（更新全局最大路径和）： 以当前节点为根的局部最大路径和为——</span><code id="u0de65436"><span id="u23e40f45">当前节点值 + 左子树最大贡献 + 右子树最大贡献</span></code><span id="ue0465d31">，如果之前记录过的最大和小于这个临时的和，就将其覆写</span></li></ol>

<a id="GHs4m"></a>
maxPathSum（）
```cpp
class Solution
{
public:
    int maxPathSum(TreeNode* root)
    {
        pathGain(root);
        return maxSum;
    }
private :
    int maxSum = INT_MIN;
    int pathGain(TreeNode* curr)
    {
        if(curr == nullptr) return 0;

        // 计算左右子树的最大贡献（不小于零）
        int left_gain = std::max(pathGain(curr->left), 0);
        int right_gain = std::max(pathGain(curr->right), 0);

        // 以当前节点为根的最大路径之和
        int curr_sum = curr->val + left_gain + right_gain;

        // 更新最大值
        maxSum = std::max(maxSum, curr_sum);

        // 向上传递
        return curr->val + std::max(left_gain, right_gain);
    }
};
```

原文：[hard](<https://www.yuque.com/u62694975/iaaa/et78lki3tfprbiwg>)
