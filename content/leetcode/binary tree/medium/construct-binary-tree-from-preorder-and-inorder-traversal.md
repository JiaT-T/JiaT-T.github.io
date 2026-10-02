+++
slug = "construct-binary-tree-from-preorder-and-inorder-traversal"
title = "从前序与中序遍历序列构造二叉树"
problems = [105]
problem_id = 105
difficulty = "Medium"
weight = 105
summary = "从前序与中序遍历序列构造二叉树的解题思路与 C++ 实现。"
+++

题目：[从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)


<a id="第一百零五题从前序与中序遍历序列构造二叉树"></a>



通过递归的方法来构造二叉树，可以拆解为三个步骤：
	**1).找到当前根节点**  -->  **2).找到左右子树的根节点**  -->  **3).递归深入**

因为前序遍历会先遍历所有根节点，所以第一步只需要对数组 preorder 的下标进行递增即可

同时根据中序遍历的特性，左子树与右子树分别会位于 inorder 数组中根节点的左右两侧，所以需要使用一种快速的方法，能够通过根节点的值直接在 inorder 数组中找到根节点对应的下标（也可以说是位置），这里选用的是**哈希表**。如此一来，左右子树的所有元素就也被找到了，对拆分出来的两个数组再次递归调用即可

注：这里比较难理解的是递归时选取的左右边界

对于<font style="background-color:#FBDE28;">左子树</font>：

**preorder的左边界**要加1，因为preorder的第一个元素是根节点，往后一个节点就是这个根节点的左子树的根节点；**右边界**就是左边界位置直接加上左子树元素个数

**inorder的左边界**保持不变；**右边界**是根节点位置向前移动一位

对于<font style="background-color:#FBDE28;">右子树</font>：

**preorder的左边界**为初始左边界加上左子树元素的个数再加一（跨过根节点），**右边界**保持不变

**inorder的左边界**是根节点位置向后移动一位；**右边界**保持不变

```cpp
class Solution
{
public:
    TreeNode* helper(vector<int>& preorder, vector<int>& inorder, int preorder_left, int inorder_left, int preorder_right, int inorder_right)
    {
        if(preorder_left > preorder_right) return nullptr;

        int root_value = preorder[preorder_left];
        int inorder_root = index[root_value];
        TreeNode* root = new TreeNode(root_value);

        int left_tree_size = inorder_root - inorder_left;

        root->left = helper(preorder, inorder, preorder_left + 1, inorder_left, preorder_left + left_tree_size, inorder_root - 1);

        root->right = helper(preorder, inorder, preorder_left + left_tree_size + 1, inorder_root + 1, preorder_right, inorder_right);

        return root;
    }

    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder)
    {
        int sz = inorder.size();
        for(int i = 0; i < sz; i++)
        {
            index[inorder[i]] = i;
        }
        return helper(preorder, inorder, 0, 0, sz-1, sz-1);
    }
private :
    std::unordered_map<int, int> index;
};
```
