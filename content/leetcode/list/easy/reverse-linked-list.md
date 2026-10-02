+++
slug = "reverse-linked-list"
title = "反转链表"
problems = [206]
problem_id = 206
difficulty = "Easy"
weight = 206
summary = "反转链表的解题思路与 C++ 实现。"
+++

题目：[反转链表](https://leetcode.cn/problems/reverse-linked-list/)


<a id="第二百零六题反转链表"></a>



<font style="color:#F38F39;">第一种解法：双指针</font>

思路如下：
原链表:1→2→3→4(pre=null)
1: null←1 2→3→4(pre=1)
2: null←1←2 3→4(pre=2)
3: null←1←2←3 4(pre=3)
4: null←1←2←3←4(pre=4)

循环终止的条件是：当前节点为nullptr，之后因为在上一次循环中已经指定pre等于上一次循环的curr，因此直接返回pre即可

```cpp
ListNode* reverseList(ListNode* head)
    {
        ListNode *pre = nullptr;
        ListNode *curr = head;
        while(curr)
        {
            ListNode* temp = curr->next;
            curr->next = pre;
            pre = curr;
            curr = temp;
        }
        return pre;
    }
```



<font style="color:#F38F39;">第二种解法：递归</font>

总体思路还是在双指针的基础上进行的

reverse函数接收当前节点与上一个节点，如果curr为空，也就是递归到了最后一个节点，就直接返回prev；

若未到达尾节点，就跟双指针解法一样curr和pre都向后移一位，并再次调用reverse（注：此时temp和curr就是移动过后的curr和prev）

在reverseList函数中对reverse的调用也是直接省去了curr和prev的初始化环节

```cpp
ListNode* reverse(ListNode* curr, ListNode* prev)
    {
        if(curr == nullptr) return prev;
        ListNode* temp = curr->next;
        curr->next = prev;
        return reverse(temp, curr);
    }

    ListNode* reverseList(ListNode* head)
    {
        return reverse(head, nullptr);
    }
```
