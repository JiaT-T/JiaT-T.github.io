+++
slug = "copy-list-with-random-pointer"
title = "随机链表的复制"
problems = [138]
problem_id = 138
difficulty = "Medium"
weight = 138
summary = "随机链表的复制的解题思路与 C++ 实现。"
+++

题目：[随机链表的复制](https://leetcode.cn/problems/copy-list-with-random-pointer/)


<a id="第一百三十八题随机链表的复制"></a>



使用到的是哈希表

思路：因为第一次遍历复制各个结点的时候，是不知道后面的节点的，因此一次遍历无法将random元素对应上去，所以一共需要两次遍历：第一次复制所有节点并并对应的random与当前节点绑定，第二次将当前节点的random元素指向对应的成员

```cpp
Node* copyRandomList(Node* head)
    {
        if(head == nullptr) return nullptr;
        Node* curr = head;
        std::unordered_map<Node*, Node*> map;

        while(curr != nullptr)
        {
            map[curr] = new Node(curr->val);
            curr = curr->next;
        }

        curr = head;
        while(curr != nullptr)
        {
            map[curr]->next = map[curr->next];
            map[curr]->random = map[curr->random];
            curr = curr->next;
        }
        return map[head];
    }
```
