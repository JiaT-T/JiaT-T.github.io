\#### <font style="color:#DF2A3F;">第二十一题</font>：\[<font style="color:rgb(10, 132, 255);">合并两个有序链表</font>](https://leetcode.cn/problems/merge-two-sorted-lists/)

使用的是递归的方法



首先判断是否有链表为空，如果是，则直接返回另一个链表



之后对list1和list2的值进行判断，更小者的下一个节点将调用原函数继续递归（比如情况一，list1的值更小，就让list1的next节点继续调用函数，将list1剩下的节点继续与list2比较）



```cpp

ListNode\* mergeTwoLists(ListNode\* list1, ListNode\* list2)

&nbsp;   {

&nbsp;       if(list1 == nullptr) return list2;

&nbsp;       if(list2 == nullptr) return list1;

&nbsp;       if(list1->val < list2->val)

&nbsp;       {

&nbsp;           list1->next = mergeTwoLists(list1->next, list2);

&nbsp;           return list1;

&nbsp;       }

&nbsp;       else

&nbsp;       {

&nbsp;           list2->next = mergeTwoLists(list1, list2->next);

&nbsp;           return list2;

&nbsp;       }

&nbsp;   }

```



\#### <font style="color:#DF2A3F;">第一百一十四题</font>：\[环形链表](https://leetcode.cn/problems/linked-list-cycle/)

使用的是双指针（快慢指针）



如果链表中此存在环的话，那么两个指针就一定会在这个环内循环，也就一定会相遇，因此可以将两个指针相等作为链表中存在环的判断条件（至于为什么会相遇：这里令慢指针的速度为1，快指针速度为2，两者的相对速度为1，所以在进入环之后，相当于是快指针在以1的速度追慢指针，之后一定会追上）



<font style="background-color:#FBDE28;">注：这里的两个if一定要先判断head与fast是否为空！！！！！</font>



```cpp

bool hasCycle(ListNode \*head)

&nbsp;   {

&nbsp;       if(head == nullptr || head->next == nullptr) return false;

&nbsp;       ListNode \*slow = head, \*fast = head->next;

&nbsp;       while(slow != fast)

&nbsp;       {

&nbsp;           if( fast == nullptr || fast->next == nullptr) return false;

&nbsp;           slow = slow->next;

&nbsp;           fast = fast->next->next;

&nbsp;       }

&nbsp;       return true;

&nbsp;   }

```



\#### <font style="color:#DF2A3F;">第一百六十题</font>：\[<font style="color:#117CEE;">相交链表</font>](https://leetcode.cn/problems/intersection-of-two-linked-lists/)

设节点指针A，B分别指向两个链表的头节点，C为首个公共节点



链表A，B的长度分别为a，b，其中公共长度为c



因此，第一次从A走到C的距离是a-c，从B走到C的距离是b-c



当指针A先遍历完链表A，再遍历链表B，直到第二次遇到公共节点C，一共走了a+（b-c）的距离



当指针B先遍历完链表B，再遍历链表A，直到第二次遇到公共节点C，一共走了b+（a-c）的距离



此时可以发现两者所走过的距离相等，因此可以利用这个条件找到第一个公共节点C：



构造while循环，只要A与B指针不相同，就继续向后遍历，因为最后走的距离相同，也就是循环的次数相同，所以在同一个循环中进行两者的遍历即可



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1775536987303-96d113ec-6c22-4000-bf4a-312191e85f55.png" width="1604" title="" crop="0,0,1,1" id="u3e62db8c" class="ne-image">



```cpp

ListNode\* getIntersectionNode(ListNode \*headA, ListNode \*headB)

&nbsp;   {

&nbsp;       ListNode \*A = headA, \*B = headB;

&nbsp;       while(A != B)

&nbsp;       {

&nbsp;           A = A != nullptr ? A->next : headB;

&nbsp;           B = B != nullptr ? B->next : headA;

&nbsp;       }

&nbsp;       return A;

&nbsp;   }

```



\#### <font style="color:#DF2A3F;">第二百零六题</font>：\[反转链表](https://leetcode.cn/problems/reverse-linked-list/)

