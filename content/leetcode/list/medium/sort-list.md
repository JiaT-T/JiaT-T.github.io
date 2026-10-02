+++
slug = "sort-list"
title = "排序链表"
problems = [148]
problem_id = 148
difficulty = "Medium"
weight = 148
summary = "排序链表的解题思路与 C++ 实现。"
+++

题目：[排序链表](https://leetcode.cn/problems/sort-list/)


<a id="第一百四十八题排序链表"></a>



<font style="background-color:#F3BB2F;">解法一：归并排序（分治）</font>

<font style="color:#000000;">时间复杂度：O(</font>_<font style="color:#000000;">n</font>_<font style="color:#000000;">log</font>_<font style="color:#000000;">n</font>_<font style="color:#000000;">)，空间复杂度：O(log</font>_<font style="color:#000000;">n</font>_<font style="color:#000000;">)</font>

<font style="color:#000000;">从上至下将链表拆分为长度为一的单链表，然后先对长度为1的链表排序，合并两个链表；</font>

<font style="color:#000000;">再对长度为2的两个链表排序，之后合并....以此类推，每次排序并合并一半链表，最终就可以得到有序的链表</font>

具体实现：

mergeSort（）：

在头部定义一个哨兵节点，然后遍历比较left与right的值，如果left更小，就将当前left节点接到哨兵节点后面，并将left向后移动一位，继续比较（right同理）；最后当left或者right其中一个为空，也就是该子链表遍历完成时，就直接将另一个链表接到末尾，此时返回的哨兵节点的next就是排序后的链表的头节点



sortList（）：
	在主函数中，需要不断地将链表分为两半（通过递归调用），之后每一层递归都会调用mergeSort函数对当前分割出来的两个链表进行排序，直到最后合成回初始的链表



<font style="background-color:#F3BB2F;">解法二：归并排序（迭代）</font>

<font style="color:#DF2A3F;">ps：这里我还没看明白，之后再补上....................</font>

```cpp
class Solution
{
public:
    ListNode* mergeSort(ListNode* left, ListNode* right)
    {
        ListNode* dummyNode = new ListNode(0);
        ListNode* trail = dummyNode;
        while(left && right)
        {
            if(left->val < right->val)
            {
                trail->next = left;
                left = left->next;
            }
            else
            {
                trail->next = right;
                right = right->next;
            }
            trail = trail->next;
        }
        if(left)
            trail->next = left;
        else
            trail->next = right;

        return dummyNode->next;
    }

    ListNode* sortList(ListNode* head)
    {
        if(!head || !head->next) return head;

        ListNode *slow = head, *fast = head->next;
        while(fast && fast->next)
        {
            slow = slow->next;
            fast = fast->next->next;
        }
        ListNode *second = slow->next;
        slow->next = nullptr;
        ListNode *first = head;

        first = sortList(first);
        second = sortList(second);

        return mergeSort(first, second);
    }
};
```
