#### <font style="color:#DF2A3F;">第二十五题</font>：[K 个一组翻转链表](https://leetcode.cn/problems/reverse-nodes-in-k-group/)
```cpp
ListNode* reverseKGroup(ListNode* head, int k)
{
    // 统计节点个数
    int n = 0;
    for(ListNode* node = head; node; node = node->next)
    {
        n++;
    }

    ListNode dummy(0, head);
    ListNode* trailer = &dummy;
    ListNode* curr = head;
    ListNode* prev = nullptr;

    //外层循环：确保每次只翻转 k 个节点
    for(; k <= n; n -= k)
    {
        // 内层循环：执行翻转的操作
        for(int i = 0; i < k; i++)
        {
            ListNode* temp = curr->next;
            curr->next = prev;
            prev = curr;
            curr = temp;
        }

        // 将翻转后的节点组与其他节点进行连接
        /* trailer->next 原本指向的是翻转链表的第一个节点
           经过翻转之后，这个节点变成了最后一个节点 */
        ListNode* nxt = trailer->next;
        trailer->next = prev;
        nxt->next = curr;
        // 将 trailer 移动到下一组的前一个节点
        trailer = nxt;
    }
    return dummy.next;
}
```
