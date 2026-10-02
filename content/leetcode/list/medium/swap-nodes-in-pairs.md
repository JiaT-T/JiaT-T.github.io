+++
slug = "swap-nodes-in-pairs"
title = "两两交换链表中的节点"
problems = [24]
problem_id = 24
difficulty = "Medium"
weight = 24
summary = "两两交换链表中的节点的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/cnlga8u2ysfoqru7"
+++

题目：[两两交换链表中的节点](https://leetcode.cn/problems/swap-nodes-in-pairs/)


<a id="第二十四题两两交换链表中的节点"></a>



使用的是迭代

就像之前写过的大部分链表的题目一样，要创建一个哨兵节点（前置节点）

首先哨兵节点指向第一个节点，之后进入循环，前置节点指向第二个节点，第一个节点指向第三个节点，最后让第二个节点指向原来的第一个节点，将前置节点指向此时的第二个节点，进入下一次循环

```cpp
ListNode* swapPairs(ListNode* head)
    {
        if( !head || !head->next ) return head;
        ListNode header1(0, head);
        ListNode* prev = &header1;

        while(prev->next && prev->next->next)
        {
            auto node1 = prev->next;
            auto node2 = prev->next->next;

            prev->next = node2;
            node1->next = node2->next;
            node2->next = node1;

            prev = node1;
        }

        return header1.next;
    }
```


<a id="Acr0E"></a>

<strong>补充解法：递归交换相邻节点</strong>

```cpp
ListNode* swapPairs(ListNode* head)
{
    if(head == nullptr || head->next == nullptr) return head;

    ListNode* newHead = head->next;
    head->next = swapPairs(newHead->next);
    newHead->next = head;
    return newHead;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/cnlga8u2ysfoqru7)
