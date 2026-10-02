+++
slug = "convert-sorted-list-to-binary-search-tree"
title = "有序链表转换二叉搜索树"
problems = [109]
problem_id = 109
difficulty = "Medium"
weight = 109
summary = "有序链表转换二叉搜索树的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/cnlga8u2ysfoqru7"
+++

题目：[有序链表转换二叉搜索树](https://leetcode.cn/problems/convert-sorted-list-to-binary-search-tree/)


<a id="第一百零九题有序链表转换二叉搜索树"></a>

<a id="qSFMg"></a>

<a id="ua961fbd0"></a>使用到了<strong>递归</strong>与<strong>双指针</strong>

<a id="vTsCg"></a>
sortedListToBST（）
```cpp
TreeNode* sortedListToBST(ListNode* head)
{
    if(head == nullptr) return nullptr;
    if(head->next == nullptr) return new TreeNode(head->val);

    // 找出链表的中点
    // 循环结束时，slow 即为树的根节点
    // 同时 slow 左边的链表为左子树，slow 右边为右子树
    ListNode *slow = head, *fast = head, *prev = nullptr;
    while(fast != nullptr && fast->next != nullptr)
    {
        prev = slow;
        slow = slow->next;
        fast = fast->next->next;
    }

    prev->next = nullptr;
    TreeNode* root = new TreeNode(slow->val);
    root->left = sortedListToBST(head);
    root->right = sortedListToBST(slow->next);
    return root;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/cnlga8u2ysfoqru7)