<font style="color:#F38F39;">第一种解法：双指针</font>



思路如下：  

原链表:1→2→3→4(pre=null)  

1: null←1 2→3→4(pre=1)  

2: null←1←2 3→4(pre=2)  

3: null←1←2←3 4(pre=3)  

4: null←1←2←3←4(pre=4)



循环终止的条件是：当前节点为nullptr，之后因为在上一次循环中已经指定pre等于上一次循环的curr，因此直接返回pre即可



```cpp

ListNode\* reverseList(ListNode\* head)

&nbsp;   {

&nbsp;       ListNode \*pre = nullptr;

&nbsp;       ListNode \*curr = head;

&nbsp;       while(curr)

&nbsp;       {

&nbsp;           ListNode\* temp = curr->next;

&nbsp;           curr->next = pre;

&nbsp;           pre = curr;

&nbsp;           curr = temp;

&nbsp;       }

&nbsp;       return pre;

&nbsp;   }

```







<font style="color:#F38F39;">第二种解法：递归</font>



总体思路还是在双指针的基础上进行的



reverse函数接收当前节点与上一个节点，如果curr为空，也就是递归到了最后一个节点，就直接返回prev；



若未到达尾节点，就跟双指针解法一样curr和pre都向后移一位，并再次调用reverse（注：此时temp和curr就是移动过后的curr和prev）



在reverseList函数中对reverse的调用也是直接省去了curr和prev的初始化环节



```cpp

ListNode\* reverse(ListNode\* curr, ListNode\* prev)

&nbsp;   {

&nbsp;       if(curr == nullptr) return prev;

&nbsp;       ListNode\* temp = curr->next;

&nbsp;       curr->next = prev;

&nbsp;       return reverse(temp, curr);

&nbsp;   }



&nbsp;   ListNode\* reverseList(ListNode\* head)

&nbsp;   {

&nbsp;       return reverse(head, nullptr);

&nbsp;   }

```







\#### <font style="color:#DF2A3F;">第二百三十四题</font>：\[回文链表](https://leetcode.cn/problems/palindrome-linked-list/)

使用的是双指针，以及上面那一题的反转函数



一种比较粗暴的方法是将链表转换成数组，之后再使用双指针从两边向中间遍历比较，但是这个方法的空间复杂度是O(n)



下面这个方法的思路是：找出链表的中点，翻转后半部分，再指定两个指针，分别从首节点与中间节点的后一个节点开始，向后进行遍历比较



那么问题就变成了<font style="color:#ECAA04;">如何找到链表的中点</font>：



首先定义两个指针：slow指针和fast指针



slow初始指向head，fast初始指向head->next，之后进行循环，slow每次向后移动一位，fast则移动两位，直到fast的下一个节点为空（偶数链表）或fast本身为空（奇数链表），此时可以判断----slow指向的节点就是前半部分链表的最后一个节点



之后对slow后面的另一半链表进行翻转，再逐个比较即可



```cpp

ListNode\* reverse(ListNode\* curr, ListNode\* prev)

&nbsp;   {

&nbsp;       if(curr == nullptr) return prev;

&nbsp;       ListNode\* temp = curr->next;

&nbsp;       curr->next = prev;

&nbsp;       return reverse(temp, curr);

&nbsp;   }



&nbsp;   bool isPalindrome(ListNode\* head)

&nbsp;   {

&nbsp;       ListNode\* slow = head;

&nbsp;       ListNode\* fast = head->next;

&nbsp;       int half = 1;



&nbsp;       while(fast \&\& fast->next)

&nbsp;       {

&nbsp;           slow = slow->next;

&nbsp;           fast = fast->next->next;

&nbsp;           half++;

&nbsp;       }



&nbsp;       slow = reverse(slow, nullptr);

&nbsp;       for(int i = 0; i < half; i++)

&nbsp;       {

&nbsp;           if(head->val != slow->val) return false;

&nbsp;           head = head->next;

&nbsp;           slow = slow->next;

&nbsp;       }

&nbsp;       return true;

&nbsp;   }

```

