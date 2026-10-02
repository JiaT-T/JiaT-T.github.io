+++
slug = "intersection-of-two-linked-lists"
title = "相交链表"
problems = [160]
problem_id = 160
difficulty = "Easy"
weight = 160
summary = "相交链表的解题思路与 C++ 实现。"
+++

题目：[相交链表](https://leetcode.cn/problems/intersection-of-two-linked-lists/)


<a id="第一百六十题"></a>



设节点指针A，B分别指向两个链表的头节点，C为首个公共节点

链表A，B的长度分别为a，b，其中公共长度为c

因此，第一次从A走到C的距离是a-c，从B走到C的距离是b-c

当指针A先遍历完链表A，再遍历链表B，直到第二次遇到公共节点C，一共走了a+（b-c）的距离

当指针B先遍历完链表B，再遍历链表A，直到第二次遇到公共节点C，一共走了b+（a-c）的距离

此时可以发现两者所走过的距离相等，因此可以利用这个条件找到第一个公共节点C：

构造while循环，只要A与B指针不相同，就继续向后遍历，因为最后走的距离相同，也就是循环的次数相同，所以在同一个循环中进行两者的遍历即可

<img src="/images/leetcode-list-easy/leetcode-list-easy-01.png" width="1604" title="" crop="0,0,1,1" id="u3e62db8c" class="ne-image" alt="链表 headA 与 headB 在首个公共节点汇合，并共享后续尾部" loading="lazy" decoding="async" height="904">

```cpp
ListNode* getIntersectionNode(ListNode *headA, ListNode *headB)
    {
        ListNode *A = headA, *B = headB;
        while(A != B)
        {
            A = A != nullptr ? A->next : headB;
            B = B != nullptr ? B->next : headA;
        }
        return A;
    }
```
