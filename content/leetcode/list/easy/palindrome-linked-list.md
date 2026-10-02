+++
slug = "palindrome-linked-list"
title = "回文链表"
problems = [234]
problem_id = 234
difficulty = "Easy"
weight = 234
summary = "回文链表的解题思路与 C++ 实现。"
+++

题目：[回文链表](https://leetcode.cn/problems/palindrome-linked-list/)


<a id="第二百三十四题回文链表"></a>



使用的是双指针，以及上面那一题的反转函数

一种比较粗暴的方法是将链表转换成数组，之后再使用双指针从两边向中间遍历比较，但是这个方法的空间复杂度是O(n)

下面这个方法的思路是：找出链表的中点，翻转后半部分，再指定两个指针，分别从首节点与中间节点的后一个节点开始，向后进行遍历比较

那么问题就变成了<font style="color:#ECAA04;">如何找到链表的中点</font>：

首先定义两个指针：slow指针和fast指针

slow初始指向head，fast初始指向head->next，之后进行循环，slow每次向后移动一位，fast则移动两位，直到fast的下一个节点为空（偶数链表）或fast本身为空（奇数链表），此时可以判断----slow指向的节点就是前半部分链表的最后一个节点

之后对slow后面的另一半链表进行翻转，再逐个比较即可

```cpp
ListNode* reverse(ListNode* curr, ListNode* prev)
    {
        if(curr == nullptr) return prev;
        ListNode* temp = curr->next;
        curr->next = prev;
        return reverse(temp, curr);
    }

    bool isPalindrome(ListNode* head)
    {
        ListNode* slow = head;
        ListNode* fast = head->next;
        int half = 1;

        while(fast && fast->next)
        {
            slow = slow->next;
            fast = fast->next->next;
            half++;
        }

        slow = reverse(slow, nullptr);
        for(int i = 0; i < half; i++)
        {
            if(head->val != slow->val) return false;
            head = head->next;
            slow = slow->next;
        }
        return true;
    }
```