\#### <font style="color:#DF2A3F;">第二十一题</font>：\[<font style="color:rgb(10, 132, 255);">合并两个有序链表</font>](https://leetcode.cn/problems/merge-two-sorted-lists/)

使用的是递归的方法



首先判断是否有链表为空，如果是，则直接返回另一个链表



之后对list1和list2的值进行判断，更小者的下一个节点将调用原函数继续递归（比如情况一，list1的值更小，就让list1的next节点继续调用函数，将list1剩下的节点继续与list2比较）



```cpp

ListNode\* mergeTwoLists(ListNode\* list1, ListNode\* list2)

&nbsp;   {

&nbsp;       if(list1 == nullptr) return list2;

&nbsp;       if(list2 == nullptr) return list1;

&nbsp;       if(list1->val < list2->val)

&nbsp;       {

&nbsp;           list1->next = mergeTwoLists(list1->next, list2);

&nbsp;           return list1;

&nbsp;       }

&nbsp;       else

&nbsp;       {

&nbsp;           list2->next = mergeTwoLists(list1, list2->next);

&nbsp;           return list2;

&nbsp;       }

&nbsp;   }

```



\#### <font style="color:#DF2A3F;">第一百一十四题</font>：\[环形链表](https://leetcode.cn/problems/linked-list-cycle/)

使用的是双指针（快慢指针）



如果链表中此存在环的话，那么两个指针就一定会在这个环内循环，也就一定会相遇，因此可以将两个指针相等作为链表中存在环的判断条件（至于为什么会相遇：这里令慢指针的速度为1，快指针速度为2，两者的相对速度为1，所以在进入环之后，相当于是快指针在以1的速度追慢指针，之后一定会追上）



<font style="background-color:#FBDE28;">注：这里的两个if一定要先判断head与fast是否为空！！！！！</font>



```cpp

bool hasCycle(ListNode \*head)

&nbsp;   {

&nbsp;       if(head == nullptr || head->next == nullptr) return false;

&nbsp;       ListNode \*slow = head, \*fast = head->next;

&nbsp;       while(slow != fast)

&nbsp;       {

&nbsp;           if( fast == nullptr || fast->next == nullptr) return false;

&nbsp;           slow = slow->next;

&nbsp;           fast = fast->next->next;

&nbsp;       }

&nbsp;       return true;

&nbsp;   }

```



\#### <font style="color:#DF2A3F;">第一百六十题</font>：\[<font style="color:#117CEE;">相交链表</font>](https://leetcode.cn/problems/intersection-of-two-linked-lists/)

设节点指针A，B分别指向两个链表的头节点，C为首个公共节点



链表A，B的长度分别为a，b，其中公共长度为c



因此，第一次从A走到C的距离是a-c，从B走到C的距离是b-c



当指针A先遍历完链表A，再遍历链表B，直到第二次遇到公共节点C，一共走了a+（b-c）的距离



当指针B先遍历完链表B，再遍历链表A，直到第二次遇到公共节点C，一共走了b+（a-c）的距离



此时可以发现两者所走过的距离相等，因此可以利用这个条件找到第一个公共节点C：



构造while循环，只要A与B指针不相同，就继续向后遍历，因为最后走的距离相同，也就是循环的次数相同，所以在同一个循环中进行两者的遍历即可



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1775536987303-96d113ec-6c22-4000-bf4a-312191e85f55.png" width="1604" title="" crop="0,0,1,1" id="u3e62db8c" class="ne-image">



```cpp

ListNode\* getIntersectionNode(ListNode \*headA, ListNode \*headB)

&nbsp;   {

&nbsp;       ListNode \*A = headA, \*B = headB;

&nbsp;       while(A != B)

&nbsp;       {

&nbsp;           A = A != nullptr ? A->next : headB;

&nbsp;           B = B != nullptr ? B->next : headA;

&nbsp;       }

&nbsp;       return A;

&nbsp;   }

```



\#### <font style="color:#DF2A3F;">第二百零六题</font>：\[反转链表](https://leetcode.cn/problems/reverse-linked-list/)

