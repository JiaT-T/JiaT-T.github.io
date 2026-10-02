+++
slug = "validate-binary-search-tree"
title = "验证二叉搜索树"
problems = [98]
problem_id = 98
difficulty = "Medium"
weight = 98
summary = "验证二叉搜索树的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/gvwgx0lykh5yempx"
+++

题目：[验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/)


<a id="第九十八题验证二叉搜索树"></a>



**解法一**：<u>通过中序遍历将整棵树装入vector，再判断数组是否单调</u>

具体实现非常简单，但不是一个好方法，因为他需要先将所有节点的数值装入容器，再进行比较，然而实际上每次比较只需要使用到两个节点，这会造成空间的浪费

所以应该使用“<font style="background-color:#FBDE28;">边遍历，边比较</font>”的方法

```cpp
void traversal(TreeNode* root, std::vector<int>& v)
{
    if(!root) return;

    traversal(root->left, v);

    v.push_back(root->val);

    traversal(root->right, v);
}

bool isValidBST(TreeNode* root)
{
    std::vector<int> vec;
    traversal(root, vec);

    int sz = vec.size();
    for(int i = 0; i < sz - 1; i++)
    {
        if(vec[i+1] <= vec[i]) return false;
    }
    return true;
}
```



**解法二**：<u>使用指针成员装载当前节点的父节点，并在访问当前节点时就继续比较</u>

这样就避免了在堆上分配内存，所有操作都只在栈上进行

相较于上一个方法，这个方法的空间复杂度从O(n)下降到了O(h),其中h为树的最大深度

```cpp
class Solution
{
public:
    bool isValidBST(TreeNode* root)
    {
        if(!root) return true;                         // 遍历到叶子节点之后进行剪枝，返回上一个节点
        if(!isValidBST(root->left)) return false;      // 如果左子树底下的节点已经不满足规则，就没必要继续遍历了
        if(prev && root->val <= prev->val) return false;
        prev = root;
        return isValidBST(root->right);                // 此时左边已经全部满足规则，只需要判断右子树是否也全部满足规则即可
    }
private :
    TreeNode* prev = nullptr;
};
```


<a id="rM2yw"></a>

<strong>补充解法：递归维护上下界</strong>

```cpp
bool isValid(TreeNode* root, long min_val, long max_val)
{
    if(root == nullptr) return true;
    if(root->val <= min_val || max_val <= root->val) return false;
    return isValid(root->left, min_val, root->val) &&
           isValid(root->right, root->val, max_val);
}
bool isValidBST(TreeNode* root)
{
    return isValid(root, LONG_MIN, LONG_MAX);
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/gvwgx0lykh5yempx)
