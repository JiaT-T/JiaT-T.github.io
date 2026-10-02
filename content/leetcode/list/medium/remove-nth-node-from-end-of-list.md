+++
slug = "remove-nth-node-from-end-of-list"
title = "删除链表的倒数第 N 个结点"
problems = [19]
problem_id = 19
difficulty = "Medium"
weight = 19
summary = "删除链表的倒数第 N 个结点的解题思路与 C++ 实现。"
+++

题目：[删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/)


<a id="第十九题"></a>



使用的是双指针

定义左指针left和右指针right，初始都先指向头结点的前一个结点（哨兵节点），然后先将right指针向后移动n的距离，这样当right指针遍历到尾节点时，left指针恰好处于right指针后n个位置，也就是倒数第n个节点。

到达目标位置之后，先将需要删除的节点保存在一个临时变量中，避免内存泄漏，再将上一个节点的指向改为当前节点的下一个节点，最后delete当前节点，并返回头节点

```cpp
ListNode* removeNthFromEnd(ListNode* head, int n)
    {
        ListNode dummyNode(0, head);
        ListNode* left = &dummyNode;
        ListNode* right = &dummyNode;
        for(int i = 0; i < n; i++)
        {
            right = right->next;
        }

        while(right->next != nullptr)
        {
            right = right->next;
            left  = left->next;
        }
        auto temp = left->next;
        left->next = left->next->next;
        delete temp;
        return dummyNode.next;
    }
```