<font style="color:#F38F39;">第一种解法：双指针</font>



思路如下：  

原链表:1→2→3→4(pre=null)  

1: null←1 2→3→4(pre=1)  

2: null←1←2 3→4(pre=2)  

3: null←1←2←3 4(pre=3)  

4: null←1←2←3←4(pre=4)



循环终止的条件是：当前节点为nullptr，之后因为在上一次循环中已经指定pre等于上一次循环的curr，因此直接返回pre即可



```cpp

ListNode\* reverseList(ListNode\* head)

&nbsp;   {

&nbsp;       ListNode \*pre = nullptr;

&nbsp;       ListNode \*curr = head;

&nbsp;       while(curr)

&nbsp;       {

&nbsp;           ListNode\* temp = curr->next;

&nbsp;           curr->next = pre;

&nbsp;           pre = curr;

&nbsp;           curr = temp;

&nbsp;       }

&nbsp;       return pre;

&nbsp;   }

```







<font style="color:#F38F39;">第二种解法：递归</font>



总体思路还是在双指针的基础上进行的



reverse函数接收当前节点与上一个节点，如果curr为空，也就是递归到了最后一个节点，就直接返回prev；



若未到达尾节点，就跟双指针解法一样curr和pre都向后移一位，并再次调用reverse（注：此时temp和curr就是移动过后的curr和prev）



在reverseList函数中对reverse的调用也是直接省去了curr和prev的初始化环节



```cpp

ListNode\* reverse(ListNode\* curr, ListNode\* prev)

&nbsp;   {

&nbsp;       if(curr == nullptr) return prev;

&nbsp;       ListNode\* temp = curr->next;

&nbsp;       curr->next = prev;

&nbsp;       return reverse(temp, curr);

&nbsp;   }



&nbsp;   ListNode\* reverseList(ListNode\* head)

&nbsp;   {

&nbsp;       return reverse(head, nullptr);

&nbsp;   }

```







\#### <font style="color:#DF2A3F;">第二百三十四题</font>：\[回文链表](https://leetcode.cn/problems/palindrome-linked-list/)

使用的是双指针，以及上面那一题的反转函数



一种比较粗暴的方法是将链表转换成数组，之后再使用双指针从两边向中间遍历比较，但是这个方法的空间复杂度是O(n)



下面这个方法的思路是：找出链表的中点，翻转后半部分，再指定两个指针，分别从首节点与中间节点的后一个节点开始，向后进行遍历比较



那么问题就变成了<font style="color:#ECAA04;">如何找到链表的中点</font>：



首先定义两个指针：slow指针和fast指针



slow初始指向head，fast初始指向head->next，之后进行循环，slow每次向后移动一位，fast则移动两位，直到fast的下一个节点为空（偶数链表）或fast本身为空（奇数链表），此时可以判断----slow指向的节点就是前半部分链表的最后一个节点



之后对slow后面的另一半链表进行翻转，再逐个比较即可



```cpp

ListNode\* reverse(ListNode\* curr, ListNode\* prev)

&nbsp;   {

&nbsp;       if(curr == nullptr) return prev;

&nbsp;       ListNode\* temp = curr->next;

&nbsp;       curr->next = prev;

&nbsp;       return reverse(temp, curr);

&nbsp;   }



&nbsp;   bool isPalindrome(ListNode\* head)

&nbsp;   {

&nbsp;       ListNode\* slow = head;

&nbsp;       ListNode\* fast = head->next;

&nbsp;       int half = 1;



&nbsp;       while(fast \&\& fast->next)

&nbsp;       {

&nbsp;           slow = slow->next;

&nbsp;           fast = fast->next->next;

&nbsp;           half++;

&nbsp;       }



&nbsp;       slow = reverse(slow, nullptr);

&nbsp;       for(int i = 0; i < half; i++)

&nbsp;       {

&nbsp;           if(head->val != slow->val) return false;

&nbsp;           head = head->next;

&nbsp;           slow = slow->next;

&nbsp;       }

&nbsp;       return true;

&nbsp;   }

```



