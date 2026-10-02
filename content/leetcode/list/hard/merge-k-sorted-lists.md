+++
slug = "merge-k-sorted-lists"
title = "合并 K 个升序链表"
problems = [23]
problem_id = 23
difficulty = "Hard"
weight = 23
summary = "合并 K 个升序链表的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/av5kg1ai1uglgc6i"
+++

题目：[合并 K 个升序链表](https://leetcode.cn/problems/merge-k-sorted-lists/)


<a id="第二十三题合并-k-个升序链表"></a>

<a id="bf9DM"></a>

<a id="u201dc356"></a>参考：<a id="OCxcY"></a>[https://leetcode.cn/problems/merge-k-sorted-lists/solutions/2384305/liang-chong-fang-fa-zui-xiao-dui-fen-zhi-zbzx/?envType=problem-list-v2&amp;envId=91oI3WTD](<https://leetcode.cn/problems/merge-k-sorted-lists/solutions/2384305/liang-chong-fang-fa-zui-xiao-dui-fen-zhi-zbzx/?envType=problem-list-v2&envId=91oI3WTD>)

<a id="ua6fedfe8"></a>首先明确思路：对于第一个插入的节点，一定是某一个链表的头节点，而第二个节点，不是当前节点的下一个节点，就是其他链表的头节点...此时需要有一个数据结构，能够<strong>找到并去除最小节点</strong>，同时还要<strong>能插入新节点</strong>——这里使用的是“<strong>最小堆</strong>”

<a id="u9982850f"></a>首先定义初始状态——将三个头节点存入堆中，然后找出最小节点作为头节点；接着判断被删去的节点是否存在下一个节点，如果有，就将其存入堆中，之后进行进行相同的判断，直到堆为空

<a id="kEXaE"></a>
mergeKLists（）
```cpp
ListNode* mergeKLists(vector<ListNode*>& lists)
{
    auto cmp = [](ListNode* a, ListNode* b)
    {
        return a->val > b -> val;
    };
    std::priority_queue<ListNode*, std::vector<ListNode*>, decltype(cmp)> less_heap;

    for(auto head : lists)
    {
        if(head != nullptr)
            less_heap.push(head);
    }

    ListNode dummy(0);
    ListNode* head = &dummy;
    while(!less_heap.empty())
    {
        auto node = less_heap.top();
        less_heap.pop();
        if(node->next != nullptr)
        {
            less_heap.push(node->next);
        }
        head->next = node;
        head = head->next;
    }
    return dummy.next;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/av5kg1ai1uglgc6i)
