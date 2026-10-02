+++
slug = "add-two-numbers"
title = "两数相加"
problems = [2]
problem_id = 2
difficulty = "Medium"
weight = 2
summary = "两数相加的解题思路与 C++ 实现。"
+++

题目：[两数相加](https://leetcode.cn/problems/add-two-numbers/)


<a id="第二题两数相加"></a>



首先明确思路，逐节点的将l1和l2相加，如果遇到需要进位的情况，就单独将所进的位数保存起来，并加到下一次的sum中去，然后在同一次循环中构造好相加后的链表

```cpp
ListNode* addTwoNumbers(ListNode* l1, ListNode* l2)
{
    ListNode dummy(0);
    ListNode* curr = &dummy;

    int carry = 0;
    while(l1 || l2 || carry != 0)
    {
        int sum = carry;
        if(l1)
        {
            sum += l1->val;
            l1 = l1->next;
        }
        if(l2)
        {
            sum += l2->val;
            l2 = l2->next;
        }

        // 进位
        carry = sum / 10;
        int digit = sum % 10;
        curr->next = new ListNode(digit);
        curr = curr->next;
    }
    return dummy.next;
}
```
