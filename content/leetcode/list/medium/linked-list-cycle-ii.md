+++
slug = "linked-list-cycle-ii"
title = "环形链表 II"
problems = [142]
problem_id = 142
difficulty = "Medium"
weight = 142
summary = "环形链表 II的解题思路与 C++ 实现。"
+++

题目：[环形链表 II](https://leetcode.cn/problems/linked-list-cycle-ii/)


<a id="第一百四十二题环形链表-ii"></a>



如图，环外的长度为a，slow指针进入环内走了b才与fast相遇，fast走完了n圈，也就是n（b+c）+ b的距离

根据两者相遇时的时间相同，可以得到等式：_<font style="color:#F8B881;">a</font>_<font style="color:#F8B881;">+(</font>_<font style="color:#F8B881;">n</font>_<font style="color:#F8B881;">+1)</font>_<font style="color:#F8B881;">b</font>_<font style="color:#F8B881;">+</font>_<font style="color:#F8B881;">nc</font>_<font style="color:#F8B881;">=2(</font>_<font style="color:#F8B881;">a</font>_<font style="color:#F8B881;">+</font>_<font style="color:#F8B881;">b</font>_<font style="color:#F8B881;">)⟹</font>_<font style="color:#F8B881;">a</font>_<font style="color:#F8B881;">=</font>_<font style="color:#F8B881;">c</font>_<font style="color:#F8B881;">+(</font>_<font style="color:#F8B881;">n</font>_<font style="color:#F8B881;">−1)(</font>_<font style="color:#F8B881;">b</font>_<font style="color:#F8B881;">+</font>_<font style="color:#F8B881;">c</font>_<font style="color:#F8B881;">)</font>

当n等于1时，a=c；此时如果放置一个指针从head处向后移动，同时另一个指针从slow与fast相遇的地方以相同的速度沿着c移动，那么两者最终会在环的入口处相遇；至于为什么不考虑n，而是直接取n为1，是因为n仅仅代表着相遇处的指针多走的圈数，最后两者还是会在入口相遇

<img src="/images/leetcode-list-medium/leetcode-list-medium-01.png" width="2000" title="" crop="0,0,1,1" id="HF5TL" class="ne-image" alt="环形链表中，环外长度 a、入口至相遇点长度 b 和返回入口长度 c 的示意" loading="lazy" decoding="async" height="1125">

```cpp
ListNode *detectCycle(ListNode *head)
    {
        if(head == nullptr || head->next == nullptr) return nullptr;
        ListNode *slow = head, *fast = head, *p1 = head;
        while(fast != nullptr)
        {
            slow = slow->next;
            if(fast->next == nullptr) return nullptr;
            fast = fast->next->next;
            if(slow == fast)
            {
                while(p1 != slow)
                {
                    p1 = p1->next;
                    slow = slow->next;
                }
                return p1;
            }
        }
        return nullptr;
    }
```
