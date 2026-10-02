+++
slug = "linked-list-cycle"
title = "环形链表"
problems = [141]
problem_id = 141
difficulty = "Easy"
weight = 141
summary = "环形链表的解题思路与 C++ 实现。"
+++

题目：[环形链表](https://leetcode.cn/problems/linked-list-cycle/)


<a id="第一百一十四题环形链表"></a>



使用的是双指针（快慢指针）

如果链表中此存在环的话，那么两个指针就一定会在这个环内循环，也就一定会相遇，因此可以将两个指针相等作为链表中存在环的判断条件（至于为什么会相遇：这里令慢指针的速度为1，快指针速度为2，两者的相对速度为1，所以在进入环之后，相当于是快指针在以1的速度追慢指针，之后一定会追上）

<font style="background-color:#FBDE28;">注：这里的两个if一定要先判断head与fast是否为空！！！！！</font>

```cpp
bool hasCycle(ListNode *head)
    {
        if(head == nullptr || head->next == nullptr) return false;
        ListNode *slow = head, *fast = head->next;
        while(slow != fast)
        {
            if( fast == nullptr || fast->next == nullptr) return false;
            slow = slow->next;
            fast = fast->next->next;
        }
        return true;
    }
```
