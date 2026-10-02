+++
slug = "merge-two-sorted-lists"
title = "合并两个有序链表"
problems = [21]
problem_id = 21
difficulty = "Easy"
weight = 21
summary = "合并两个有序链表的解题思路与 C++ 实现。"
+++

题目：[合并两个有序链表](https://leetcode.cn/problems/merge-two-sorted-lists/)


<a id="第二十一题"></a>



使用的是递归的方法

首先判断是否有链表为空，如果是，则直接返回另一个链表

之后对list1和list2的值进行判断，更小者的下一个节点将调用原函数继续递归（比如情况一，list1的值更小，就让list1的next节点继续调用函数，将list1剩下的节点继续与list2比较）

```cpp
ListNode* mergeTwoLists(ListNode* list1, ListNode* list2)
    {
        if(list1 == nullptr) return list2;
        if(list2 == nullptr) return list1;
        if(list1->val < list2->val)
        {
            list1->next = mergeTwoLists(list1->next, list2);
            return list1;
        }
        else
        {
            list2->next = mergeTwoLists(list1, list2->next);
            return list2;
        }
    }
```
