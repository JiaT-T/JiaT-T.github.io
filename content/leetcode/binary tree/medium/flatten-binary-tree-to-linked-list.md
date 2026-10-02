+++
slug = "flatten-binary-tree-to-linked-list"
title = "二叉树展开为链表"
problems = [114]
problem_id = 114
difficulty = "Medium"
weight = 114
summary = "二叉树展开为链表的解题思路与 C++ 实现。"
+++

题目：[二叉树展开为链表](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/)


<a id="第一百一十四题二叉树展开为链表"></a>



因为要求O(1)的空间复杂度，因此不能再使用额外的容器，所以这里使用了一个原地算法

思路如下：
	最终结果是将原来的树退化为了一条沿着右子树不断延伸的链表，根据结果不难发现：越<u>是靠右的节点，在链表中的位置越靠前；而越是靠左的节点，在链表中的位置越往后</u>

因此，<font style="background-color:#FBDE28;">可以通过迭代，每次将父节点的整棵左子树插入父节点与右子树之间</font>

<img src="/images/leetcode-binary-tree-medium/leetcode-binary-tree-medium-01.png" width="562" title="" crop="0,0,1,1" id="u2c813c24" class="ne-image" alt="二叉树按先序顺序展开为 1 至 6 的右指针链表" loading="lazy" decoding="async" height="249">

具体实现：

先确定迭代终止条件：当前节点为空

之后判断当前节点是否存在左节点（因为需要做的就是将左子树插入），如果左子树不存在，就可以认为此时位于最左边的节点，也就是此时这一支已经满足了单链表要求；然后就可以对右子树进行遍历，当到达右子树最后一个结点之后，就把父节点的整颗右子树挂在当前节点的右枝，再将根节点的左子树完整的移动到右子树，左子树置空即可

```cpp
void flatten(TreeNode* root)
{
    while(root)
    {
        if(root->left)
        {
            auto temp = root->left;
            while(temp->right) temp = temp->right;
            temp->right = root->right;
            root->right = root->left;
            root->left = nullptr;
        }
        root = root->right;
    }
}
```
