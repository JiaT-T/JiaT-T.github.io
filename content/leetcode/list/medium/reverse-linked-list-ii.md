+++
slug = "reverse-linked-list-ii"
title = "反转链表 II"
problems = [92]
problem_id = 92
difficulty = "Medium"
weight = 92
summary = "反转链表 II的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/cnlga8u2ysfoqru7"
+++

题目：[反转链表 II](https://leetcode.cn/problems/reverse-linked-list-ii/)


<a id="第九十二题反转链表-ii"></a>

<a id="l9k3z"></a>

<a id="u20842552"></a><strong>核心思想：将 left 的前一个节点指向 right，将 left 指向 right 的下一个节点</strong>

<a id="u0e5fe76d"></a>所以一共需要<strong>找到三个节点</strong>的位置，这里使用的是两个遍历，分别定位 <strong>left 的前一个节点 / left节点</strong>和 <strong>right 的下一个节点</strong>

<a id="QPjrk"></a>
reverseBetween（）
```cpp
ListNode* reverse(ListNode* prev, ListNode* curr, ListNode* last)
{
    if(curr == last)
    {
        return prev;
    }
    ListNode* temp = curr->next;
    curr->next = prev;
    return reverse(curr, temp, last);
}
ListNode* reverseBetween(ListNode* head, int left, int right)
{
    ListNode* dummy = new ListNode(0);
    dummy->next = head;
    ListNode* pre = dummy;

    // 找到 pre（left 的前一个节点）
    for(int i = 1; i < left; i++)
    {
        pre = pre->next;
    }
    // 通过 pre 可以定位到 left
    ListNode* left_node = pre->next;

    // 找到 right 的下一个节点
    ListNode* last = left_node;
    for(int i = left; i <= right; i++)
    {
        last = last->next;
    }

    // 将【left，right】区间翻转
    // 这里的 new_head 就是之前的 right
    ListNode* new_head = reverse(nullptr, left_node, last);
    pre->next = new_head;
    left_node->next = last;

    return dummy->next;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/cnlga8u2ysfoqru7)
